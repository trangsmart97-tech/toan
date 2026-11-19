# Chỗ CẦN CÔ ĐIỀN (máy tự lập khi dựng trang)

Tệp này do `nguon/dung_site.py` ghi mỗi lần chạy. Cô nhắn nội dung, session Web điền vào `nguon/cau_hinh.json` rồi dựng lại.

| Khóa | Cần gì | Xuất hiện ở trang | Bắt buộc khi đăng |
|---|---|---|---|
| `vi_du_lop_trang_chu` | Hai hoặc ba ví dụ thật từ lớp: ảnh bài làm của các con (đã xin phép ba mẹ, che tên), kèm một dòng mô tả; và lời nhận xét của ba mẹ (có phép). | trang-chu | không (ẩn nếu để trống) |
| `lich_khai_giang_lo_trinh` | Lịch khai giảng và ngày bắt đầu của các lớp sắp mở (nếu cô muốn cho ba mẹ thấy ở đây). | lo-trinh | không (ẩn nếu để trống) |
| `vi_du_lop` | Ví dụ thật từ lớp: ảnh bài làm của các con (đã xin phép ba mẹ, che tên), kèm một dòng cô mô tả con đã làm gì. Gửi 3 đến 6 ví dụ. Không đưa đề thi, không đưa đáp án. | tu-lop-hoc | không (ẩn nếu để trống) |
| `phan_hoi` | Phản hồi của ba mẹ (có phép), mỗi lời một hai câu, ghi “Ba mẹ của một bạn lớp 3” hay tên nếu ba mẹ đồng ý. Không dựng lời khen. | tu-lop-hoc | không (ẩn nếu để trống) |
| `vao_giua_chung` | Cô trả lời: con có vào năm 2 hay năm 3 được không, cần điều kiện gì. | cau-hoi | không (ẩn nếu để trống) |
| `hinh_thuc_hoc` | Cô cho biết lớp học trực tiếp hay trực tuyến (hoặc cả hai), và học ở đâu. | cau-hoi | không (ẩn nếu để trống) |
| `hoc_phi` | Học phí (chỉ ghi khi cô đã chốt). | cau-hoi, dang-ky | không (ẩn nếu để trống) |
| `lich_khai_giang` | Lịch khai giảng, ngày học trong tuần, giờ học (chỉ ghi khi cô đã chốt). | cau-hoi, dang-ky | không (ẩn nếu để trống) |
| `hoc_thu` | Cô cho biết có buổi học thử hay tư vấn miễn phí không, và cách đăng ký. | cau-hoi, dang-ky | không (ẩn nếu để trống) |
| `lien_he.dien_thoai` | Số điện thoại cô muốn ba mẹ gọi (cô quyết dùng số nào). | dang-ky | không (ẩn nếu để trống) |
| `lien_he.zalo` | Số Zalo hoặc đường liên kết Zalo. | dang-ky | không (ẩn nếu để trống) |
| `lien_he.email` | Địa chỉ email nhận câu hỏi của ba mẹ. | dang-ky | không (ẩn nếu để trống) |
| `dia_chi` | Địa chỉ lớp (nếu có lớp trực tiếp). | dang-ky | không (ẩn nếu để trống) |
| `gio_tu_van` | Khung giờ cô hoặc trợ lý nhận tin. | dang-ky | không (ẩn nếu để trống) |
| `gioi_thieu_co` | Họ tên đầy đủ, ảnh chân dung (nếu cô muốn), và ba bốn câu giới thiệu: cô dạy bao lâu, vì sao cô xây chương trình này. Chỉ ghi điều cô muốn ba mẹ biết. | co-trang | không (ẩn nếu để trống) |
