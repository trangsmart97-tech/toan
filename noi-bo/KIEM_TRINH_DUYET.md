# Kiểm bằng trình duyệt thật (19/11/2026)

Làm bằng trình duyệt tích hợp và Google Chrome không giao diện, chạy cục bộ ở `http://127.0.0.1:8731/` (máy chủ tĩnh của Python). Không đăng gì lên mạng.

| Việc kiểm | Cách làm | Kết quả |
|---|---|---|
| Bố cục điện thoại | Khung 390 px (và 360 px), mở từng trang | Đạt: một cột, nút rộng cả hàng, không cắt chữ |
| Tràn ngang | Mở 15 trang ở 4 khổ (360, 390, 768, 1280 px), đo chiều rộng nội dung | Đạt: không trang nào rộng hơn màn hình |
| Cỡ chữ | Đo cỡ chữ thật của mọi thành phần chứa chữ ở 4 khổ trên | Đạt: không có chữ nào dưới 16 px |
| Menu điện thoại | Bấm nút “Menu”, mở rồi đóng | Đạt: danh sách dọc cỡ lớn, có nút Đăng ký tư vấn; menu dài hơn màn hình thì cuộn được |
| Menu máy tính | Khung 1280 px | Đạt: menu nằm ngang một hàng (từ 1180 px trở lên) |
| Ảnh chụp | `anh-kiem/dien-thoai-*.jpg`, `anh-kiem/may-tinh-*.jpg` (15 trang × 2 khổ) | Có đủ |
| Ảnh chia sẻ | Mở từng ảnh `tai-san/og/*.png` (1200×630) | Đạt: chữ rõ, logo đúng, không bị cắt |

Chưa kiểm được ở lượt này (cần máy thật hoặc sau khi đăng): xem trước chia sẻ trên Zalo và Facebook bằng đường dẫn thật `toan.tramtuduy.org` (hai mạng xã hội chỉ đọc được trang đã đăng công khai); tốc độ trên mạng 4G thật; chạy trên iPhone, iPad thật.
