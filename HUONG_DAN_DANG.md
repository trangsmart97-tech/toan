# Hướng dẫn đăng web Toán lên toan.tramtuduy.org

Viết cho cô Trang, ngày 19/11/2026. Ba việc cô cần làm (tạo kho, bật trang, thêm bản ghi tên miền) đều cần tài khoản của cô, nên cô tự làm theo từng bước dưới đây. Em chưa làm gì trên mạng: chưa tạo kho, chưa đẩy lên, chưa chạm tên miền.

Cô đọc xong mục 0 rồi làm lần lượt mục 1 đến 6. Cả quá trình khoảng 30 phút, cộng thời gian chờ tên miền cập nhật (vài phút đến vài giờ).

## 0. Trước khi đăng, cô cần xong hai việc

1. **Duyệt chữ.** Mở thử trang ở máy: chạy lệnh `python3 -m http.server 8731` trong thư mục `6_WEB-TOAN`, rồi mở `http://127.0.0.1:8731/` bằng trình duyệt (hoặc nhờ Claude mở giúp). Xem các ảnh chụp trong `anh-kiem/` nếu chỉ muốn xem nhanh.
2. **Điền các chỗ “CẦN CÔ ĐIỀN”.** Danh sách ở `noi-bo/CHO_CAN_CO_DIEN.md` (cách liên hệ, học phí, lịch, hình thức học, ví dụ từ lớp, phản hồi, giới thiệu cô). Cô nhắn nội dung, Claude ghi vào `nguon/cau_hinh.json` rồi dựng lại. Bản đăng chính thức dựng bằng lệnh `python3 nguon/dung_site.py --dang`: lệnh này từ chối nếu chưa có ít nhất một cách liên hệ, và tự ẩn các khung tùy chọn mà cô chưa điền.

Không đăng khi trang còn khung nét đứt “CẦN CÔ ĐIỀN” (trừ khi cô chủ ý để lại).

## 1. Tạo kho GitHub mới

1. Đăng nhập GitHub bằng tài khoản đang chứa kho `phong-thi-nghiem` (cùng tài khoản với lab, để bản ghi tên miền ở mục 4 giống bản ghi của lab).
2. Bấm dấu **+** góc trên bên phải, chọn **New repository**.
3. **Repository name:** `toan`.
4. Chọn **Public** (công khai). GitHub Pages miễn phí cần kho công khai. Kho này chỉ chứa nội dung giới thiệu chương trình, không có dữ liệu học sinh, đề hay đáp án.
5. **Không** tích “Add a README file”, “.gitignore” hay “license”: để kho trống.
6. Bấm **Create repository**.

## 2. Đưa nội dung lên kho

Có hai cách. Cách A dễ hơn, không cần gõ lệnh.

**Cách A. Kéo thả trên trang GitHub**
1. Ở trang kho vừa tạo, bấm **uploading an existing file**.
2. Mở thư mục `6_WEB-TOAN` trong Finder. Chọn tất cả tệp và thư mục **trừ thư mục ẩn `.git`** (Finder thường không hiện thư mục ẩn, nên cô chỉ cần bấm Cmd + A). Kéo thả vào trang GitHub. Có khoảng 90 tệp, dưới mức 100 tệp của một lần tải lên (nếu GitHub báo quá nhiều tệp thì tải thư mục `anh-kiem` riêng, hoặc bỏ qua thư mục này).
3. Chờ tải xong, kéo xuống dưới, bấm **Commit changes**.
4. Kiểm tra: ở trang kho phải thấy `index.html`, `CNAME`, `.nojekyll` (tệp bắt đầu bằng dấu chấm có thể không được kéo; nếu thiếu `.nojekyll` thì cô bấm **Add file → Create new file**, đặt tên `.nojekyll`, để trống, bấm Commit; nếu thiếu `CNAME` thì tạo tệp tên `CNAME` với đúng một dòng `toan.tramtuduy.org`).

**Cách B. Đẩy từ máy (kho Git trên máy đã có sẵn các lần lưu)**
Cô cho phép, Claude chạy giúp ba lệnh sau, hoặc cô tự chạy trong thư mục `6_WEB-TOAN` (thay `TÊN-TÀI-KHOẢN` bằng tên tài khoản GitHub của cô):

```bash
git remote add origin https://github.com/TÊN-TÀI-KHOẢN/toan.git
git push -u origin main
```

Lần đầu GitHub sẽ hỏi đăng nhập. Claude không tự đẩy khi cô chưa nói “đẩy đi”.

## 3. Bật GitHub Pages và đặt tên miền

1. Ở kho `toan`, bấm **Settings** (thanh trên cùng).
2. Cột bên trái, bấm **Pages**.
3. Mục **Build and deployment → Source**: chọn **Deploy from a branch**.
4. **Branch:** chọn `main`, thư mục `/ (root)`, bấm **Save**.
5. Mục **Custom domain**: gõ `toan.tramtuduy.org`, bấm **Save**. (Nếu tệp `CNAME` đã có trong kho, ô này có thể đã điền sẵn.)
6. GitHub sẽ báo “DNS check unsuccessful” cho đến khi cô làm mục 4. Đó là bình thường.

Làm mục 3 **trước** mục 4 để không ai chiếm được tên `toan` trong lúc cô chưa gắn xong.

## 4. Thêm bản ghi tên miền `toan` (CNAME)

Cô vào trang quản lý tên miền `tramtuduy.org` (nơi cô đã tạo bản ghi `lab`, `luyende`, `luyennghe`). Thêm **một** bản ghi mới:

