#!/usr/bin/env python3
"""Dựng site tĩnh toan.tramtuduy.org từ dữ liệu Mục lục 9.2.

Dùng (chạy ở thư mục 6_WEB-TOAN):
    python3 nguon/dung_site.py            # bản xem trước: chỗ chưa có nội dung hiện khung CẦN CÔ ĐIỀN
    python3 nguon/dung_site.py --dang     # bản đăng: từ chối nếu còn chỗ bắt buộc chưa điền,
                                          # còn chỗ tùy chọn chưa có thì ẩn đi

Không cần thư viện ngoài trừ Pillow (chỉ để vẽ ảnh chia sẻ). Không gọi mạng, không ghi ra ngoài 6_WEB-TOAN.
"""
import json, sys, html, re
from pathlib import Path

GOC = Path(__file__).resolve().parents[1]
ND = GOC / "nguon"
SITE = "https://toan.tramtuduy.org"
LAB = "https://lab.tramtuduy.org"
CHINH = "https://tramtuduy.org"
NGAY = "2026-11-19"
DANG = "--dang" in sys.argv

TRAM = json.loads((ND / "du-lieu" / "tram.json").read_text(encoding="utf-8"))
MUC_LUC = json.loads((ND / "du-lieu" / "muc_luc_92.json").read_text(encoding="utf-8"))
CH = json.loads((ND / "cau_hinh.json").read_text(encoding="utf-8"))
T = TRAM["tram"]

MACH_THU_TU = ["LG", "SO", "SH", "QL", "DT", "MH", "HH"]
MACH_TEN = TRAM["mach"]
# Mức của từng mạch qua ba năm: lấy từ Khung 7.3, mục 4
MACH_MO_TA = {
    "LG": ["thứ tự, bắc cầu, bảng loại trừ trên đồ vật thật",
           "bảng logic nhiều manh mối; ai nói thật, ai nói dối; lớn nhất, bé nhất",
           "logic trong mọi bài lời văn; nghĩ đến trường hợp xui nhất"],
    "SO": ["giá trị theo hàng, cả và phần, nhóm bằng nhau, gấp mấy lần",
           "tính chất phép tính, tính nhanh, phân số",
           "phân số nâng cao, số thập phân"],
    "SH": ["chữ số chẵn, lẻ; chu kỳ và số dư trong lịch",
           "chia hết, ước, bội, số nguyên tố, chữ số tận cùng",
           "ước chung, bội chung, số chính phương, số dư của số lớn"],
    "QL": ["dãy hình lặp lại và lớn dần; dấu “=” là cân bằng",
           "dãy cách đều, quy luật dãy số và dãy hình, hình thứ n bằng lời",
           "quy tắc mới, máy vào – ra, khái quát bằng chữ"],
    "DT": ["liệt kê có hệ thống, cây, bảng",
           "quy tắc cộng và nhân, đếm hình",
           "sơ đồ Venn, bao hàm – loại trừ, nguyên lý Dirichlet, đếm phần bù, số liệu"],
    "MH": ["sơ đồ đoạn thẳng: một phần của cả, hơn kém, đi ngược",
           "tổng – hiệu, giả thiết tạm, bài toán phân số",
           "tỉ số, phần trăm, chuyển động, công việc chung"],
    "HH": ["lưới ô vuông: chu vi, diện tích, cắt ghép",
           "góc, hình ghép phẳng, khối lập phương, khai triển",
           "tam giác, hình thang, hình tròn, thể tích, sơn mặt khối"],
}
NAM = {
    1: dict(ten="Xây nền", tuoi="8 đến 9 tuổi", lop=3,
            loi="Con học nhìn, học nghĩ, học nói chữ “vì”.", cay="Rễ bám sâu trước."),
    2: dict(ten="Dựng khung", tuoi="9 đến 10 tuổi", lop=4,
            loi="Con nhìn thấy cấu trúc bên trong mỗi bài toán.", cay="Thân dựng lên vững."),
    3: dict(ten="Vươn cao", tuoi="10 đến 11 tuổi", lop=5,
            loi="Con tự tin bắt đầu cả với bài toán lạ.", cay="Trí tuệ nở ra."),
}

# ---------- tính số liệu từ dữ liệu (không gõ tay) ----------
N_TRAM = len(T)
N_BUOI = sum(int(v["buoi"]) for v in MUC_LUC["lich"].values())
N_MACH = len(MACH_THU_TU)
BUOI_NAM = {int(k): v for k, v in MUC_LUC["lich"].items()}
TRAM_NAM = {n: [t for t in T if t["nam"] == n] for n in (1, 2, 3)}


# ---------- tiện ích ----------
def esc(s):
    return html.escape(str(s), quote=True)


def ten_dep(s):
    t = s.lower()
    t = t[0].upper() + t[1:]
    for a, b in (("venn", "Venn"), ("dirichlet", "Dirichlet")):
        t = t.replace(a, b)
    return t


def tuoi_dep(s):
    return s.replace(" – ", " đến ")


def so_tram(t):
    return int(t["ma"].split("T")[1])


CHO_THIEU = []   # (trang, khóa, gợi ý, bắt buộc)
TRANG_HIEN_TAI = [""]


def cho(khoa, goi_y, bat_buoc=False, nho=False):
    """Khung chờ cô điền. Bản đăng: chỗ tùy chọn được ẩn, chỗ bắt buộc làm dừng máy."""
    CHO_THIEU.append((TRANG_HIEN_TAI[0], khoa, goi_y, bat_buoc))
    if DANG and not bat_buoc:
        return ""
    cl = "cho cho--nho" if nho else "cho"
    nhan = '<b class="cho__nhan">CẦN CÔ ĐIỀN</b>'
    if nho:
        return f'<span class="{cl}" data-can-co-dien="{esc(khoa)}">{nhan}{esc(goi_y)}</span>'
    return f'<div class="{cl}" data-can-co-dien="{esc(khoa)}"><p>{nhan}</p><p>{esc(goi_y)}</p></div>'


def gia_tri(khoa, goi_y, bat_buoc=False, nho=True, tu=None):
    v = (tu if tu is not None else CH).get(khoa)
    if v:
        return esc(v)
    return cho(khoa, goi_y, bat_buoc, nho)


# ---------- ảnh chia sẻ ----------
def ve_og(ten_tep, tieu_de, phu):
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1200, 630
    KEM, BAC_HA, TIM, DAT, CHU_PHU = (255, 249, 240), (234, 247, 241), (70, 54, 101), (122, 78, 50), (74, 68, 88)
    anh = Image.new("RGB", (W, H), KEM)
    d = ImageDraw.Draw(anh)
    d.ellipse((730, 120, 1330, 720), fill=BAC_HA)
    from PIL import ImageChops
    goc_ic = Image.open(GOC / "tai-san/logo/bieu-tuong-512.png").convert("RGBA").resize((400, 400), Image.LANCZOS)
    tren_trang = Image.new("RGBA", goc_ic.size, (255, 255, 255, 255))
    tren_trang.alpha_composite(goc_ic)
    ic = tren_trang.convert("RGB")
    # nền trắng của biểu tượng thành trong suốt (chỉ để vẽ ảnh chia sẻ, không sửa tệp gốc)
    mau = ic.split()
    cmin = ImageChops.darker(ImageChops.darker(mau[0], mau[1]), mau[2])
    ic = ic.convert("RGBA")
    ic.putalpha(cmin.point(lambda v: max(0, min(255, (250 - v) * 16))))
    anh.paste(ic, (790, 140), ic)
    lg = Image.open(GOC / "tai-san/logo/logo-tram-tu-duy-ngang.png").convert("RGBA")
    w = 330
    lg = lg.resize((w, int(lg.height * w / lg.width)), Image.LANCZOS)
    anh.paste(lg, (64, 52), lg)
    phong_ten = Path(PHONG) / "Inter-Ten.ttf"
    phong_kh = Path(PHONG) / "Inter-KhauHieu.ttf"
    f1 = ImageFont.truetype(str(phong_ten), 66)
    f2 = ImageFont.truetype(str(phong_kh), 32)

    def ngat(chu, f, rong):
        dong, cur = [], ""
        for tu in chu.split():
            thu = (cur + " " + tu).strip()
            if f.getlength(thu) <= rong:
                cur = thu
            else:
                dong.append(cur)
                cur = tu
        if cur:
            dong.append(cur)
        return dong

    y = 200
    for l in ngat(tieu_de, f1, 660)[:3]:
        d.text((64, y), l, font=f1, fill=TIM)
        y += 82
    y += 14
    for l in ngat(phu, f2, 640)[:3]:
        d.text((64, y), l, font=f2, fill=CHU_PHU)
        y += 44
    d.rectangle((0, H - 22, W, H), fill=TIM)
    d.rectangle((0, H - 22, 260, H), fill=DAT)
    d.text((64, H - 64), "toan.tramtuduy.org", font=ImageFont.truetype(str(phong_kh), 26), fill=DAT)
    dich = GOC / "tai-san/og" / (ten_tep + ".png")
    dich.parent.mkdir(parents=True, exist_ok=True)
    anh.quantize(colors=96, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).save(dich, optimize=True)


