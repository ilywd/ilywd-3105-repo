# ilywd 3105 Location Tools Repository

Đây là repository độc lập dùng đúng giao thức nguồn công khai của 3105. Repository
không yêu cầu chỉnh sửa, chép file vào hoặc thay đổi cấu trúc mã nguồn của 3105.

## Nguyên tắc tích hợp

- 3105 chỉ đọc `repo.json` qua HTTPS.
- Mỗi công cụ được phát hành dưới dạng gói `.3105` do chính 3105 xuất.
- Repository chỉ chứa metadata, ảnh giới thiệu và file tải xuống.
- Không đưa UUID container vào Patch; dùng Bundle ID hoặc App Group ID ổn định.
- Không đưa token, cookie, tài khoản hay dữ liệu xác thực vào repository.
- Chỉ phát hành công cụ cho ứng dụng và dữ liệu mà người tạo có quyền chỉnh sửa.

## Cấu trúc

```text
ilywd-3105-location-repo/
├── repo.json
├── sources.json
├── packages/
├── templates/location-color/
│   ├── settings.json
│   ├── payload.example.json
│   └── package.example.json
├── docs/
│   ├── AUTHOR_INTEGRATION.vi.md
│   └── LOCATION_TOOL_SPEC.vi.md
└── scripts/
    └── validate_repo.py
```

## Cách hoàn thiện Tool định vị

1. Xác định app đích thuộc quyền quản lý và Bundle ID hoặc App Group ID của nó.
2. Xác định file cấu hình thật chứa màu định vị và đường dẫn tương đối trong container.
3. Sao chép `templates/location-color/settings.json` vào workspace Patch.
4. Chuyển `payload.example.json` thành đúng plist/JSON mà app đích sử dụng.
5. Apply trên dữ liệu thử nghiệm, kiểm tra khởi động lại và Restore.
6. Xuất file `.3105` từ 3105 vào thư mục `packages/`.
7. Tính SHA-256, dung lượng và thêm package vào `repo.json`.
8. Chạy `python3 scripts/validate_repo.py` trước khi đưa lên HTTPS.

## URL sau khi đưa lên GitHub

```text
https://raw.githubusercontent.com/ilywd/ilywd-3105-repo/main/repo.json
```

Người dùng thêm URL này trong tab **Nguồn** của 3105. Không cần tích hợp cứng URL
vào ứng dụng. Nếu tác giả đồng ý đưa repo vào catalog mặc định, chỉ cần thêm URL
trên vào `sources.json` của catalog chính thức.

## Color Studio

Web tạo cấu hình màu trung tính đã được xuất bản tại:

```text
https://ilywd-color-studio.truongk593.chatgpt.site
```

Web đã lấy đúng bộ tham số từ `ilywd_3105_FREE_COLOR_TOOL`: tên patch, màu súng,
màu viền, độ trong màu và độ dày viền. Kết quả được xuất thành cấu hình JSON; bốn
gói demo trong repo dùng đích trung tính `com.test` tại `Documents/ilywd/test`.

## Trạng thái hiện tại

Repo có bốn package `.3105` demo: đỏ, xanh dương, vàng và tím. Tất cả chỉ trỏ tới
Bundle ID trung tính `com.test` và file thử nghiệm `Documents/ilywd/test`; không
chứa tên hoặc đường dẫn của game bên
thứ ba. Đây là bộ minh hoạ tích hợp Repo, không phải cấu hình sản xuất.
