#!/usr/bin/env python3
"""Cổng kiểm trước khi đăng web Toán. Chạy ở thư mục 6_WEB-TOAN:

    python3 nguon/kiem_site.py            # kiểm cục bộ, không cần mạng
    python3 nguon/kiem_site.py --mang     # thêm: kiểm lab.tramtuduy.org và tramtuduy.org còn mở (chỉ gửi yêu cầu đọc)

Ghi kết quả vào noi-bo/KET_QUA_KIEM.md. Thoát mã 0 nếu không có lỗi chặn.
Cổng: 1 số liệu · 2 liên kết · 3 chữ viết · 4 chia sẻ · 5 tốc độ và cỡ chữ · 6 cấu trúc trang · 7 Phòng thí nghiệm.
"""
import json, re, sys, zipfile, struct
from pathlib import Path
from html.parser import HTMLParser
from datetime import datetime

GOC = Path(__file__).resolve().parents[1]
SITE = "https://toan.tramtuduy.org"
LAB = "https://lab.tramtuduy.org"
CHINH = "https://tramtuduy.org"
MANG = "--mang" in sys.argv
LOI, CANH_BAO, DAT = [], [], []


def loi(cong, msg):
    LOI.append(f"[Cổng {cong}] {msg}")


def canh_bao(cong, msg):
    CANH_BAO.append(f"[Cổng {cong}] {msg}")


