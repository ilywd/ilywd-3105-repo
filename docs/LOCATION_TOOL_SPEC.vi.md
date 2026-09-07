# Đặc tả Color Tool

## Mục tiêu

Tách bộ điều khiển từ `ilywd_3105_FREE_COLOR_TOOL`: tên patch, màu súng, màu
viền, độ trong màu và độ dày viền. Web xuất cấu hình trung tính để tác giả 3105
có thể nối với engine hợp lệ mà không thay đổi cấu trúc ứng dụng hiện tại.

## Luồng người dùng

1. Cài Tool từ repo.
2. Mở Tool trong **Đã cài**.
3. Chọn màu súng, màu viền, độ trong và độ dày viền.
4. Đóng ứng dụng đích.
5. Bấm **Áp dụng patch**.
6. Mở lại ứng dụng đích để kiểm tra.
7. Dùng **Khôi phục file gốc** khi muốn hoàn tác.

## Dữ liệu phải xác minh trước khi tạo package thật

- Bundle ID hoặc App Group ID ổn định.
- Loại container: `Application` hay `AppGroup`.
- Đường dẫn tương đối của plist/JSON.
- Key chính xác chứa màu súng, màu viền, alpha và độ dày viền.
- Định dạng màu: HEX, RGB 0-255, RGB 0-1 hoặc số nguyên ARGB.
- Thời điểm app đích đọc lại file: ngay lập tức, khi mở lại hay khi bắt đầu phiên.
- Dải iOS và phiên bản app đã thử nghiệm.

## Quy tắc an toàn

- Merge đúng key thay vì thay toàn bộ file nếu file còn chứa dữ liệu khác.
- Backup và thử Restore trên dữ liệu kiểm tra trước khi phát hành.
- Không chứa đường dẫn tuyệt đối, UUID container hoặc symbolic link.
- Không để hai payload cùng trỏ tới một file đích.
- Không lưu dữ liệu xác thực trong `settings.json` hoặc metadata repo.

## Tiêu chí hoàn thành

- Apply thành công trên ít nhất một bản app được hỗ trợ.
- Màu thay đổi sau đúng thao tác reload đã mô tả.
- Restore trả file về đúng byte ban đầu.
- SHA-256 và dung lượng trong `repo.json` khớp package.
- Package bị từ chối an toàn trên phiên bản không tương thích.