| Mục | Điền |
|---|---|
| Loại (Type) | `CNAME` |
| Tên (Host / Name) | `toan` |
| Giá trị (Value / Points to / Target) | `trangsmart97-tech.github.io` |
| TTL | để mặc định (hoặc 1 giờ) |

Ghi chú:
- Bản ghi của `lab` hiện trỏ đúng tới `trangsmart97-tech.github.io`; bản ghi mới giống hệt, chỉ khác tên. Nếu nơi quản lý tên miền bắt buộc dấu chấm cuối thì gõ `trangsmart97-tech.github.io.`
- Nếu cô dùng tài khoản GitHub khác cho kho `toan`, thay phần `trangsmart97-tech` bằng tên tài khoản đó (viết thường).
- **Không** sửa, **không** xóa bản ghi nào khác (đặc biệt là `lab`, `luyende`, `luyennghe`, bản ghi của `tramtuduy.org`). Chỉ thêm một dòng.
- Không dùng bản ghi loại A cho `toan`.

## 5. Chờ rồi bật HTTPS

1. Chờ vài phút đến vài giờ. Quay lại **Settings → Pages**: khi hiện dấu tích xanh “DNS check successful”, GitHub bắt đầu cấp chứng chỉ bảo mật.
2. Khi ô **Enforce HTTPS** sáng lên, tích vào. (Nếu chưa sáng, chờ thêm rồi làm lại; có thể mất tới một ngày.)

## 6. Cách kiểm sau khi đăng (từng bước)

**a. Tên miền đã trỏ đúng chưa.** Trong Terminal:

```bash
dig +short CNAME toan.tramtuduy.org
```

Phải ra `trangsmart97-tech.github.io.` (có thể kèm vài dòng địa chỉ).

**b. Trang mở được chưa.** Mở `https://toan.tramtuduy.org/` bằng điện thoại. Cô sẽ thấy trang chủ, ổ khóa an toàn trên thanh địa chỉ. Mở thử bốn trang: `/chuong-trinh/`, `/32-tram/`, `/lo-trinh/`, `/dang-ky/`. Gõ một địa chỉ sai như `/abc/` phải hiện trang “Không tìm thấy”.

**c. Máy kiểm tự động.** Trong thư mục `6_WEB-TOAN` (hoặc nhờ Claude):

```bash
python3 nguon/kiem_site.py --mang
```

Phải ra “ĐẠT, 0 lỗi chặn”. Kết quả ghi ở `noi-bo/KET_QUA_KIEM.md`.

**d. Chia sẻ trên mạng xã hội.** Gửi `https://toan.tramtuduy.org/32-tram/` vào Zalo (vào mục “Cloud của tôi” cho an toàn) và xem thẻ hiện ảnh và tiêu đề riêng. Với Facebook, mở https://developers.facebook.com/tools/debug/ , dán địa chỉ, bấm “Debug” rồi “Scrape Again” nếu thẻ còn cũ. Mỗi trang phải hiện ảnh và tiêu đề khác nhau.

**e. Phòng thí nghiệm không bị ảnh hưởng.** Quét một mã QR đã in trong sách: phải mở đúng bàn thí nghiệm như trước. Bấm nút “Vào Phòng thí nghiệm” trên web Toán: phải mở `https://lab.tramtuduy.org`. Web Toán chỉ dẫn vào lab, không sao chép hay đổi tên bất kỳ tệp nào của lab.

**f. Điện thoại và máy tính bảng thật.** Mở thử bằng iPhone hoặc iPad của cô: menu mở được, chữ đọc thoải mái, bấm nút dễ.

Chỉ khi cả sáu mục đều đạt thì báo điều phối gửi phiếu cho session Web của dự án Trần Đại Nghĩa thêm nút trỏ sang web Toán (phiếu đã soạn sẵn trong `0_DIEU-PHOI/BAN_GIAO/`). Không nên thêm nút sang trang chưa mở được.

## 7. Cập nhật nội dung sau này

1. Cô nhắn nội dung mới cho Claude (học phí, lịch, ví dụ từ lớp, …). Claude ghi vào `nguon/cau_hinh.json`.
2. Chạy `python3 nguon/dung_site.py --dang` (dựng lại), `python3 nguon/kiem_site.py` (kiểm), rồi lưu (`git commit`).
3. Đưa lên kho: Cách A (kéo thả tệp đã đổi, chọn “Replace”) hoặc Cách B (`git push`).
4. Khoảng 1 đến 2 phút sau, trang tự cập nhật.

## 8. Nếu có sự cố

| Thấy gì | Nên làm |
|---|---|
| “DNS check unsuccessful” kéo dài quá một ngày | Kiểm lại bản ghi ở mục 4: tên `toan`, loại CNAME, giá trị đúng. Chạy lệnh ở mục 6a. |
| Trang hiện nhưng mất màu, chữ xấu | Cô mở bằng địa chỉ `github.io/toan` thay vì `toan.tramtuduy.org`. Web Toán chỉ chạy đúng ở tên miền riêng; đặt tên miền ở mục 3 rồi dùng địa chỉ riêng. |
| Trang trắng hoặc 404 sau khi đăng | Vào **Settings → Pages**, xem Branch có là `main` và `/ (root)` chưa; vào tab **Actions** xem lần dựng gần nhất có báo lỗi không. |
| Thiếu tệp `.nojekyll` hoặc `CNAME` trên kho | Tạo bằng **Add file → Create new file** (xem mục 2, Cách A, bước 4). |
| Muốn gỡ trang | Xóa bản ghi `toan` ở nơi quản lý tên miền; kho GitHub để nguyên cũng không sao. |