PHONG = "/Users/duongthithuytrang/Desktop/DỰ ÁN TÀI LIỆU LUYỆN THI TRẦN ĐẠI NGHĨA/THUONG HIEU/PHONG CHU/Inter"

# ---------- khung trang ----------
NAV = [("chuong-trinh", "Chương trình", True), ("32-tram", "32 Trạm", True), ("lo-trinh", "Lộ trình", True),
       ("muc-tieu", "Mục tiêu", True), ("tu-lop-hoc", "Từ lớp học", False), ("phong-thi-nghiem", "Phòng thí nghiệm", True),
       ("cau-hoi", "Hỏi đáp", True), ("hanh-trinh", "Hành trình của con", False), ("co-trang", "Giới thiệu cô", False)]

TRANG = []  # (slug, tieu_de, mo_ta, priority)


def menu(hien):
    li = []
    for slug, ten, pc in NAV:
        cur = ' aria-current="page"' if hien == slug else ""
        cl = "" if pc else ' class="menu__khong-pc"'
        li.append(f'<li{cl}><a href="/{slug}/"{cur}>{ten}</a></li>')
    li.append(f'<li class="menu__phu"><a href="{CHINH}">Về web Trạm Tư Duy</a></li>')
    li.append('<li><a class="btn btn--chinh" href="/dang-ky/">Đăng ký tư vấn</a></li>')
    return "\n".join(li)


def khung(slug, tieu_de, mo_ta, body, hien="", og_tieu_de=None, og_phu=None, json_ld="", khong_og=False):
    url = f"{SITE}/{slug}/" if slug else f"{SITE}/"
    ten_og = slug.strip("/").replace("/", "-") or "trang-chu"
    if not khong_og:
        ve_og(ten_og, og_tieu_de or tieu_de, og_phu or mo_ta)
    anh = f"{SITE}/tai-san/og/{ten_og}.png"
    tt = f"{tieu_de} · Toán tư duy Trạm Tư Duy" if slug else "Toán tư duy ba năm · Trạm Tư Duy"
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(tt)}</title>
<meta name="description" content="{esc(mo_ta)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Trạm Tư Duy · Toán tư duy">
<meta property="og:locale" content="vi_VN">
<meta property="og:title" content="{esc(tt)}">
<meta property="og:description" content="{esc(mo_ta)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{anh}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(og_tieu_de or tieu_de)}: Toán tư duy Trạm Tư Duy">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(tt)}">
<meta name="twitter:description" content="{esc(mo_ta)}">
<meta name="twitter:image" content="{anh}">
<meta name="theme-color" content="#463665">
<link rel="icon" type="image/png" sizes="32x32" href="/tai-san/logo/bieu-tuong-32.png">
<link rel="apple-touch-icon" href="/tai-san/logo/bieu-tuong-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;display=swap" media="print" onload="this.media='all'">
<noscript><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&amp;display=swap"></noscript>
<link rel="stylesheet" href="/tai-san/css/site.css">
<script>document.documentElement.classList.add("js")</script>
{json_ld}</head>
<body>
<a class="bo-qua" href="#noi-dung">Bỏ qua, đến nội dung</a>
<header class="dau">
<div class="wrap dau__hang">
<a class="dau__logo" href="/" aria-label="Toán tư duy Trạm Tư Duy, về trang chủ"><img src="/tai-san/logo/logo-tram-tu-duy-ngang.svg" width="114" height="44" alt="Trạm Tư Duy, Xây nền trí tuệ"></a>
<button class="nut-menu" id="nut-menu" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
<nav class="menu" id="menu" aria-label="Menu chính">
<ul>
{menu(hien)}
</ul>
</nav>
</div>
</header>
<main id="noi-dung">
{body}
</main>
<footer class="chan">
<div class="wrap">
<div class="chan__luoi">
<div>
<a class="chan__logo" href="/" aria-label="Về trang chủ"><img src="/tai-san/logo/logo-tram-tu-duy-doc.svg" width="126" height="163" alt="Trạm Tư Duy, Xây nền trí tuệ"></a>
<p style="margin-top:14px">Chương trình Toán tư duy ba năm cho các con từ 8 đến 11 tuổi.</p>
</div>
<div>
<h2>Trong trang này</h2>
<ul>
<li><a href="/chuong-trinh/">Chương trình ba năm</a></li>
<li><a href="/32-tram/">32 Trạm theo bảy mạch</a></li>
<li><a href="/lo-trinh/">Lộ trình 8 đến 11 tuổi</a></li>
<li><a href="/muc-tieu/">Mục tiêu và kỳ thi</a></li>
<li><a href="/tu-lop-hoc/">Từ lớp học</a></li>
<li><a href="/cau-hoi/">Câu hỏi thường gặp</a></li>
</ul>
</div>
<div>
<h2>Đi tiếp</h2>
<ul>
<li><a href="/dang-ky/">Đăng ký và liên hệ</a></li>
<li><a href="/co-trang/">Giới thiệu cô Trang</a></li>
<li><a href="/phong-thi-nghiem/">Phòng thí nghiệm</a></li>
<li><a href="/hanh-trinh/">Hành trình của con</a></li>
<li><a href="{CHINH}">Về web Trạm Tư Duy</a></li>
</ul>
</div>
</div>
<p class="chan__nho">Toán tư duy là một phần của Trạm Tư Duy. Kết quả mỗi kỳ thi còn tùy sức học và sự rèn luyện của con.</p>
</div>
</footer>
<script src="/tai-san/js/site.js" defer></script>
</body>
</html>
"""


def viet(slug, tieu_de, mo_ta, body, **kw):
    TRANG_HIEN_TAI[0] = slug or "trang-chu"
    noi = khung(slug, tieu_de, mo_ta, body(), **kw) if callable(body) else khung(slug, tieu_de, mo_ta, body, **kw)
    dich = GOC / slug / "index.html" if slug else GOC / "index.html"
    dich.parent.mkdir(parents=True, exist_ok=True)
    dich.write_text(noi, encoding="utf-8")
    TRANG.append((slug, tieu_de, mo_ta))


def dau_trang(vet, h1, loi):
    return f"""<section class="dau-trang"><div class="wrap">
<p class="vet-banh"><a href="/">Trang chủ</a> › {esc(vet)}</p>
<h1>{h1}</h1>
<p>{loi}</p>
</div></section>"""


# ---------- thẻ Trạm ----------
def the_tram(t, hien_nam=True):
    so = so_tram(t)
    nam = t["nam"]
    phu = ", ".join(MACH_TEN[p] for p in t.get("phu", []))
    phu = f"<span>Mạch phụ: {esc(phu)}</span>" if phu else ""
    return f"""<article class="the tram c-{t['mach']}" id="nam{nam}-tram{so}">
<p class="tram__dau"><b>Trạm {so}</b><span>Năm {nam}, {tuoi_dep(t['tuoi'])}</span></p>
<h3>{esc(ten_dep(t['ten']))}</h3>
<p class="tram__hoi">{esc(t['hoi'])}</p>
<p class="tram__hua">{esc(t['hua'])}</p>
<div class="tram__chan"><i class="c-{t['mach']}">{esc(MACH_TEN[t['mach']])}</i>{phu}<span>{t['buoi']} buổi</span></div>
</article>"""


def chip_mach(hien=None, lien_ket=True):
    out = []
    for m in MACH_THU_TU:
        n = sum(1 for t in T if t["mach"] == m)
        tx = f"{esc(MACH_TEN[m])} ({n})"
        if lien_ket:
            out.append(f'<li><a class="chip c-{m}" href="/32-tram/#mach-{m}">{tx}</a></li>')
        else:
            out.append(f'<li><span class="chip c-{m}">{tx}</span></li>')
    return '<ul class="mach-hang">' + "".join(out) + "</ul>"


# ================= TRANG CHỦ =================
def trang_chu():
    ba_nam = ""
    for n in (1, 2, 3):
        v = NAM[n]
        b = BUOI_NAM[n]
        ba_nam += f"""<article class="the nam nam--{n}">
