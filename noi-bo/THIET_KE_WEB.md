# Bản thiết kế web Toán tư duy: toan.tramtuduy.org

Bản 1, ngày 19/11/2026. CHỜ CÔ DUYỆT. Viết cho cô Trang; đọc xong cô biết web gồm những trang nào, mỗi trang nói gì, và chỗ nào còn chờ cô điền.

## 1. Web này để làm gì

Một nơi riêng cho chương trình Toán tư duy ba năm (QĐ-13), để web tramtuduy.org của dự án Trần Đại Nghĩa không phải gánh thêm. Người đọc chính là ba mẹ đang cân nhắc cho con học: ba mẹ cần biết chương trình dạy gì, con học thế nào, hướng tới kỳ thi nào, và liên hệ ở đâu. Ba mẹ thường mở trang này bằng điện thoại, từ một tin nhắn Zalo hay Facebook, nên trang được thiết kế cho điện thoại trước, rồi mới nới ra cho máy tính.

## 2. Sơ đồ trang

Mọi địa chỉ là đường dẫn thật (không dùng `/#/`), nên chia sẻ lên Zalo hay Facebook mỗi trang hiện đúng tiêu đề, mô tả và ảnh riêng.

| Địa chỉ | Trang | Trả lời câu hỏi nào của ba mẹ |
|---|---|---|
| `/` | Trang chủ | Đây là chương trình gì, dành cho con tuổi nào, nhìn nhanh có gì? |
| `/chuong-trinh/` | Chương trình ba năm | Ba năm học đi qua những gì, một Trạm học ra sao? |
| `/32-tram/` | 32 Trạm theo bảy mạch | Cụ thể con học những Trạm nào? Lọc theo năm hoặc theo mạch. |
| `/lo-trinh/` | Lộ trình 8 đến 11 tuổi | Từng năm khác nhau thế nào, có bao nhiêu buổi, mỗi buổi bao lâu? |
| `/muc-tieu/` | Mục tiêu: Trần Đại Nghĩa, SASMO, TIMO | Chương trình giúp con chuẩn bị cho kỳ thi nào, và nói thật được đến đâu? |
| `/tu-lop-hoc/` | Từ lớp học | Lớp học trông thế nào? Ba mẹ khác nói gì? (ví dụ thật, phản hồi: chờ cô cung cấp) |
| `/cau-hoi/` | Câu hỏi thường gặp | Những điều ba mẹ hay hỏi trước khi đăng ký. |
| `/dang-ky/` | Đăng ký và liên hệ | Làm sao để hỏi, đăng ký, học thử? (thông tin liên hệ: chờ cô điền) |
| `/co-trang/` | Giới thiệu cô | Ai là người xây chương trình? (chờ cô cung cấp) |
| `/phong-thi-nghiem/` | Cửa vào Phòng thí nghiệm | Mô phỏng đi cùng bài học nằm ở đâu? Dẫn tới `https://lab.tramtuduy.org`. |
| `/hanh-trinh/` | Hành trình của con | Chỗ trống chờ session Hồ sơ học sinh; trang này chưa có dữ liệu học sinh nào. |
| `/404.html` | Không tìm thấy | Đưa ba mẹ về trang chủ. |

Menu trên cùng (điện thoại gập vào nút “Menu”): Chương trình · 32 Trạm · Lộ trình · Mục tiêu · Từ lớp học · Hỏi đáp · nút “Đăng ký tư vấn”. Trong menu có thêm: Giới thiệu cô, Phòng thí nghiệm, và một dòng “Về web Trạm Tư Duy” trỏ về `https://tramtuduy.org` (đường về trang chính). Chân trang lặp lại các đường dẫn và ghi “Toán tư duy là một phần của Trạm Tư Duy”.

## 3. Từng trang gồm gì (thứ tự từ trên xuống, theo màn điện thoại)

**Trang chủ.** (1) Tiêu đề “Biết nghĩ. Biết hỏi. Biết trình bày.”, một câu giới thiệu, hai nút (“Xem 32 Trạm”, “Đăng ký tư vấn”), bốn con số (3 năm, 32 Trạm, 7 mạch, 252 buổi). (2) Ba năm như một cái cây: Xây nền, Dựng khung, Vươn cao. (3) “Mỗi Trạm là một câu hỏi lớn” với ba Trạm làm ví dụ. (4) Bốn bước giải mọi bài toán: THINK, PLAN, SOLVE, EXPLAIN. (5) Bảy mạch tư duy. (6) Ba kỳ thi đích. (7) Một tuần học của con. (8) Cửa vào Phòng thí nghiệm. (9) Từ lớp học (chờ cô). (10) Lời mời liên hệ.

**Chương trình ba năm.** Ba thẻ năm; “một tuần học” (hai buổi trên lớp, một phiếu ở nhà, thẻ kiểm tra cuối Trạm); bốn bước THINK, PLAN, SOLVE, EXPLAIN; nguồn chắt lọc (Archimedes, Terry Chew, 180 Days of Problem Solving, đối chiếu sách giáo khoa).

**32 Trạm.** Hai bộ lọc (năm, mạch) làm bằng liên kết thật nên không cần mạng mạnh; mỗi Trạm là một thẻ: số Trạm, năm, tên, câu hỏi lớn, câu hứa “Con … được …”, mạch, số buổi. Không in mã nội bộ; không in đề, không in đáp án.

**Lộ trình.** Dòng thời gian dọc, ba năm: tuổi, lớp, số tuần, số buổi, thời lượng mỗi buổi, các Trạm, ôn tích hợp, đánh giá chặng; năm cuối có tổng ôn, đề toàn phần, nước rút. Không ghi ngày học cụ thể (lịch lớp do cô và công cụ Lịch Lớp chốt).