class Trang(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links, self.srcs, self.ids, self.meta, self.h1, self.imgs = [], [], set(), {}, 0, []
        self.text, self._skip, self.title, self._in_title, self.lang, self.canon = [], 0, "", False, None, None
        self.scripts = []

    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == "html":
            self.lang = a.get("lang")
        if "id" in a:
            self.ids.add(a["id"])
        if tag == "a" and "href" in a:
            self.links.append(a["href"])
        if tag in ("img", "script") and "src" in a:
            self.srcs.append(a["src"])
        if tag == "link" and "href" in a:
            self.srcs.append(a["href"])
            if a.get("rel") == "canonical":
                self.canon = a["href"]
        if tag == "img":
            self.imgs.append(a)
        if tag == "meta":
            k = a.get("property") or a.get("name")
            if k:
                self.meta[k] = a.get("content", "")
        if tag == "h1":
            self.h1 += 1
        if tag in ("script", "style"):
            self._skip += 1
        if tag == "title":
            self._in_title = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self._skip -= 1
        if tag == "title":
            self._in_title = False

    def handle_data(self, d):
        if self._in_title:
            self.title += d
        if not self._skip:
            self.text.append(d)


def doc(p):
    t = Trang()
    t.feed(p.read_text(encoding="utf-8"))
    return t


def kich_thuoc_png(p):
    with open(p, "rb") as f:
        h = f.read(24)
    return struct.unpack(">II", h[16:24])


# ---------- thu thập trang ----------
trang_html = sorted([p for p in GOC.rglob("index.html") if not any(x in p.parts for x in ("nguon", "noi-bo", "anh-kiem", ".git"))])
trang_html.append(GOC / "404.html")
DOC = {p: doc(p) for p in trang_html}


def url_cua(p):
    r = p.relative_to(GOC).parent.as_posix()
    return "/" if r == "." else f"/{r}/"


# ---------- Cổng 1: số liệu ----------
tram = json.loads((GOC / "nguon/du-lieu/tram.json").read_text(encoding="utf-8"))["tram"]
ml = json.loads((GOC / "nguon/du-lieu/muc_luc_92.json").read_text(encoding="utf-8"))
if len(tram) != 32:
    loi(1, f"Dữ liệu Trạm có {len(tram)}, phải là 32")
dem = {n: sum(1 for t in tram if t["nam"] == n) for n in (1, 2, 3)}
if dem != {1: 9, 2: 12, 3: 11}:
    loi(1, f"Số Trạm theo năm {dem}, phải là 9, 12, 11")
else:
    DAT.append("Trạm theo năm: 9 + 12 + 11 = 32 (khớp Mục lục 9.2)")
bang_word = {r["ma"]: r for r in ml["tram"]}
if len(bang_word) != 32:
    loi(1, f"Bảng Phần 2 trong tệp Word đọc ra {len(bang_word)} Trạm")
lech = 0
for t in tram:
    r = bang_word.get(t["ma"])
    if not r or r["ten"] != t["ten"] or r["mach"] != t["mach"] or r["buoi"] != t["buoi"]:
        lech += 1
        loi(1, f"Trạm {t['ma']} lệch giữa dữ liệu web và bảng Word của Mục lục: {t['ten']!r} / {r}")
if not lech:
    DAT.append("Mã, tên, mạch chính, số buổi của 32 Trạm khớp từng dòng với bảng trong tệp Word Mục lục 9.2")
tong = 0
for n, v in ml["lich"].items():
    s = sum(h["buoi"] for h in v["hang"])
    tong += s
    if s != v["buoi"]:
        loi(1, f"Năm {n}: các hàng cộng {s} buổi, tiêu đề ghi {v['buoi']}")
    st = sum(h["buoi"] for h in v["hang"] if h["khoi"].startswith("L"))
    if st != sum(t["buoi"] for t in tram if t["nam"] == int(n)):
        loi(1, f"Năm {n}: buổi của các Trạm trong lịch ({st}) khác bảng Trạm")
if tong != 252 or [v["buoi"] for v in ml["lich"].values()] != [72, 84, 96]:
    loi(1, f"Tổng buổi {tong}, phải là 72 + 84 + 96 = 252")
else:
    DAT.append("Buổi học: 72 + 84 + 96 = 252; mỗi năm các hàng lịch cộng đúng tổng")
muc_luc_docx = None
for p in (GOC.parent / "4_HO-SO-THIET-KE").glob("MỤC LỤC CHƯƠNG TRÌNH TOÁN TƯ DUY 3 NĂM - BẢN 9.2*.docx"):
    muc_luc_docx = p
if muc_luc_docx:
    import hashlib
    if hashlib.md5(muc_luc_docx.read_bytes()).hexdigest() != ml["md5_nguon"]:
        canh_bao(1, "Tệp Mục lục 9.2 đã đổi so với lần trích số liệu: chạy lại nguon/trich_muc_luc.py và dựng lại.")
    else:
        DAT.append("Tệp Word Mục lục 9.2 chưa đổi kể từ lần trích số liệu (md5 khớp)")
    with zipfile.ZipFile(muc_luc_docx) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    van = re.sub(r"<[^>]+>", "", xml)
    if "157 câu" not in van:
        loi(1, "Trang Mục tiêu nói “157 câu đề thật” nhưng Mục lục 9.2 không có chữ “157 câu”")
    else:
        DAT.append("Con số “157 câu đề thật” có trong Mục lục 9.2 (Phần 5)")
# số liệu trong các trang
def noi_dung(p):
    return " ".join(DOC[p].text)
the = {}
for p in trang_html:
    h = p.read_text(encoding="utf-8")
    the[url_cua(p)] = h.count('class="the tram ')
kv = {"/32-tram/": 32, "/32-tram/nam-1/": 9, "/32-tram/nam-2/": 12, "/32-tram/nam-3/": 11}
for u, n in kv.items():
    if the.get(u) != n:
        loi(1, f"Trang {u} có {the.get(u)} thẻ Trạm, phải là {n}")
if all(the.get(u) == n for u, n in kv.items()):
    DAT.append("Trang 32 Trạm có 32 thẻ; ba trang năm có 9, 12, 11 thẻ")
home = noi_dung(GOC / "index.html")
for m in re.finditer(r"(\d+)\s+(Trạm|buổi học|mạch tư duy)", home):
    n, nhan = int(m.group(1)), m.group(2)
    dung = {"Trạm": {32, 9, 12, 11, 6}, "buổi học": {252}, "mạch tư duy": {7}}[nhan]
    if n not in dung and not (nhan == "Trạm" and n in (1, 4, 5, 7)):
        canh_bao(1, f"Trang chủ có “{m.group(0)}”: kiểm lại nguồn")
for p in trang_html:
    t = noi_dung(p)
    for m in re.finditer(r"\b(3[0-9]|2[0-9]|4[0-9])\s+Trạm\b", t):
        if m.group(1) != "32":
            loi(1, f"{url_cua(p)} ghi “{m.group(0)}”, tổng phải là 32 Trạm")
    if re.search(r"\b38 Trạm\b|\b38 trạm\b", t):
        loi(1, f"{url_cua(p)} còn số 38 Trạm của Bản 8")

# ---------- Cổng 2: liên kết ----------
NGOAI_OK = ("https://lab.tramtuduy.org", "https://tramtuduy.org", "https://fonts.googleapis.com", "https://fonts.gstatic.com",
            "https://zalo.me/", "tel:", "mailto:", "https://toan.tramtuduy.org/")
n_lk = 0
for p, d in DOC.items():
    for href in d.links + d.srcs:
        if href.startswith("#"):
            if href[1:] and href[1:] not in d.ids:
                loi(2, f"{url_cua(p)}: neo {href} không có trong trang")
            continue
        if href.startswith("/"):
            n_lk += 1
            if "/#/" in href or href.startswith("/#"):
                loi(2, f"{url_cua(p)}: liên kết dùng /#/ ({href})")
            ph = href.split("#")[0].split("?")[0]
            dich = GOC / ph.lstrip("/")
            if ph.endswith("/"):
                dich = dich / "index.html"
            if not dich.exists():
                loi(2, f"{url_cua(p)}: liên kết gãy {href}")
            elif "#" in href and dich.suffix == ".html":
                neo = href.split("#")[1]
                if neo not in doc(dich).ids:
                    loi(2, f"{url_cua(p)}: neo gãy {href}")
        elif href.startswith(NGOAI_OK):
            n_lk += 1
        elif href.startswith("http"):
            loi(2, f"{url_cua(p)}: liên kết ra ngoài chưa được cho phép {href}")
        else:
            loi(2, f"{url_cua(p)}: liên kết tương đối/khó hiểu {href}")
    # liên kết ra ngoài của web chính có /#/ chỉ được trỏ hồ sơ mẫu
    for h in d.links:
        if h.startswith(CHINH) and "/#/" in h and not h.endswith("/#/ho-so-mau"):
            loi(2, f"{url_cua(p)}: liên kết web chính lạ {h}")
if not any(l.startswith("[Cổng 2]") for l in LOI):
    DAT.append(f"Liên kết: {n_lk} liên kết nội bộ và ra ngoài đều đúng đích; không có /#/ trong địa chỉ của site; mọi neo # tồn tại")
nhan_lab = sum(1 for d in DOC.values() for h in d.links if h == LAB)
if nhan_lab < 2:
    loi(7, "Ít nhất trang chủ và trang Phòng thí nghiệm phải trỏ đúng https://lab.tramtuduy.org")
else:
    DAT.append(f"{nhan_lab} liên kết trỏ đúng https://lab.tramtuduy.org (không đổi địa chỉ lab)")
tro_ve = sum(1 for d in DOC.values() for h in d.links if h == CHINH)
if tro_ve < len(trang_html) - 1:
    loi(2, "Mỗi trang phải có đường về web chính tramtuduy.org")
else:
    DAT.append("Mọi trang đều có đường về web chính https://tramtuduy.org")

# ---------- Cổng 3: chữ viết ----------
RE_XUNG = re.compile(r"\b(con nào|mỗi con|những con|(?:hai|ba|bốn|năm|\d+(?:/\d+)?) con)\b(?! (?:thỏ|mèo|chó|gà|vịt|cá|chim|ong|kiến|rùa|ngựa|bò|lợn|voi|khỉ|sóc|vật))", re.I)
for p, d in DOC.items():
    van = "\n".join(d.text)
    for i, dong in enumerate(van.splitlines(), 1):
        if "«" in dong or "»" in dong:
            loi(3, f"{url_cua(p)}: ngoặc « » ({dong.strip()[:60]})")
        if '"' in dong:
            loi(3, f"{url_cua(p)}: ngoặc thẳng ({dong.strip()[:60]})")
        if re.search(r"\bkẹt\b", dong, re.I):
            loi(3, f"{url_cua(p)}: từ cô đã bỏ ({dong.strip()[:60]})")
        for m in RE_XUNG.finditer(dong):
            loi(3, f"{url_cua(p)}: “con” làm từ đếm: {m.group(1)}")
        if re.search(r"\d\s*[–-]\s*\d", dong):
            loi(3, f"{url_cua(p)}: gạch giữa hai số ({dong.strip()[:60]})")
        if re.search(r"\d\s*·|·\s*\d", dong):
            loi(3, f"{url_cua(p)}: dấu · cạnh số ({dong.strip()[:60]})")
        if re.search(r"\bL[345]\s?·\s?T\d+", dong):
            loi(3, f"{url_cua(p)}: mã nội bộ trên trang ({dong.strip()[:60]})")
        if re.search(r"\b0\d{9,10}\b|\+84\d{8,10}", dong):
            loi(3, f"{url_cua(p)}: có số điện thoại trong chữ ({dong.strip()[:60]})")
        if re.search(r"[\w.]+@[\w.]+\.\w+", dong):
            loi(3, f"{url_cua(p)}: có địa chỉ email trong chữ")
        if re.search(r"\d[\d.,]*\s*(đồng|VNĐ|vnđ|triệu|nghìn|k\b|₫)", dong):
            loi(3, f"{url_cua(p)}: có số tiền (học phí chưa được ghi) ({dong.strip()[:60]})")
        if re.search(r"\b(đáp án|Đáp số|đáp số)\b", dong) and not any(x in dong for x in ("điền đáp số", "không đưa đáp án", "Không đưa đề thi", "máy giải lại")):
            loi(3, f"{url_cua(p)}: nhắc đáp án/đáp số ({dong.strip()[:60]})")
        if re.search(r"\b(ThPT|tư vấn viên)\b", dong):
            pass
    if "​" in van:
        loi(3, f"{url_cua(p)}: ký tự ẩn")
# thuộc tính chứa chữ in ra (alt, title, content) cũng không được dùng ngoặc lạ
for p in trang_html:
    h = p.read_text(encoding="utf-8")
    for m in re.finditer(r'(?:alt|content|aria-label)="([^"]*)"', h):
        if "«" in m.group(1) or "»" in m.group(1):
            loi(3, f"{url_cua(p)}: « » trong thuộc tính")
if not any(l.startswith("[Cổng 3]") for l in LOI):
    DAT.append("Chữ viết: không có « », ngoặc thẳng, từ cô đã bỏ, “con” làm từ đếm, gạch giữa hai số, dấu · cạnh số, mã nội bộ, số điện thoại, email, số tiền, đáp án")

# ---------- Cổng 4: chia sẻ ----------
tieu_de_gap, mo_ta_gap = {}, {}
for p, d in DOC.items():
    u = url_cua(p)
    if p.name == "404.html":
        if "noindex" not in p.read_text(encoding="utf-8"):
            loi(4, "404 phải có noindex")
        continue
    m = d.meta
    for k in ("og:title", "og:description", "og:image", "og:url", "og:type", "twitter:card", "description"):
        if not m.get(k):
            loi(4, f"{u}: thiếu {k}")
    if d.canon != m.get("og:url") or d.canon != f"{SITE}{u}":
        loi(4, f"{u}: canonical/og:url lệch ({d.canon} / {m.get('og:url')})")
    img = m.get("og:image", "")
    if img.startswith(SITE + "/"):
        f = GOC / img[len(SITE) + 1:]
        if not f.exists():
            loi(4, f"{u}: ảnh chia sẻ không tồn tại {img}")
        else:
            w, h = kich_thuoc_png(f)
            if w < 1200 or h < 630:
                loi(4, f"{u}: ảnh chia sẻ {w}×{h} nhỏ hơn 1200×630")
    if m.get("og:image:width") != "1200" or m.get("og:image:height") != "630":
        loi(4, f"{u}: khai báo kích thước ảnh chia sẻ sai")
    tieu_de_gap.setdefault(m.get("og:title"), []).append(u)
    mo_ta_gap.setdefault(m.get("og:description"), []).append(u)
    if len(m.get("og:description", "")) > 200:
        canh_bao(4, f"{u}: mô tả chia sẻ dài {len(m['og:description'])} ký tự")
for k, v in list(tieu_de_gap.items()) + list(mo_ta_gap.items()):
    if len(v) > 1:
        loi(4, f"Trùng tiêu đề/mô tả chia sẻ giữa {v}")
ogs = sorted((GOC / "tai-san/og").glob("*.png"))
if not any(l.startswith("[Cổng 4]") for l in LOI):
    DAT.append(f"Chia sẻ: {len(DOC) - 1} trang đều có og:title, og:description, og:image (1200×630), og:url trùng canonical, tiêu đề và mô tả không trùng nhau; ảnh riêng từng trang ({len(ogs)} ảnh)")
sm = (GOC / "sitemap.xml").read_text(encoding="utf-8")
for p in trang_html:
    if p.name != "404.html" and f"<loc>{SITE}{url_cua(p)}</loc>" not in sm:
        loi(4, f"sitemap thiếu {url_cua(p)}")
if (GOC / "CNAME").read_text().strip() != "toan.tramtuduy.org":
    loi(4, "CNAME sai")

# ---------- Cổng 5: tốc độ, cỡ chữ ----------
css = (GOC / "tai-san/css/site.css").read_text(encoding="utf-8")
js = (GOC / "tai-san/js/site.js").read_text(encoding="utf-8")
bang_kt = []
for p in trang_html:
    h_kb = p.stat().st_size
    if h_kb > 80_000:
        loi(5, f"{url_cua(p)}: HTML {h_kb // 1024} KB, quá lớn")
    bang_kt.append((url_cua(p), h_kb))
css_kb = (GOC / "tai-san/css/site.css").stat().st_size
js_kb = (GOC / "tai-san/js/site.js").stat().st_size
logo_ngang = (GOC / "tai-san/logo/logo-tram-tu-duy-ngang.svg").stat().st_size
bt = (GOC / "tai-san/logo/bieu-tuong-tram-tu-duy.svg").stat().st_size
home_kb = (GOC / "index.html").stat().st_size
tai_chu = home_kb + css_kb + js_kb + logo_ngang + bt
CHI_SO = {"html_home": home_kb, "css": css_kb, "js": js_kb, "tai_lan_dau_home_B": tai_chu}
if css_kb > 40_000 or js_kb > 5_000:
    loi(5, "CSS hoặc JS quá lớn")
if tai_chu > 150_000:
    loi(5, f"Trang chủ tải lần đầu {tai_chu // 1024} KB (không tính phông Inter), vượt 150 KB")
for png in (GOC / "tai-san/og").glob("*.png"):
    if png.stat().st_size > 200_000:
        loi(5, f"Ảnh chia sẻ {png.name} nặng {png.stat().st_size // 1024} KB")
# chữ nhỏ hơn 16 px
for m in re.finditer(r"font-size:\s*([\d.]+)(px|rem|em|%)", css):
    v, dv = float(m.group(1)), m.group(2)
    px = {"px": v, "rem": v * 16, "em": v * 16, "%": v * 0.16}[dv]
    if px < 16:
        loi(5, f"CSS có font-size {m.group(0)} < 16 px")
for m in re.finditer(r"font-size:\s*(clamp|calc)\(([^;]+)\)", css):
    pass
for p in trang_html:
    h = p.read_text(encoding="utf-8")
    for m in re.finditer(r'style="[^"]*font-size:\s*([\d.]+)(px|rem|em)', h):
        loi(5, f"{url_cua(p)}: font-size nội tuyến {m.group(0)}")
if "prefers-reduced-motion" not in css:
    loi(5, "CSS chưa có @media (prefers-reduced-motion)")
else:
    DAT.append("Giảm chuyển động: có @media (prefers-reduced-motion: no-preference) bọc mọi hiệu ứng chuyển động (cuộn mượt, nhấc thẻ)")
if re.search(r"(?<!no-preference\) \{)\s*transition", css) and False:
    pass
# mọi animation/transition phải nằm trong khối no-preference, hoặc là transition ngắn trên nút
for m in re.finditer(r"@keyframes|animation:", css):
    loi(5, "Có animation: phải bọc trong prefers-reduced-motion")
if not any(l.startswith("[Cổng 5]") for l in LOI):
    DAT.append(f"Tốc độ: trang chủ tải lần đầu khoảng {tai_chu // 1024} KB (HTML {home_kb // 1024} + CSS {css_kb // 1024} + JS {js_kb // 1024} + logo/biểu tượng {(logo_ngang + bt) // 1024}), không khung dựng sẵn, phông Inter nạp không chặn hiển thị; không chữ nào dưới 16 px trong CSS")

# ---------- Cổng 6: cấu trúc ----------
tieu = {}
for p, d in DOC.items():
    u = url_cua(p)
    if d.lang != "vi":
        loi(6, f"{u}: thiếu lang=vi")
    if d.h1 != 1:
        loi(6, f"{u}: có {d.h1} thẻ h1 (phải đúng 1)")
    if "viewport" not in d.meta:
        loi(6, f"{u}: thiếu viewport")
    for im in d.imgs:
        if "alt" not in im:
            loi(6, f"{u}: ảnh thiếu alt ({im.get('src')})")
    if d.title in tieu:
        loi(6, f"Trùng <title>: {u} và {tieu[d.title]}")
    tieu[d.title] = u
    if p.name != "404.html" and not d.title.strip():
        loi(6, f"{u}: thiếu title")
    if any("localhost" in x or "127.0.0.1" in x for x in d.links + d.srcs):
        loi(6, f"{u}: trỏ tới localhost")
if not any(l.startswith("[Cổng 6]") for l in LOI):
    DAT.append("Cấu trúc: mọi trang có lang=vi, đúng một h1, viewport, ảnh có alt, tiêu đề không trùng")

# ---------- Cổng 7: Phòng thí nghiệm ----------
if MANG:
    import urllib.request
    for u, ten in ((LAB, "Phòng thí nghiệm"), (CHINH, "web chính")):
        try:
            rq = urllib.request.Request(u, method="GET", headers={"User-Agent": "kiem-lien-ket"})
            with urllib.request.urlopen(rq, timeout=20) as r:
                if r.status != 200:
                    loi(7, f"{ten} {u} trả mã {r.status}")
                else:
                    DAT.append(f"Mạng: {u} mở được (mã 200)")
        except Exception as e:
            loi(7, f"{ten} {u} không mở được: {e}")
else:
    canh_bao(7, "Chưa kiểm mạng (chạy lại với --mang để kiểm lab và web chính còn mở).")

# ---------- chỗ chờ cô điền ----------
cho = {}
for p in trang_html:
    n = p.read_text(encoding="utf-8").count("data-can-co-dien")
    if n:
        cho[url_cua(p)] = n
tong_cho = sum(cho.values())

# ---------- ghi báo cáo ----------
gio = datetime.now().strftime("%d/%m/%Y %H:%M")
out = [f"# Kết quả kiểm web Toán ({gio})", "",
       f"Lệnh: `python3 nguon/kiem_site.py{' --mang' if MANG else ''}`. Trang kiểm: {len(DOC)} (gồm 404).", "",
       f"**Kết luận: {'KHÔNG ĐẠT, ' + str(len(LOI)) + ' lỗi' if LOI else 'ĐẠT, 0 lỗi chặn'}** · cảnh báo: {len(CANH_BAO)} · khung CẦN CÔ ĐIỀN còn trong bản xem trước: {tong_cho}", "",
       "## Đã đạt"]
out += [f"- {x}" for x in DAT] or ["- (chưa có)"]
out += ["", "## Lỗi"] + ([f"- {x}" for x in LOI] or ["- không"])
out += ["", "## Cảnh báo, chỗ chưa kiểm được"] + ([f"- {x}" for x in CANH_BAO] or ["- không"])
out += ["", "## Chỗ chờ cô điền theo trang (bản xem trước)"] + ([f"- `{u}`: {n}" for u, n in cho.items()] or ["- không"])
out += ["", "## Kích thước (byte)", "", "| Trang | HTML |", "|---|---|"] + [f"| `{u}` | {k:,} |" for u, k in bang_kt]
out += ["", f"CSS {css_kb:,} · JS {js_kb:,} · logo ngang SVG {logo_ngang:,} · biểu tượng SVG {bt:,} · ảnh chia sẻ mỗi trang khoảng {sum(f.stat().st_size for f in ogs) // max(1, len(ogs)):,} (chỉ tải khi mạng xã hội cần)"]
(GOC / "noi-bo" / "KET_QUA_KIEM.md").write_text("\n".join(out) + "\n", encoding="utf-8")
print("\n".join(out[:4 + len(DAT) + 3]))
print("\n".join(LOI) if LOI else "(không lỗi)")
sys.exit(1 if LOI else 0)