<span class="nhan">Năm {n}</span>
<h3>{v['ten']}</h3>
<p class="nam__tuoi">{v['tuoi']}, lớp {v['lop']}</p>
<p><b>{v['cay']}</b></p>
<p class="nam__loi">{v['loi']}</p>
<ul class="nam__so"><li><b>{len(TRAM_NAM[n])}</b> Trạm</li><li><b>{b['buoi']}</b> buổi</li><li><b>{b['phut']}</b> phút mỗi buổi</li></ul>
</article>"""
    mau = ""
    for ma in ("L3·T1", "L4·T9", "L5·T4"):
        t = next(x for x in T if x["ma"] == ma)
        mau += the_tram(t)
    thi = [("Khảo sát vào lớp 6 Trần Đại Nghĩa", "Bài trình bày lời giải chấm theo từng bước, đề tiếng Anh tăng dần."),
           ("SASMO", "Olympic Toán quốc tế cho học sinh tiểu học."),
           ("TIMO", "Olympic Toán quốc tế: logic, số học, hình học, tổ hợp.")]
    the_thi = "".join(f'<div class="the the--nen"><h3>{a}</h3><p>{b}</p></div>' for a, b in thi)
    vd_home = cho("vi_du_lop_trang_chu", "Hai hoặc ba ví dụ thật từ lớp: ảnh bài làm của các con (đã xin phép ba mẹ, che tên), kèm một dòng mô tả; và lời nhận xét của ba mẹ (có phép).")
    khoi_lop = ""
    if vd_home:
        khoi_lop = f'''<section class="khoi"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Từ lớp học</span><h2>Ba mẹ thấy gì ở lớp của con?</h2></div>
{vd_home}
<p style="margin-top:18px"><a class="lien-ket-mui" href="/tu-lop-hoc/">Vào trang Từ lớp học</a></p>
</div></section>'''
    return f"""
<section class="mo"><div class="wrap mo__luoi">
<div>
<span class="nhan">Chương trình Toán tư duy ba năm, từ 8 đến 11 tuổi</span>
<h1>Biết nghĩ. Biết hỏi. <span>Biết trình bày.</span></h1>
<p class="mo__loi">Ba năm, {N_TRAM} Trạm. Mỗi Trạm là một câu hỏi lớn, để con hiểu tận gốc rồi mới đi tiếp.</p>
<div class="hang-nut"><a class="btn btn--chinh" href="/32-tram/">Xem {N_TRAM} Trạm</a><a class="btn btn--phu" href="/dang-ky/">Đăng ký tư vấn</a></div>
<ul class="so-chip">
<li><b>3</b><span>năm học</span></li>
<li><b>{N_TRAM}</b><span>Trạm</span></li>
<li><b>{N_MACH}</b><span>mạch tư duy</span></li>
<li><b>{N_BUOI}</b><span>buổi học</span></li>
</ul>
</div>
<div class="mo__cay"><img src="/tai-san/logo/bieu-tuong-tram-tu-duy.svg" width="240" height="260" alt="Biểu tượng Trạm Tư Duy: quyển vở mở, rễ, thân cây và bộ não ở tán cây"></div>
</div></section>

<section class="khoi"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Ba năm, một cái cây</span><h2>Rễ trước. Thân sau. Tán cuối cùng.</h2><p>Mỗi năm có một việc chính. Năm sau đứng trên vai năm trước, nên con không bị bỏ lại và cũng không bị đẩy đi quá nhanh.</p></div>
<div class="luoi luoi--3">{ba_nam}</div>
<p style="margin-top:18px"><a class="lien-ket-mui" href="/lo-trinh/">Xem lộ trình từng năm</a></p>
</div></section>

<section class="khoi khoi--bac-ha"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Mỗi Trạm là một câu hỏi lớn</span><h2>Con dừng lại để hiểu, không chạy theo dạng bài.</h2><p>Mỗi Trạm kéo dài từ 4 đến 7 buổi. Trạm mở bằng một câu hỏi con chưa trả lời được, và khép lại bằng một câu hứa nhỏ: sau Trạm này, con làm được điều gì.</p></div>
<div class="luoi luoi--3">{mau}</div>
<p style="margin-top:18px"><a class="lien-ket-mui" href="/32-tram/">Xem cả {N_TRAM} Trạm</a></p>
</div></section>

<section class="khoi"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Bốn bước cho mọi bài toán</span><h2>Bài dễ hay bài khó, con đi cùng một nhịp.</h2></div>
{buoc()}
<p style="margin-top:18px" class="noi-dung">Từ năm thứ hai, con còn tập trình bày lời giải thành từng bước, như bài tự luận trong kỳ khảo sát.</p>
</div></section>

<section class="khoi khoi--trang"><div class="wrap">
<div class="khoi__dau"><span class="nhan">{N_MACH} mạch tư duy</span><h2>Một mạch đi xuyên ba năm.</h2><p>Mỗi Trạm là một ý lớn của một mạch. Cùng một mạch, mức hiểu cao dần từ năm này sang năm khác.</p></div>
{chip_mach()}
</div></section>

<section class="khoi"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Ba kỳ thi đích</span><h2>Nơi con dùng điều đã hiểu.</h2><p>Chương trình không luyện mẹo cho từng kỳ thi. Chương trình dạy con hiểu sâu; kỳ thi là chỗ con thử sức.</p></div>
<div class="luoi luoi--3">{the_thi}</div>
<p style="margin-top:18px"><a class="lien-ket-mui" href="/muc-tieu/">Xem chi tiết và lời nói thật</a></p>
</div></section>

<section class="khoi khoi--bac-ha"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Một tuần học của con</span><h2>Hai buổi trên lớp, một phiếu ở nhà.</h2></div>
{mot_tuan()}
</div></section>

<section class="khoi khoi--tim"><div class="wrap lab-khoi">
<div>
<span class="nhan">Phòng thí nghiệm</span>
<h2>Kéo thử, nhìn thấy, rồi mới hiểu.</h2>
<p>Mỗi bàn thí nghiệm đi cùng một bài trong Bài học của con: con tự thay số, tự xếp, tự quan sát. Phòng thí nghiệm không hỏi tên và không lưu thông tin của con.</p>
<div class="hang-nut"><a class="btn btn--sang" href="{LAB}">Vào Phòng thí nghiệm</a><a class="btn btn--phu" style="color:#fff;border-color:#fff" href="/phong-thi-nghiem/">Tìm hiểu thêm</a></div>
</div>
<div class="lab-thung"><b>Hiện có</b>Các bàn thí nghiệm cho năm 8 đến 9 tuổi. Các năm sau được thêm dần.</div>
</div></section>

{khoi_lop}

<section class="khoi khoi--bac-ha"><div class="wrap keu">
<h2>Bắt đầu từ một câu hỏi nhỏ.</h2>
<p class="noi-dung">Ba mẹ muốn biết chương trình có hợp với con không? Cứ hỏi cô. Cô trả lời thẳng, không hứa điều không làm được.</p>
<div class="hang-nut"><a class="btn btn--chinh" href="/dang-ky/">Đăng ký tư vấn</a><a class="btn btn--phu" href="/cau-hoi/">Đọc câu hỏi thường gặp</a></div>
</div></section>
"""


def buoc():
    return """<ul class="buoc">
<li class="b-think"><b>THINK</b><span>Con biết gì? Đề hỏi gì?</span></li>
<li class="b-plan"><b>PLAN</b><span>Con sẽ làm thế nào?</span></li>
<li class="b-solve"><b>SOLVE</b><span>Con giải: vẽ hình, tính.</span></li>
<li class="b-explain"><b>EXPLAIN</b><span>Vì sao đúng? Con kiểm tra lại.</span></li>
</ul>"""


def mot_tuan():
    return """<div class="luoi luoi--4">
<div class="the"><h3>Trên lớp</h3><p>Hai buổi mỗi tuần. Mỗi buổi mở bằng 5 đến 10 phút nhớ lại bài cũ. Năm 1 và năm 2 có thêm Góc không gian 10 phút với khối, giấy, gương.</p></div>
<div class="the"><h3>Ở nhà</h3><p>Một phiếu sau mỗi buổi, phần chính khoảng 15 phút ở năm đầu; phần ★ đến ★★★ cho con muốn thử sức. Ba mẹ ghi giờ, ký tên, và hỏi con một câu “vì sao?”.</p></div>
<div class="the"><h3>Khi gặp khó khăn</h3><p>Con viết một câu hỏi vào ô “Khi gặp khó khăn”. Đầu buổi sau, cả lớp cùng gỡ từ chính câu hỏi của các con.</p></div>
<div class="the the--nen"><h3>Theo dõi tiến bộ</h3><p>Thẻ kiểm tra 30 phút ở cuối mỗi Trạm. Sau mỗi chặng 2 đến 4 Trạm có một tuần ôn tích hợp và một tuần đánh giá.</p></div>
</div>"""


# ================= CHƯƠNG TRÌNH =================
def trang_chuong_trinh():
    ba = ""
    for n in (1, 2, 3):
        v = NAM[n]
        b = BUOI_NAM[n]
        ba += f"""<article class="the nam nam--{n}">
