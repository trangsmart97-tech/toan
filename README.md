# Web Toán tư duy Trạm Tư Duy (toan.tramtuduy.org)

Site tĩnh cho chương trình Toán tư duy ba năm. Bản 1, 19/11/2026, CHỜ CÔ DUYỆT; chưa đăng lên mạng.

- Thiết kế: `noi-bo/THIET_KE_WEB.md`
- Hướng dẫn đăng (cho cô Trang): `HUONG_DAN_DANG.md`
- Kết quả kiểm: `noi-bo/KET_QUA_KIEM.md`, `noi-bo/KIEM_TRINH_DUYET.md`; ảnh chụp: `anh-kiem/`
- Chỗ chờ cô điền: `noi-bo/CHO_CAN_CO_DIEN.md`; nội dung điền ở `nguon/cau_hinh.json`

Dựng lại và kiểm (cần Python 3 và Pillow; chạy ở thư mục này):

```bash
python3 nguon/trich_muc_luc.py     # trích số liệu từ tệp Word Mục lục 9.2 (chỉ đọc)
python3 nguon/dung_site.py         # dựng bản xem trước
python3 nguon/dung_site.py --dang  # dựng bản đăng (từ chối nếu thiếu cách liên hệ)
python3 nguon/kiem_site.py --mang  # cổng kiểm
python3 -m http.server 8731        # xem thử tại http://127.0.0.1:8731/
```

Số liệu (32 Trạm, 252 buổi) đều lấy từ Mục lục 9.2 qua `nguon/du-lieu/`; không gõ tay trong trang. Logo chép nguyên từ bộ nhận diện Bản 2, md5 ở `tai-san/logo/MD5.txt`. Không có dữ liệu học sinh, đề hay đáp án trong kho này.
