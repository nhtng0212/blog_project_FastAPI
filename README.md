Blog API System - Backend Assignment
Dự án xây dựng hệ thống REST API cho mạng xã hội Blog, hỗ trợ đa nền tảng (Web/Mobile). Hệ thống được thiết kế với tư duy Clean Code, bảo mật JWT và tối ưu hóa hiệu năng bằng Redis Caching.

🚀 Tính năng chính
Xác thực & Phân quyền:

Đăng ký, Đăng nhập và Quản lý phiên bằng JWT (Access Token & Refresh Token).

Cơ chế Blacklist/Revoke Token qua Redis khi Logout hoặc khi bị Admin khóa tài khoản.

Phân quyền rõ ràng giữa Admin (Duyệt bài, khóa người dùng) và User (Viết bài, bình luận).

Quản lý bài viết (Post):

CRUD bài viết với hỗ trợ gắn thẻ (Tags).

Cơ chế duyệt bài (Pending/Approved).

Tối ưu hóa tốc độ tải danh sách bài viết bằng Redis Cache.

Hệ thống Bình luận (Comment):

Người dùng có thể bình luận vào các bài viết đã được phê duyệt.

Hỗ trợ lưu trữ Media (Ảnh/Video) giả lập qua LocalStack (S3).

Hạ tầng:

Database: PostgreSQL (Lưu trữ dữ liệu quan hệ).


💻 Hướng dẫn cài đặt và chạy Local
1. Yêu cầu hệ thống
Đã cài đặt Docker và Docker Compose.

2. Các bước khởi chạy
Clone dự án:

Bash
git clone <repository_url>
cd blog_project
Cấu hình biến môi trường:
Tạo file .env tại thư mục gốc và cấu hình các thông số (có thể tham khảo file .env.example).

Khởi động bằng Docker Compose:

PowerShell
docker-compose up -d --build
Thiết lập S3 Bucket (LocalStack):
Do giới hạn quyền trên các hệ điều hành khác nhau, bạn cần cấp quyền thực thi cho script khởi tạo:

PowerShell
# Dành cho Windows (PowerShell)
docker exec -it blog_project-localstack-1 chmod +x /etc/localstack/init/ready.d/init_s3.sh
docker exec -it blog_project-localstack-1 /etc/localstack/init/ready.d/init_s3.sh
3. Truy cập tài liệu API
Sau khi hệ thống khởi động thành công, bạn có thể truy cập tài liệu API tự động tại:

Swagger UI: http://localhost:8000/docs

ReDoc: http://localhost:8000/redoc

📝 Báo cáo kỹ thuật (Report)
Các trở ngại và giải pháp:
Bảo mật: Đã xử lý lỗi cho phép bình luận trên bài viết chưa phê duyệt (PENDING) bằng cách chặn trực tiếp tại tầng Service.

Hiệu năng: Triển khai cơ chế Cache Aside với Redis. Khi có bài viết mới hoặc bình luận mới, hệ thống tự động xóa cache (Invalidation) để đảm bảo tính nhất quán dữ liệu.

Hạ tầng giả lập: Xử lý lỗi NoSuchBucket và lỗi phân quyền thực thi trên LocalStack bằng các script khởi tạo tự động.

Các điểm Bonus đạt được:
[x] Sử dụng Docker & Docker Compose.

[x] Phân quyền Admin/User (Authorization).

[x] Tích hợp Caching (Redis).

[x] Xử lý lỗi và kiểm tra dữ liệu đầu vào (Validation) chặt chẽ.

Cache: Redis (Lưu trữ Session và danh sách dữ liệu thường truy cập).

Storage: LocalStack (Giả lập AWS S3 để upload file).