<span class="nhan">Năm {n}</span><h3>{v['ten']}</h3>
<p class="nam__tuoi">{v['tuoi']}, lớp {v['lop']}</p>
<p><b>{v['cay']}</b> {v['loi']}</p>
<ul class="nam__so"><li><b>{len(TRAM_NAM[n])}</b> Trạm</li><li><b>{b['tuan']}</b> tuần học</li><li><b>{b['buoi']}</b> buổi</li></ul>
<p style="margin-top:12px"><a class="lien-ket-mui" href="/32-tram/nam-{n}/">Các Trạm của năm {n}</a></p>
</article>"""
    return dau_trang("Chương trình", "Chương trình Toán tư duy ba năm",
                     f"Ba năm, {N_TRAM} Trạm, {N_MACH} mạch tư duy, {N_BUOI} buổi học. Từ lớp 3 đến kỳ khảo sát vào lớp 6.") + f"""
<section class="khoi"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Ba năm</span><h2>Mỗi năm một việc chính.</h2></div>
<div class="luoi luoi--3">{ba}</div>
</div></section>

<section class="khoi khoi--bac-ha"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Một Trạm</span><h2>Một Trạm là một câu hỏi lớn.</h2></div>
<div class="hai-cot noi-dung">
<div>
<p>Con dừng lại ở mỗi Trạm từ 4 đến 7 buổi. Trong Trạm, nhiệm vụ đi qua ba lớp từ dễ đến khó. Mỗi lớp mở bằng một bài giải mẫu đầy đủ, rút dần, rồi con tự giải.</p>
<p>Mỗi buổi con làm theo một nhịp: từ vật thật, đến sơ đồ, đến ký hiệu. Con tự khám phá trước, rồi mới nghe kết luận.</p>
</div>
<div>
<p>Kiến thức không học một lần rồi bỏ. Mỗi buổi mở bằng vài phút nhớ lại bài của một tuần, một tháng và ba tháng trước. Phiếu ở nhà có câu ôn đan xen từ Trạm trước.</p>
<p>Chương trình đi song song với trường. Chỗ nào đi trước trường thì đi trước có chủ đích, thường không quá hai tháng, và có cầu nối bằng vật thật hoặc sơ đồ.</p>
</div>
</div>
</div></section>

<section class="khoi"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Bốn bước</span><h2>Mọi bài toán đi theo bốn bước.</h2></div>
{buoc()}
</div></section>

<section class="khoi khoi--trang"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Cách một Trạm ra đời</span><h2>Soạn kỹ, kiểm kỹ, dạy thử rồi mới chốt.</h2></div>
<div class="luoi luoi--3">
<div class="the"><h3>Tra nguồn uy tín</h3><p>Sách giáo khoa và chương trình chính thức; sách và tạp chí của nhà xuất bản, tổ chức toán học lớn; nghiên cứu giáo dục toán có bình duyệt.</p></div>
<div class="the"><h3>Chắt lọc từ ba bộ sách</h3><p>Archimedes (Việt Nam), Terry Chew (Singapore), 180 Days of Problem Solving (Mỹ), đối chiếu với sách giáo khoa và đề thi thật.</p></div>
<div class="the"><h3>Kiểm từng điểm kiến thức</h3><p>Mỗi điểm kiến thức được đối chiếu với nguồn uy tín. Đáp số đề mẫu được máy giải lại. Mỗi Trạm có bước dạy thử trước khi chốt, và cô là người duyệt cuối.</p></div>
</div>
<p class="nho" style="margin-top:14px">Tài liệu từng Trạm được soạn dần theo quy trình này.</p>
</div></section>

<section class="khoi khoi--bac-ha"><div class="wrap keu">
<h2>Xem từng Trạm, từng mạch.</h2>
<div class="hang-nut"><a class="btn btn--chinh" href="/32-tram/">{N_TRAM} Trạm theo bảy mạch</a><a class="btn btn--phu" href="/lo-trinh/">Lộ trình theo năm</a></div>
</div></section>
"""


# ================= 32 TRẠM =================
def loc_nam(hien):
    out = ['<li><a class="chip" href="/32-tram/"' + (' aria-current="true"' if hien == "mach" else "") + ">Theo mạch</a></li>"]
    for n in (1, 2, 3):
        cur = ' aria-current="true"' if hien == n else ""
        out.append(f'<li><a class="chip" href="/32-tram/nam-{n}/"{cur}>Năm {n} ({len(TRAM_NAM[n])})</a></li>')
    return '<ul class="mach-hang">' + "".join(out) + "</ul>"


def trang_32_tram():
    khoi = ""
    for m in MACH_THU_TU:
        ds = sorted([t for t in T if t["mach"] == m], key=lambda t: (t["nam"], so_tram(t)))
        mo_ta = "".join(f"<li><b>Năm {i + 1}:</b> {esc(x)}</li>" for i, x in enumerate(MACH_MO_TA[m]))
        khoi += f"""<section class="nhom-mach" id="mach-{m}">
<div class="nhom-nam"><h2>{esc(MACH_TEN[m])}</h2><span>{len(ds)} Trạm chính</span></div>
<div class="mach-mo-ta c-{m}"><ul class="mach-bac" style="list-style:none;padding:0;margin:0">{mo_ta}</ul></div>
<div class="luoi luoi--3">{''.join(the_tram(t) for t in ds)}</div>
</section>"""
    return dau_trang("32 Trạm", f"{N_TRAM} Trạm theo {N_MACH} mạch",
                     "Chọn xem theo mạch hoặc theo năm. Mỗi Trạm có tên, câu hỏi lớn và câu hứa: sau Trạm này, con làm được điều gì.") + f"""
<section class="khoi"><div class="wrap">
<div class="loc"><div><h2>Xem theo</h2>{loc_nam('mach')}</div><div><h2>Nhảy tới mạch</h2>{chip_mach()}</div></div>
<p class="nho noi-dung">Mỗi Trạm thuộc một mạch chính. Ở dưới tên Trạm có ghi số buổi. Cả {N_TRAM} Trạm cộng lại là {sum(t['buoi'] for t in T)} buổi; phần còn lại của {N_BUOI} buổi là Học cách học, ôn tích hợp, đánh giá, tổng ôn và đề toàn phần (xem <a href="/lo-trinh/">Lộ trình</a>).</p>
{khoi}
</div></section>
"""


def trang_nam(n):
    v = NAM[n]
    ds = sorted(TRAM_NAM[n], key=so_tram)
    b = BUOI_NAM[n]
    khac = "".join(f'<li><a class="chip" href="/32-tram/nam-{k}/">Năm {k}</a></li>' for k in (1, 2, 3) if k != n)
    return dau_trang(f"Năm {n}", f"Năm {n}: {v['ten']}, {len(ds)} Trạm",
                     f"{v['tuoi'].capitalize()}, lớp {v['lop']}. {v['loi']}") + f"""
