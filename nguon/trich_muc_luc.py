#!/usr/bin/env python3
"""Trích số liệu thẳng từ Mục lục Bản 9.2 (tệp Word) để kiểm web, không cần thư viện ngoài.

Dùng: python3 nguon/trich_muc_luc.py [đường dẫn tệp .docx]
Ghi: nguon/du-lieu/muc_luc_92.json (lịch ba năm theo buổi và bảng 32 Trạm đọc từ Word).
Tệp Word gốc chỉ được đọc, không bị sửa.
"""
import json, re, sys, zipfile, hashlib
from pathlib import Path
import xml.etree.ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
GOC = Path(__file__).resolve().parents[2]
MAC_DINH = GOC / "4_HO-SO-THIET-KE" / "MỤC LỤC CHƯƠNG TRÌNH TOÁN TƯ DUY 3 NĂM - BẢN 9.2 (CHỜ CÔ DUYỆT).docx"


def doc_docx(duong_dan):
    with zipfile.ZipFile(duong_dan) as z:
        goc = ET.fromstring(z.read("word/document.xml"))
    thanh = []
    for el in goc.find(W + "body"):
        if el.tag == W + "p":
            t = "".join(x.text or "" for x in el.iter(W + "t"))
            if t.strip():
                thanh.append(("p", t))
        elif el.tag == W + "tbl":
            hang = []
            for tr in el.iter(W + "tr"):
                o = []
                for tc in tr.findall(W + "tc"):
                    o.append(" / ".join("".join(x.text or "" for x in p.iter(W + "t")) for p in tc.findall(W + "p")).strip())
                hang.append(o)
            thanh.append(("tbl", hang))
    return thanh


def so(s):
    m = re.match(r"\d+", s.strip())
    return int(m.group()) if m else None


def trich(duong_dan):
    thanh = doc_docx(duong_dan)
    lich = {}      # năm -> {"tieu_de":..., "hang":[...]}
    tram = []      # bảng Phần 2: mã, tên, mạch, buổi, số mục
    nam_hien = 0
    for loai, nd in thanh:
        if loai == "p":
            m = re.match(r"1\.(\d)\. Năm (\d+ – \d+) tuổi · (\d+) tuần học · (\d+) buổi × (\d+)′", nd)
            if m:
                nam_hien = int(m.group(1))
                lich[nam_hien] = {"tuoi": m.group(2), "tuan": int(m.group(3)), "buoi": int(m.group(4)),
                                  "phut": int(m.group(5)), "hang": []}
            continue
        # bảng
        dau = nd[0] if nd else []
        if dau[:3] == ["Khối", "Nội dung", "Số buổi"] and nam_hien:
            for r in nd[1:]:
                lich[nam_hien]["hang"].append({"khoi": r[0], "noi_dung": r[1], "buoi": so(r[2])})
        elif dau[:5] == ["Mã", "Tên Trạm", "Mạch", "Buổi", "Số mục"]:
            for r in nd[1:]:
                tram.append({"ma": r[0], "ten": r[1], "mach": r[2], "buoi": so(r[3]), "so_muc": so(r[4])})
    return lich, tram


def main():
    nguon = Path(sys.argv[1]) if len(sys.argv) > 1 else MAC_DINH
    lich, tram = trich(nguon)
    out = {
        "nguon": nguon.name,
        "md5_nguon": hashlib.md5(nguon.read_bytes()).hexdigest(),
        "lich": lich,
        "tram": tram,
    }
    dich = Path(__file__).resolve().parent / "du-lieu" / "muc_luc_92.json"
    dich.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print("Đã ghi", dich, "· Trạm:", len(tram), "· năm:", sorted(lich))


if __name__ == "__main__":
    main()