**Mục tiêu.** Ba thẻ kỳ thi (khảo sát vào lớp 6 Trần Đại Nghĩa, SASMO, TIMO) nói đúng cách chương trình phục vụ từng kỳ; lời nói thật: không hứa kết quả, lịch thi các năm sau chưa công bố.

**Từ lớp học, Hỏi đáp, Đăng ký, Giới thiệu cô, Phòng thí nghiệm, Hành trình.** Xem mục 6 về chỗ chờ cô điền.

## 4. Thiết kế điện thoại trước

- Một cột, lề trái và phải 20 px; thẻ xếp dọc; nút cao tối thiểu 48 px; khoảng cách giữa hai nút bấm tối thiểu 12 px (ngón cái chạm đúng).
- Chữ thân bài 17 px (1,0625 rem), giãn dòng 1,65; không có chữ nào dưới 16 px (kể cả nhãn nhỏ, chú thích, chân trang).
- Tiêu đề nét 600, giãn dòng 1,15 đến 1,2, không ép khoảng cách chữ (theo bộ nhận diện).
- Menu: nút “Menu” mở danh sách dọc cỡ lớn. Nếu trình duyệt tắt JavaScript, danh sách vẫn hiện sẵn.
- Từ 760 px: thẻ xếp hai cột; từ 1040 px: ba hoặc bốn cột, khung rộng tối đa 1120 px, menu trải ngang.
- Giảm chuyển động: mọi hiệu ứng chuyển động (nhấc thẻ khi rê chuột, cuộn mượt) tắt khi thiết bị đặt “giảm chuyển động”. Trang không có hoạt cảnh nào bắt buộc để hiểu nội dung.
- Tải nhanh: không khung dựng sẵn (framework), không phông ngoài chặn hiển thị, mỗi trang chỉ một tệp CSS (khoảng 20 KB), một tệp JS rất nhỏ (menu, lọc), ảnh chia sẻ chỉ tải khi mạng xã hội cần. Mục tiêu: trang chủ dưới 200 KB lần đầu (không tính logo trong bộ nhận diện).

## 5. Nhận diện và giọng văn

- Logo ngang Bản 2 ở đầu trang, logo dọc ở chân trang và ảnh chia sẻ; biểu tượng làm tab và biểu tượng ứng dụng. Chép nguyên từ bộ nhận diện, kèm md5 (xem `tai-san/logo/MD5.txt`).
- Màu: tím chàm `#463665` (chữ tiêu đề, nút chính), nâu đất `#7A4E32` (nhãn phụ), cát `#A86F45` và `#D2A06C` (chỉ để trang trí, không dùng cho chữ), bạc hà `#EAF7F1` (nền tươi), kem `#FFF9F0` (nền chính). Bảy mạch dùng bảy chấm màu lấy từ bảng trạng thái của web hiện có; luôn đi kèm chữ, không bao giờ chỉ dựa vào màu.
- Phông: Inter; trên máy Apple dùng phông hệ thống, giống web hiện có.
- Giọng văn giống web tramtuduy.org: ngắn, ấm, nói bằng ẩn dụ cây (rễ, thân, tán), nói với ba mẹ là “ba mẹ” và nói về học sinh là “con”, “các con”. Câu ngắn, mỗi đoạn một ý.
- Quy ước chữ viết của dự án: chỉ dùng ngoặc “ ” và ‘ ’; không dùng từ cô đã bỏ; không dùng “con” làm từ đếm; không gạch “–” giữa hai số (viết “từ 8 đến 11 tuổi”); không in mã nội bộ như L3·T1.
- Không ghi học phí, lịch học, địa chỉ, số điện thoại, email khi cô chưa cung cấp. Không có ví dụ đề thi, không đáp án, không dữ liệu học sinh thật.

## 6. Chỗ chờ cô điền (hiện là khung đứt nét có chữ “CẦN CÔ ĐIỀN”)

Danh sách đầy đủ ở phiếu bàn giao. Gồm: cách liên hệ (số điện thoại, Zalo, email, địa chỉ lớp), học phí, lịch khai giảng và hình thức học (lớp trực tiếp hay trực tuyến), ví dụ thật từ lớp (ảnh bài làm đã xin phép), phản hồi của phụ huynh (có phép), giới thiệu cô Trang (ảnh và vài dòng), trang trả lời cho vài câu hỏi thường gặp cần cô quyết. Cách điền: cô nhắn nội dung, session Web ghi vào tệp `nguon/cau_hinh.json` rồi dựng lại trang. Máy dựng trang từ chối bản “đăng” nếu còn chỗ trống bắt buộc.

## 7. Liên kết hai chiều

- Từ web Toán về web chính: dòng “Về web Trạm Tư Duy” trong menu và chân trang, trỏ `https://tramtuduy.org`.
- Từ web chính sang web Toán: chỉ một thay đổi, mô tả ở phiếu gửi session Web của dự án Trần Đại Nghĩa.
- Sang Phòng thí nghiệm: `https://lab.tramtuduy.org` (giữ nguyên địa chỉ để mã QR đã in vẫn mở); web Toán chỉ dẫn vào, không sao chép, không đổi tên tệp lab.

## 8. Cổng kiểm trước khi đăng

Kiểm liên kết, chữ viết, số liệu với Mục lục 9.2, thẻ chia sẻ, kích thước tải, Phòng thí nghiệm mở đúng. Lệnh chạy và kết quả ở `noi-bo/KET_QUA_KIEM.md`.