<section class="khoi"><div class="wrap">
<div class="loc"><div><h2>Xem theo</h2>{loc_nam(n)}</div></div>
<p class="noi-dung">Năm {n} có <b>{len(ds)}</b> Trạm trong <b>{b['buoi']}</b> buổi học ({b['tuan']} tuần, mỗi buổi {b['phut']} phút). Các Trạm xếp đúng thứ tự học.</p>
<div class="luoi luoi--3" style="margin-top:20px">{''.join(the_tram(t) for t in ds)}</div>
<p style="margin-top:26px"><span class="nho">Xem năm khác:</span></p><ul class="mach-hang">{khac}</ul>
</div></section>
"""


# ================= LỘ TRÌNH =================
def chang_cua_nam(n):
    """Gom các hàng của Mục lục 9.2 thành chặng: mỗi chặng kết thúc bằng Đánh giá."""
    hang = BUOI_NAM[n]["hang"]
    chang, cur = [], []
    for h in hang:
        cur.append(h)
        if h["khoi"] == "Đánh giá":
            chang.append(cur)
            cur = []
    return chang, cur


def trang_lo_trinh():
    out = ""
    for n in (1, 2, 3):
        v, b = NAM[n], BUOI_NAM[n]
        chang, du = chang_cua_nam(n)
        dong = ""
        for i, c in enumerate(chang, 1):
            tr = [h for h in c if h["khoi"].startswith("L")]
            on = sum(h["buoi"] for h in c if h["khoi"] == "Ôn")
            dg = sum(h["buoi"] for h in c if h["khoi"] == "Đánh giá")
            hcch = sum(h["buoi"] for h in c if h["khoi"] == "Học cách học")
            ten_tr = ", ".join(esc(ten_dep(next(t for t in T if t["ma"] == h["khoi"])["ten"])) for h in tr)
            ghi = []
            if hcch:
                ghi.append(f"Học cách học {hcch} buổi")
            ghi.append(f"Trạm {so_tram(next(t for t in T if t['ma'] == tr[0]['khoi']))}" + (f" đến {so_tram(next(t for t in T if t['ma'] == tr[-1]['khoi']))}" if len(tr) > 1 else "") + f" ({sum(h['buoi'] for h in tr)} buổi)")
            ghi.append(f"ôn tích hợp {on} buổi")
            ghi.append(f"đánh giá {dg} buổi")
            on_ten = next((h["noi_dung"] for h in c if h["khoi"] == "Ôn"), "")
            m_chang = re.search(r"Chặng (\d+)", on_ten)
            ten_chang = f"Chặng {m_chang.group(1)}" if m_chang else "Chặng cuối năm"
            dong += f"<li><h3>{ten_chang}</h3><p class=\"nho\">{'; '.join(ghi)}.</p><p>{ten_tr}.</p></li>"
        # phần cuối năm không thuộc chặng nào
        cuoi = ""
        if du:
            ten_khoi = {"Tổng ôn": "Tổng ôn", "Đề": "Đề toàn phần", "Nước rút": "Nước rút: bài nhẹ, không đề mới", "Đệm": "Buổi đệm"}
            goc = {}
            for h in du:
                goc[h["khoi"]] = goc.get(h["khoi"], 0) + h["buoi"]
            mo_ta = "; ".join(f"{ten_khoi.get(k, k)} {s} buổi" for k, s in goc.items())
            ten_c = "Về đích" if n == 3 else "Cuối năm"
            cuoi = f"<li><h3>{ten_c}</h3><p class=\"nho\">{mo_ta}.</p></li>"
        # bảng tổng
        gom = {}
        for h in b["hang"]:
            k = "Trạm" if h["khoi"].startswith("L") else h["khoi"]
            gom[k] = gom.get(k, 0) + h["buoi"]
        ten_k = {"Học cách học": "Học cách học", "Trạm": f"{len(TRAM_NAM[n])} Trạm", "Ôn": "Ôn tích hợp", "Đánh giá": "Đánh giá chặng và cuối năm",
                 "Đệm": "Buổi đệm", "Tổng ôn": "Tổng ôn", "Đề": "Đề toàn phần (làm và chữa)", "Nước rút": "Nước rút"}
        bang = "".join(f"<tr><td>{ten_k[k]}</td><td>{s}</td></tr>" for k, s in gom.items())
        assert sum(gom.values()) == b["buoi"], "tổng buổi lệch Mục lục"
        out += f"""<section class="khoi{' khoi--bac-ha' if n == 2 else ''}" id="nam-{n}"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Năm {n}, {v['tuoi']}, lớp {v['lop']}</span><h2>{v['ten']}</h2><p>{v['cay']} {v['loi']}</p></div>
<div class="hai-cot">
<div><ul class="dong">{dong}{cuoi}</ul></div>
<div class="the"><h3>Trong {b['buoi']} buổi</h3>
<p class="nho">{b['tuan']} tuần học, mỗi buổi {b['phut']} phút, hai buổi mỗi tuần{' (tháng cuối ba buổi mỗi tuần)' if n == 3 else ''}.</p>
<div class="bang-cuon"><table class="bang-buoi"><thead><tr><th>Nội dung</th><th>Buổi</th></tr></thead><tbody>{bang}</tbody><tfoot><tr><td>Cộng</td><td>{b['buoi']}</td></tr></tfoot></table></div>
<p style="margin-top:14px"><a class="lien-ket-mui" href="/32-tram/nam-{n}/">Các Trạm của năm {n}</a></p></div>
</div></div></section>"""
    return dau_trang("Lộ trình", "Lộ trình từ 8 đến 11 tuổi",
                     f"Ba năm liền, {N_BUOI} buổi học. Mỗi năm đứng trên vai năm trước.") + f"""
<section class="khoi khoi--trang"><div class="wrap noi-dung">
<ul class="so-chip" style="max-width:none">
<li><b>3</b><span>năm học</span></li><li><b>{N_BUOI}</b><span>buổi</span></li><li><b>{N_TRAM}</b><span>Trạm</span></li><li><b>{sum(b['tuan'] for b in BUOI_NAM.values())}</b><span>tuần học</span></li>
</ul>
<p style="margin-top:18px">Ngày học cụ thể của từng lớp do cô xếp riêng cho từng lớp.</p>
{cho("lich_khai_giang_lo_trinh", "Lịch khai giảng và ngày bắt đầu của các lớp sắp mở (nếu cô muốn cho ba mẹ thấy ở đây).")}
</div></section>
{out}
<section class="khoi"><div class="wrap keu">
<h2>Con ở năm nào là hợp?</h2>
<p class="noi-dung">Cô sẽ trao đổi với ba mẹ về con trước khi chọn lớp.</p>
<div class="hang-nut"><a class="btn btn--chinh" href="/dang-ky/">Đăng ký tư vấn</a><a class="btn btn--phu" href="/cau-hoi/">Câu hỏi thường gặp</a></div>
</div></section>
"""


# ================= MỤC TIÊU =================
def trang_muc_tieu():
    return dau_trang("Mục tiêu", "Ba kỳ thi, một con đường",
                     "Chương trình dạy con hiểu sâu. Ba kỳ thi dưới đây là nơi con dùng điều đã hiểu.") + f"""
<section class="khoi"><div class="wrap">
<div class="luoi luoi--3">
<article class="the"><span class="nhan">Kỳ thi 1</span><h3>Khảo sát vào lớp 6 Trường Trần Đại Nghĩa</h3>
<p>Phần Toán và tư duy logic có bài tự luận chấm theo từng bước, và đề có phần tiếng Anh. Vì vậy từ năm thứ hai, mỗi Trạm có một bài trình bày lời giải chấm theo bước, và đề tiếng Anh tăng dần.</p>
<p>Các dạng toán trong đề những năm gần đây đều có Trạm dạy dạng ấy: 157 câu đề thật đã được rà, câu nào cũng có chỗ trong chương trình.</p>
<p class="nho">Lịch khảo sát các năm sau chưa được công bố.</p></article>
<article class="the"><span class="nhan">Kỳ thi 2</span><h3>SASMO</h3>
<p>Olympic Toán quốc tế cho học sinh tiểu học. 25 câu, 90 phút: 15 câu trắc nghiệm và 10 câu điền đáp số.</p>
<p>Phần trắc nghiệm có trừ điểm câu sai, nên con được tập cân nhắc khi nào nên trả lời và khi nào nên bỏ qua.</p></article>
<article class="the"><span class="nhan">Kỳ thi 3</span><h3>TIMO</h3>
<p>Olympic Toán quốc tế. Vòng loại và vòng quốc gia gồm 25 câu, 90 phút; không trừ điểm câu sai. Đề chia đều năm mảng: tư duy logic, số học và đại số, lý thuyết số, hình học, tổ hợp.</p>
<p>Vì cách chấm khác SASMO, con được tập hai cách làm bài khác nhau.</p></article>
</div>
</div></section>

<section class="khoi khoi--bac-ha"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Chương trình phục vụ thế nào</span><h2>Cùng một nền, ba kỳ thi.</h2></div>
<div class="luoi luoi--3">
<div class="the"><h3>Hai năm đầu</h3><p>Con làm câu thử thách ★★★ lấy từ kho đề SASMO và TIMO. Đề được dịch và chỉnh số, không chép nguyên.</p></div>
<div class="the"><h3>Năm thứ hai</h3><p>Từ chặng hai, mỗi phiếu có một câu thử thách bằng tiếng Anh. Mỗi Trạm có một bài trình bày lời giải chấm theo bước.</p></div>
<div class="the"><h3>Năm thứ ba</h3><p>Con dự thi. Cuối năm có tổng ôn, bốn đề toàn phần và hai buổi nước rút nhẹ.</p></div>
</div>
</div></section>

<section class="khoi khoi--trang"><div class="wrap noi-dung">
<div class="luu-y"><p><b>Lời nói thật.</b> Kết quả mỗi kỳ thi còn tùy sức học và sự rèn luyện của con. Chương trình không hứa điểm số hay huy chương. Điều chương trình hứa là: con hiểu vì sao, biết trình bày, và dám bắt đầu cả với bài toán lạ.</p></div>
</div></section>

