# Ghi chú gửi tác giả 3105

Repository này được thiết kế để dùng nguyên giao thức Repository v1 hiện có của
3105. Không yêu cầu thay đổi mã nguồn, cấu trúc thư mục, tab giao diện, patch
engine hoặc danh sách nguồn mặc định.

## Cách dùng không sửa 3105

1. Chủ repo đưa toàn bộ thư mục lên một host HTTPS, ví dụ GitHub raw.
2. Người dùng tự thêm URL `repo.json` trong tab **Nguồn**.
3. 3105 kiểm tra schema, URL HTTPS, phiên bản iOS, SHA-256 và gói `.3105` như mọi
   repository khác.
4. Patch được cài vào thư viện hiện tại và đi qua Apply/Restore hiện có.

## Tuỳ chọn nếu tác giả muốn duyệt repo mặc định

Tác giả chỉ cần thêm URL `repo.json` vào catalog nguồn chính thức. Đây là thay đổi
dữ liệu catalog, không phải sửa cấu trúc ứng dụng. Nếu không duyệt, repository vẫn
hoạt động bằng cách thêm nguồn thủ công.

## Cam kết phạm vi

- Không phụ thuộc API riêng hoặc entitlement mới.
- Không ghi thẳng vào dữ liệu nội bộ của 3105.
- Không thay manifest `.3105-project.plist` bằng tay.
- Không phân phối token, cookie hoặc dữ liệu xác thực.
- Không dùng Patch để vượt cơ chế thanh toán hoặc xác thực của ứng dụng khác.