<section class="khoi"><div class="wrap keu">
<h2>Muốn hỏi riêng về con?</h2>
<div class="hang-nut"><a class="btn btn--chinh" href="/dang-ky/">Đăng ký tư vấn</a><a class="btn btn--phu" href="/lo-trinh/">Xem lộ trình</a></div>
</div></section>
"""


# ================= TỪ LỚP HỌC =================
def trang_tu_lop():
    vd = CH.get("vi_du_lop") or []
    ph = CH.get("phan_hoi") or []
    if vd:
        khoi_vd = '<div class="luoi luoi--3">' + "".join(
            f'<figure class="the" style="margin:0">' + (f'<img src="{esc(x["anh"])}" alt="{esc(x.get("mo_ta_anh", x["tieu_de"]))}" loading="lazy" style="border-radius:10px;margin-bottom:10px">' if x.get("anh") else "")
            + f'<h3>{esc(x["tieu_de"])}</h3><p>{esc(x["mo_ta"])}</p></figure>' for x in vd) + "</div>"
    else:
        khoi_vd = cho("vi_du_lop", "Ví dụ thật từ lớp: ảnh bài làm của các con (đã xin phép ba mẹ, che tên), kèm một dòng cô mô tả con đã làm gì. Gửi 3 đến 6 ví dụ. Không đưa đề thi, không đưa đáp án.", nho=False)
    if ph:
        khoi_ph = '<div class="luoi luoi--3">' + "".join(
            f'<blockquote class="the" style="margin:0"><p>“{esc(x["noi_dung"])}”</p><p class="nho">{esc(x.get("nguoi_noi", "Ba mẹ học sinh"))}</p></blockquote>' for x in ph) + "</div>"
    else:
        khoi_ph = cho("phan_hoi", "Phản hồi của ba mẹ (có phép), mỗi lời một hai câu, ghi “Ba mẹ của một bạn lớp 3” hay tên nếu ba mẹ đồng ý. Không dựng lời khen.")
    return dau_trang("Từ lớp học", "Từ lớp học của cô",
                     "Con làm gì trong lớp, và ba mẹ nói gì sau một thời gian.") + f"""
<section class="khoi"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Ví dụ từ lớp</span><h2>Một buổi học trông thế nào?</h2></div>
{khoi_vd}
</div></section>
<section class="khoi khoi--bac-ha"><div class="wrap">
<div class="khoi__dau"><span class="nhan">Phản hồi</span><h2>Ba mẹ nói gì?</h2></div>
{khoi_ph}
</div></section>
<section class="khoi"><div class="wrap keu">
<h2>Muốn xem thêm?</h2>
<div class="hang-nut"><a class="btn btn--chinh" href="/dang-ky/">Đăng ký tư vấn</a><a class="btn btn--phu" href="/phong-thi-nghiem/">Vào Phòng thí nghiệm</a></div>
</div></section>
"""


# ================= HỎI ĐÁP =================
def faq():
    mo = lambda v: "" if v else None
    muc = []
    muc.append(("Chương trình dành cho con tuổi nào?",
                "<p>Từ 8 đến 11 tuổi, từ lớp 3 đến lớp 5, học liền ba năm. Năm 1 là Xây nền (8 đến 9 tuổi), năm 2 là Dựng khung (9 đến 10 tuổi), năm 3 là Vươn cao (10 đến 11 tuổi).</p>"))
    muc.append(("Con có thể vào học giữa chừng không?",
                f"<p>{gia_tri('vao_giua_chung', 'Cô trả lời: con có vào năm 2 hay năm 3 được không, cần điều kiện gì.', nho=False)}</p>"))
    muc.append(("Một tuần con học thế nào?",
                "<p>Hai buổi mỗi tuần. Buổi dài 90 phút ở năm 1 và 105 phút ở năm 2, năm 3. Ở nhà con làm một phiếu sau mỗi buổi; phần chính khoảng 15 phút ở năm đầu, phần ★ đến ★★★ cho con muốn thử sức.</p>"))
    muc.append(("Chương trình khác gì lớp học thêm giải bài?",
                "<p>Chương trình không chia theo dạng bài. Mỗi Trạm là một câu hỏi lớn; con dừng lại 4 đến 7 buổi để hiểu tận gốc rồi mới đi tiếp. Con học nói chữ “vì”: vì sao đúng, vì sao làm thế.</p>"))
    muc.append(("Chương trình có theo kịp sách giáo khoa không?",
                "<p>Có. Trạm về kiến thức của sách giáo khoa được đặt cùng lúc hoặc sau khi trường dạy. Chỗ nào đi trước trường thì đi trước có chủ đích, thường không quá hai tháng, và có cầu nối bằng vật thật hoặc sơ đồ.</p>"))
    muc.append(("Học chương trình này có chắc vào được Trần Đại Nghĩa không?",
                "<p>Không ai hứa được điều đó, và cô cũng không hứa. Chương trình phủ các dạng toán trong đề những năm gần đây và rèn cả cách trình bày lời giải theo bước. Kết quả còn tùy sức học và sự rèn luyện của con. Lịch khảo sát các năm sau chưa được công bố.</p>"))
    muc.append(("Con có phải thi SASMO và TIMO không?",
                "<p>Hai năm đầu, con chỉ làm câu thử thách lấy từ đề hai kỳ thi này. Sang năm thứ ba, con dự thi.</p>"))
    muc.append(("Con học nhanh hơn bạn, hoặc chậm hơn bạn, thì sao?",
                "<p>Mỗi phiếu có phần chính vừa sức cả lớp và phần ★ đến ★★★ cho con muốn thử sức. Khi gặp khó khăn, con viết một câu hỏi vào ô riêng; đầu buổi sau cả lớp cùng gỡ từ câu hỏi của các con.</p>"))
    muc.append(("Ba mẹ theo dõi con bằng cách nào?",
                "<p>Cuối mỗi Trạm có thẻ kiểm tra 30 phút. Sau mỗi chặng 2 đến 4 Trạm có một tuần ôn tích hợp và một tuần đánh giá. Trang <a href=\"/hanh-trinh/\">Hành trình của con</a> đang được xây để ba mẹ xem con đã vững gì, còn vướng gì.</p>"))
    muc.append(("Phòng thí nghiệm là gì?",
                f"<p>Là nơi con thử, kéo, xếp và quan sát; mỗi bàn đi cùng một bài trong Bài học. Phòng thí nghiệm không hỏi tên và không lưu thông tin của con. Địa chỉ: <a href=\"{LAB}\">lab.tramtuduy.org</a>.</p>"))
    muc.append(("Học trực tiếp hay trực tuyến?",
                f"<p>{gia_tri('hinh_thuc_hoc', 'Cô cho biết lớp học trực tiếp hay trực tuyến (hoặc cả hai), và học ở đâu.', nho=False)}</p>"))
    muc.append(("Học phí và lịch khai giảng thế nào?",
                f"<p>{gia_tri('hoc_phi', 'Học phí (chỉ ghi khi cô đã chốt).', nho=False)}</p><p>{gia_tri('lich_khai_giang', 'Lịch khai giảng, ngày học trong tuần, giờ học (chỉ ghi khi cô đã chốt).', nho=False)}</p>"))
    muc.append(("Có học thử không?",
                f"<p>{gia_tri('hoc_thu', 'Cô cho biết có buổi học thử hay tư vấn miễn phí không, và cách đăng ký.', nho=False)}</p>"))
    out = []
    for q, a in muc:
        if "<p></p>" in a or a.strip() == "":
            continue
        out.append(f'<details class="hoi"><summary>{q}</summary><div class="hoi__tra">{a}</div></details>')
    return "\n".join(out)


def trang_cau_hoi():
    return dau_trang("Hỏi đáp", "Câu hỏi thường gặp",
                     "Những điều ba mẹ hay hỏi trước khi đăng ký cho con.") + f"""
<section class="khoi"><div class="wrap noi-dung">
{faq()}
<div class="luu-y" style="margin-top:26px"><p>Còn câu hỏi khác? <a href="/dang-ky/">Hỏi cô trực tiếp</a>.</p></div>
</div></section>
"""


# ================= ĐĂNG KÝ =================
def trang_dang_ky():
    lh = CH["lien_he"]
    dong = []
    dt = lh.get("dien_thoai")
    dong.append(("Điện thoại", f'<a href="tel:{re.sub(r"[^0-9+]", "", dt)}">{esc(dt)}</a>' if dt else cho("lien_he.dien_thoai", "Số điện thoại cô muốn ba mẹ gọi (cô quyết dùng số nào).", bat_buoc=False, nho=True)))
    z = lh.get("zalo")
    dong.append(("Zalo", f'<a href="https://zalo.me/{re.sub(r"[^0-9]", "", z)}">{esc(z)}</a>' if z else cho("lien_he.zalo", "Số Zalo hoặc đường liên kết Zalo.", nho=True)))
    em = lh.get("email")
    dong.append(("Email", f'<a href="mailto:{esc(em)}">{esc(em)}</a>' if em else cho("lien_he.email", "Địa chỉ email nhận câu hỏi của ba mẹ.", nho=True)))
    dong.append(("Địa chỉ lớp", gia_tri("dia_chi", "Địa chỉ lớp (nếu có lớp trực tiếp).", tu=lh)))
    dong.append(("Giờ nhận tư vấn", gia_tri("gio_tu_van", "Khung giờ cô hoặc trợ lý nhận tin.", tu=lh)))
    if DANG and not any(lh.get(k) for k in ("dien_thoai", "zalo", "email")):
        CHO_THIEU.append(("dang-ky", "lien_he.(it_nhat_mot)", "Cần ít nhất một cách liên hệ", True))
    bang = "".join(f"<tr><th scope=\"row\">{a}</th><td>{b}</td></tr>" for a, b in dong if b)
    return dau_trang("Đăng ký", "Đăng ký và liên hệ",
                     "Ba mẹ muốn hỏi, đăng ký hoặc xem lớp: đây là cách liên hệ với cô.") + f"""
<section class="khoi"><div class="wrap">
<div class="hai-cot">
<div class="noi-dung">
<h2>Liên hệ</h2>
<div class="bang-cuon"><table class="bang-buoi bang-lh"><tbody>{bang}</tbody></table></div>
<p class="nho" style="margin-top:14px">Trang này không có biểu mẫu và không thu thập thông tin của ba mẹ hay của con.</p>
</div>
<div class="noi-dung">
<h2>Khi nhắn cho cô, ba mẹ cho cô biết</h2>
<ul class="danh-sach-tick">
<li>Con mấy tuổi, đang học lớp mấy.</li>
<li>Con đã học toán thêm ở đâu chưa.</li>
<li>Điều ba mẹ mong muốn ở con.</li>
</ul>
<h2 style="margin-top:1.4em">Học phí, lịch, học thử</h2>
{gia_tri('hoc_phi', 'Học phí (chỉ ghi khi cô đã chốt).', nho=False)}
<div style="height:12px"></div>
{gia_tri('lich_khai_giang', 'Lịch khai giảng, ngày học trong tuần, giờ học (chỉ ghi khi cô đã chốt).', nho=False)}
<div style="height:12px"></div>
{gia_tri('hoc_thu', 'Có học thử hay tư vấn miễn phí không, và cách đăng ký.', nho=False)}
</div>
</div>
</div></section>
<section class="khoi khoi--bac-ha"><div class="wrap keu">
<h2>Chưa chắc? Đọc trước đã.</h2>
<div class="hang-nut"><a class="btn btn--chinh" href="/cau-hoi/">Câu hỏi thường gặp</a><a class="btn btn--phu" href="/lo-trinh/">Lộ trình ba năm</a></div>
</div></section>
"""


# ================= GIỚI THIỆU CÔ =================
def trang_co():
    c = CH["gioi_thieu_co"]
    if c.get("doan_van"):
        thanh = "".join(f"<p>{esc(p)}</p>" for p in c["doan_van"])
        ten = esc(c.get("ho_ten", "Cô Trang"))
    else:
        thanh = cho("gioi_thieu_co", "Họ tên đầy đủ, ảnh chân dung (nếu cô muốn), và ba bốn câu giới thiệu: cô dạy bao lâu, vì sao cô xây chương trình này. Chỉ ghi điều cô muốn ba mẹ biết.")
        ten = "Cô Trang"
    return dau_trang("Giới thiệu cô", "Người xây chương trình",
                     "Chương trình do cô Trang chủ biên và trực tiếp dạy.") + f"""
<section class="khoi"><div class="wrap">
<div class="hai-cot">
<div class="noi-dung"><h2>{ten}</h2>{thanh}</div>
<div class="the the--nen"><h3>Cô tin vào điều gì</h3>
<p>Con học tốt khi con hiểu vì sao. Con nhớ lâu khi kiến thức quay lại nhiều lần. Con tự tin khi dám bắt đầu với bài toán lạ.</p>
<p>Ba điều ấy là ba năm của chương trình: Xây nền, Dựng khung, Vươn cao.</p></div>
</div>
</div></section>
<section class="khoi khoi--bac-ha"><div class="wrap keu">
<h2>Muốn gặp cô?</h2>
<div class="hang-nut"><a class="btn btn--chinh" href="/dang-ky/">Đăng ký tư vấn</a><a class="btn btn--phu" href="/chuong-trinh/">Xem chương trình</a></div>
</div></section>
"""


# ================= PHÒNG THÍ NGHIỆM =================
def trang_lab():
    return dau_trang("Phòng thí nghiệm", "Phòng thí nghiệm Trạm Tư Duy",
                     "Kéo thử, xếp thử, nhìn thấy rồi mới hiểu. Mỗi bàn đi cùng một bài trong Bài học.") + f"""
<section class="khoi"><div class="wrap">
<div class="hai-cot">
<div class="noi-dung">
<h2>Con làm gì ở đây?</h2>
<p>Mỗi bàn thí nghiệm là một mô phỏng nhỏ. Con tự thay số, tự xếp, tự quan sát điều gì xảy ra, rồi nói lại bằng lời của mình.</p>
<ul class="danh-sach-tick">
<li>Mỗi bàn đi cùng một bài trong Bài học của con.</li>
<li>Con thử nhiều lần, không sợ sai.</li>
<li>Phòng thí nghiệm không hỏi tên và không lưu thông tin của con.</li>
</ul>
<div class="hang-nut"><a class="btn btn--chinh" href="{LAB}">Vào Phòng thí nghiệm</a></div>
<p class="nho" style="margin-top:12px">Phòng thí nghiệm nằm ở một địa chỉ riêng: <a href="{LAB}">lab.tramtuduy.org</a>. Địa chỉ này giữ nguyên để các mã QR trong sách vẫn mở đúng bàn.</p>
</div>
<div class="the the--nen"><h3>Hiện có</h3>
<p>Các bàn thí nghiệm cho năm 8 đến 9 tuổi. Các năm sau được thêm dần cùng chương trình.</p>
<h3 style="margin-top:1em">Ba mẹ ngồi xem cùng</h3>
<p>Ba mẹ có thể mở trên điện thoại hoặc máy tính bảng và để con tự thử.</p></div>
</div>
</div></section>
"""


# ================= HÀNH TRÌNH =================
def trang_hanh_trinh():
    return dau_trang("Hành trình của con", "Hành trình của con",
                     "Chỗ ba mẹ sẽ thấy con đã vững gì, còn vướng gì, tuần này nên làm gì.") + f"""
<section class="khoi"><div class="wrap noi-dung">
<div class="khoi__dau"><h2>Khu này đang được xây.</h2><p>Khi mở, ba mẹ sẽ thấy hành trình của riêng con qua từng Trạm. Trang này chưa có dữ liệu của bạn nào.</p></div>
<div class="cho" data-can-co-dien="hanh_trinh"><p><b class="cho__nhan">CHỜ HỒ SƠ HỌC SINH</b></p><p>Chỗ này chờ bộ khung kỹ năng và mẫu báo cáo từ phần Hồ sơ học sinh. Chưa đặt dữ liệu học sinh thật nào vào trang web công khai.</p></div>
<p style="margin-top:22px">Trong lúc chờ, ba mẹ có thể xem một hồ sơ mẫu trên web Trạm Tư Duy để hình dung cách theo dõi: <a href="{CHINH}/#/ho-so-mau">xem hồ sơ mẫu</a>.</p>
</div></section>
"""


# ================= 404 =================
def trang_404():
    return khung("", "Không tìm thấy trang", "Trang bạn tìm không có ở đây.", f"""
<section class="khoi"><div class="wrap noi-dung">
<h1>Không tìm thấy trang này.</h1>
<p>Có thể đường dẫn đã đổi. Mời ba mẹ về trang chủ hoặc xem {N_TRAM} Trạm.</p>
<div class="hang-nut"><a class="btn btn--chinh" href="/">Về trang chủ</a><a class="btn btn--phu" href="/32-tram/">Xem {N_TRAM} Trạm</a></div>
</div></section>""", khong_og=True).replace("<head>", '<head>\n<meta name="robots" content="noindex">', 1).replace("<title>Toán tư duy ba năm · Trạm Tư Duy</title>", "<title>Không tìm thấy trang · Toán tư duy Trạm Tư Duy</title>", 1)


# ================= CHẠY =================
def json_ld():
    d = {"@context": "https://schema.org", "@type": "EducationalOrganization", "name": "Trạm Tư Duy, Toán tư duy",
         "url": SITE + "/", "logo": SITE + "/tai-san/logo/bieu-tuong-512.png",
         "description": "Chương trình Toán tư duy ba năm cho các con từ 8 đến 11 tuổi."}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + "</script>\n"


def main():
    viet("", "Toán tư duy ba năm",
         f"Chương trình Toán tư duy ba năm cho các con từ 8 đến 11 tuổi: {N_TRAM} Trạm, {N_MACH} mạch tư duy, {N_BUOI} buổi học. Biết nghĩ, biết hỏi, biết trình bày.",
         trang_chu, og_tieu_de="Biết nghĩ. Biết hỏi. Biết trình bày.", og_phu=f"Toán tư duy ba năm, {N_TRAM} Trạm, cho các con từ 8 đến 11 tuổi.", json_ld=json_ld())
    viet("chuong-trinh", "Chương trình ba năm",
         f"Ba năm, {N_TRAM} Trạm, {N_MACH} mạch tư duy, {N_BUOI} buổi học: Xây nền, Dựng khung, Vươn cao. Mỗi Trạm là một câu hỏi lớn.",
         trang_chuong_trinh, hien="chuong-trinh", og_tieu_de="Chương trình Toán tư duy ba năm", og_phu="Xây nền, Dựng khung, Vươn cao: mỗi Trạm là một câu hỏi lớn.")
    viet("32-tram", f"{N_TRAM} Trạm theo {N_MACH} mạch",
         f"Cả {N_TRAM} Trạm của chương trình, xếp theo {N_MACH} mạch tư duy: tên Trạm, câu hỏi lớn, câu hứa, số buổi.",
         trang_32_tram, hien="32-tram", og_tieu_de=f"{N_TRAM} Trạm theo {N_MACH} mạch tư duy", og_phu="Mỗi Trạm một câu hỏi lớn, một câu hứa: sau Trạm này, con làm được điều gì.")
    for n in (1, 2, 3):
        v = NAM[n]
        viet(f"32-tram/nam-{n}", f"Năm {n}: {v['ten']}",
             f"Các Trạm của năm {n} ({v['tuoi']}, lớp {v['lop']}): {len(TRAM_NAM[n])} Trạm, {BUOI_NAM[n]['buoi']} buổi. {v['loi']}",
             (lambda n=n: trang_nam(n)), hien="32-tram", og_tieu_de=f"Năm {n}: {v['ten']}", og_phu=f"{v['tuoi'].capitalize()}, lớp {v['lop']}, {len(TRAM_NAM[n])} Trạm.")
    viet("lo-trinh", "Lộ trình 8 đến 11 tuổi",
         f"Lộ trình ba năm từ 8 đến 11 tuổi: số tuần, số buổi, các chặng, ôn tích hợp, đánh giá và tổng ôn. Tổng cộng {N_BUOI} buổi.",
         trang_lo_trinh, hien="lo-trinh", og_tieu_de="Lộ trình từ 8 đến 11 tuổi", og_phu=f"Ba năm liền, {N_BUOI} buổi. Mỗi năm đứng trên vai năm trước.")
    viet("muc-tieu", "Mục tiêu và ba kỳ thi",
         "Chương trình chuẩn bị cho con thế nào cho khảo sát vào lớp 6 Trần Đại Nghĩa, SASMO và TIMO, và lời nói thật về kết quả.",
         trang_muc_tieu, hien="muc-tieu", og_tieu_de="Ba kỳ thi, một con đường", og_phu="Khảo sát vào lớp 6 Trần Đại Nghĩa, SASMO, TIMO.")
    viet("tu-lop-hoc", "Từ lớp học",
         "Ví dụ từ lớp học của cô Trang và phản hồi của ba mẹ.",
         trang_tu_lop, hien="tu-lop-hoc", og_tieu_de="Từ lớp học của cô", og_phu="Con làm gì trong lớp, và ba mẹ nói gì sau một thời gian.")
    viet("cau-hoi", "Câu hỏi thường gặp",
         "Những điều ba mẹ hay hỏi trước khi cho con học Toán tư duy ba năm.",
         trang_cau_hoi, hien="cau-hoi", og_tieu_de="Câu hỏi thường gặp", og_phu="Con học thế nào, theo kịp sách giáo khoa không, có chắc đỗ không.")
    viet("dang-ky", "Đăng ký và liên hệ",
         "Cách liên hệ với cô Trang để hỏi, đăng ký hoặc xem lớp Toán tư duy.",
         trang_dang_ky, hien="", og_tieu_de="Đăng ký và liên hệ", og_phu="Ba mẹ muốn hỏi hay xem lớp: đây là cách liên hệ với cô.")
    viet("co-trang", "Giới thiệu cô Trang",
         "Cô Trang, người chủ biên và trực tiếp dạy chương trình Toán tư duy ba năm.",
         trang_co, hien="co-trang", og_tieu_de="Giới thiệu cô Trang", og_phu="Người xây chương trình Toán tư duy ba năm.")
    viet("phong-thi-nghiem", "Phòng thí nghiệm",
         "Phòng thí nghiệm Trạm Tư Duy: mô phỏng đi cùng từng bài học, để con kéo thử, xếp thử và nhìn thấy rồi mới hiểu.",
         trang_lab, hien="phong-thi-nghiem", og_tieu_de="Phòng thí nghiệm Trạm Tư Duy", og_phu="Kéo thử, xếp thử, nhìn thấy rồi mới hiểu.")
    viet("hanh-trinh", "Hành trình của con",
         "Nơi ba mẹ sẽ thấy con đã vững gì, còn vướng gì, tuần này nên làm gì. Khu này đang được xây.",
         trang_hanh_trinh, hien="hanh-trinh", og_tieu_de="Hành trình của con", og_phu="Con đã vững gì, còn vướng gì, tuần này nên làm gì.")

    (GOC / "404.html").write_text(trang_404(), encoding="utf-8")
    (GOC / "CNAME").write_text("toan.tramtuduy.org\n", encoding="utf-8")
    (GOC / "robots.txt").write_text(
        "User-agent: *\nAllow: /\nDisallow: /nguon/\nDisallow: /noi-bo/\nDisallow: /anh-kiem/\n\nSitemap: " + SITE + "/sitemap.xml\n", encoding="utf-8")
    ut = {"": "1.0", "chuong-trinh": "0.9", "32-tram": "0.9", "lo-trinh": "0.8", "muc-tieu": "0.8", "dang-ky": "0.8"}
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for slug, _, _ in TRANG:
        sm.append(f"<url><loc>{SITE}/{slug + '/' if slug else ''}</loc><lastmod>{NGAY}</lastmod><priority>{ut.get(slug, '0.6')}</priority></url>")
    sm.append("</urlset>")
    (GOC / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")

    # danh sách chỗ chờ cô điền
    gom = {}
    for trang, khoa, gy, bb in CHO_THIEU:
        gom.setdefault(khoa, [gy, bb, []])[2].append(trang)
    dong = ["# Chỗ CẦN CÔ ĐIỀN (máy tự lập khi dựng trang)", "",
            "Tệp này do `nguon/dung_site.py` ghi mỗi lần chạy. Cô nhắn nội dung, session Web điền vào `nguon/cau_hinh.json` rồi dựng lại.", "",
            "| Khóa | Cần gì | Xuất hiện ở trang | Bắt buộc khi đăng |", "|---|---|---|---|"]
    for k, (gy, bb, ds) in gom.items():
        dong.append(f"| `{k}` | {gy} | {', '.join(sorted(set(ds)))} | {'có' if bb else 'không (ẩn nếu để trống)'} |")
    (GOC / "noi-bo" / "CHO_CAN_CO_DIEN.md").write_text("\n".join(dong) + "\n", encoding="utf-8")
    print(f"Đã dựng {len(TRANG)} trang + 404. Chỗ chờ cô điền: {len(gom)} khóa ({len(CHO_THIEU)} lần xuất hiện).")
    if DANG:
        bb = [x for x in CHO_THIEU if x[3]]
        if bb:
            print("DỪNG: còn chỗ bắt buộc chưa điền:", sorted({x[1] for x in bb}))
            sys.exit(2)


if __name__ == "__main__":
    main()
