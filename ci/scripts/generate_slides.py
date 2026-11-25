# -*- coding: utf-8 -*-
"""
Script tạo bộ Slide thuyết trình Tổng quan Dự án & CI/CD (15 Slides):
1. File PowerPoint chuẩn OpenXML (.pptx): Slide_Thuyet_Trinh_Du_An_PetManagement_CICD.pptx
2. File Web Slide tương tác (HTML5 16:9): Slide_Thuyet_Trinh_Du_An.html & wwwroot/slides.html
3. File Kịch bản thuyết trình chi tiết (Markdown): SLIDE_THUYET_TRINH.md
"""

import base64
import os
import shutil
import struct
import zipfile
from xml.sax.saxutils import escape

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
OUT_PPTX = os.path.join(ROOT_DIR, "Slide_Thuyet_Trinh_Du_An_PetManagement_CICD.pptx")
OUT_WWW_PPTX = os.path.join(ROOT_DIR, "wwwroot", "Slide_Thuyet_Trinh_Du_An_PetManagement_CICD.pptx")
OUT_HTML = os.path.join(ROOT_DIR, "Slide_Thuyet_Trinh_Du_An.html")
OUT_WWW_HTML = os.path.join(ROOT_DIR, "wwwroot", "slides.html")
OUT_MD = os.path.join(ROOT_DIR, "SLIDE_THUYET_TRINH.md")


def get_png_dimensions(path):
    try:
        with open(path, "rb") as f:
            h = f.read(24)
            if len(h) >= 24 and h[:8] == b"\x89PNG\r\n\x1a\n":
                w, ht = struct.unpack(">II", h[16:24])
                if w > 0 and ht > 0:
                    return w, ht
    except Exception:
        pass
    return 1280, 720


SLIDES_DATA = [
    {
        "num": 1,
        "section": "TỔNG QUAN ĐỀ TÀI",
        "title": "HỆ THỐNG QUẢN LÝ & CHĂM SÓC THÚ CƯNG (PETCARE HUB)",
        "subtitle": "Kết hợp Quy trình Triển khai Tự động CI/CD (Jenkins, SonarQube, Docker, SSH) & Giám sát (Prometheus, Grafana)",
        "bullets": [
            "Nền tảng ứng dụng: ASP.NET Core 8.0 Web API + Giao diện SPA (Vanilla JS) + Microsoft SQL Server 2022",
            "Kho mã nguồn GitHub: https://github.com/Hoc123421/pet-management-system",
            "Hạ tầng vận hành: 9 Docker Containers chia làm 3 cụm (App, CI/CD, Monitoring) trên mạng ảo petnet",
            "Chất lượng kiểm định: 100% Pass Unit Test (xUnit), SonarQube Quality Gate PASSED (Coverage 91.2%, Rating A)",
            "Triển khai & Giám sát: 2 Jenkins Pipelines (Local & Remote SSH) + Prometheus (4/4 UP) + Grafana (8 Panels)"
        ],
        "highlights": [
            (".NET 8 + SQL 2022", "Kiến trúc Backend & CSDL bền vững"),
            ("9 Containers", "3 cụm Docker Compose trên mạng petnet"),
            ("91.2% Coverage", "SonarQube Quality Gate: PASSED (Hạng A)")
        ],
        "image": "docs/screenshots/06_app_home.png",
        "caption": "Giao diện trang chủ ứng dụng PetCare Hub vận hành thực tế tại http://localhost:5000",
        "notes": "Chào thầy/cô và các bạn. Hôm nay nhóm em xin trình bày tổng quan về dự án Hệ thống Quản lý & Chăm sóc Thú cưng (PetCare Hub) phát triển trên nền tảng .NET 8 và SQL Server 2022, kết hợp triển khai quy trình DevOps CI/CD tự động hóa hoàn toàn với Jenkins, SonarQube, Docker Compose, SSH Remote Deploy và giám sát thời gian thực bằng Prometheus & Grafana."
    },
    {
        "num": 2,
        "section": "CHƯƠNG 1: TỔNG QUAN",
        "title": "BỐI CẢNH THỰC TẾ, BÀI TOÁN & MỤC TIÊU DỰ ÁN",
        "subtitle": "Giải quyết đồng thời bài toán số hóa nghiệp vụ thú y và tự động hóa quy trình phát triển - vận hành phần mềm",
        "bullets": [
            "Hạn chế của quản lý thủ công: Sổ sách/Excel rời rạc gây nhầm lịch tiêm phòng, trùng giờ hẹn Spa, không kiểm soát được tồn kho khi khách đặt mua vượt số lượng thực tế.",
            "Hạn chế của triển khai phần mềm truyền thống: Build và copy file thủ công dễ xung đột môi trường (.NET SDK, SQL Server), thiếu kiểm thử tự động và không phát hiện sớm khi dịch vụ quá tải.",
            "Mục tiêu Nghiệp vụ: Xây dựng hệ thống Web đồng bộ 6 phân hệ (Xác thực OAuth2, Hồ sơ Thú cưng, Dịch vụ & Đặt lịch, Cửa hàng Pet Shop có kiểm soát tồn kho, Liên hệ, Admin Console).",
            "Mục tiêu DevOps CI/CD: Tự động hóa khép kín từ khi git push lên GitHub -> Build -> Unit Test -> SonarQube Quality Gate -> Đóng gói Docker -> Deploy Local & Server Public qua SSH -> Giám sát 24/7."
        ],
        "highlights": [
            ("Số hóa 100%", "Hồ sơ thú cưng, lịch hẹn & tồn kho"),
            ("Zero-Conflict", "Đóng gói đồng nhất bằng Docker Compose"),
            ("CI/CD Khép kín", "Tự động kiểm thử, quét lỗi & triển khai")
        ],
        "image": "docs/diagrams/03_usecase_thu_cung.png",
        "caption": "Phân tách phạm vi quản lý hồ sơ thú cưng giữa Khách hàng và Quản trị viên",
        "notes": "Slide số 2 trình bày bối cảnh và mục tiêu kép của dự án: một mặt giải quyết triệt để bài toán quản lý hồ sơ thú cưng, đặt lịch spa/khám bệnh và tồn kho cửa hàng; mặt khác áp dụng quy trình DevOps CI/CD để loại bỏ hoàn toàn rủi ro xung đột môi trường và lỗi mã nguồn khi triển khai."
    },
    {
        "num": 3,
        "section": "CHƯƠNG 2: PHÂN TÍCH HỆ THỐNG",
        "title": "PHÂN TÍCH TÁC NHÂN & BIỂU ĐỒ USE CASE TỔNG QUAN",
        "subtitle": "Phân quyền chặt chẽ theo 3 nhóm đối tượng sử dụng: Khách vãng lai (Guest), Khách hàng (Customer) và Quản trị viên (Admin)",
        "bullets": [
            "Khách vãng lai (Guest): Xem danh mục gói dịch vụ Spa & Khám, tìm kiếm/lọc sản phẩm theo 4 danh mục (Thức ăn, Đồ chơi, Phụ kiện, Sức khỏe), gửi liên hệ tư vấn, Đăng ký/Đăng nhập.",
            "Khách hàng (Customer): Quản lý danh sách thú cưng thuộc sở hữu cá nhân, đặt lịch chăm sóc chỉ cho thú cưng của mình, xem lịch sử & hủy lịch hẹn, thêm giỏ hàng và đặt hàng thanh toán.",
            "Quản trị viên (Admin): Truy cập Bảng Quản Trị (Admin Console) theo dõi thống kê tổng quan và doanh thu hợp nhất; thực hiện toàn quyền CRUD đối với Thú cưng, Lịch hẹn, Dịch vụ và Sản phẩm.",
            "Cơ chế kế thừa quyền hạn: Admin kế thừa toàn bộ quyền của Customer; Customer kế thừa toàn bộ quyền tra cứu công khai của Guest."
        ],
        "highlights": [
            ("3 Actors", "Guest • Customer • Admin"),
            ("6 Phân hệ", "Đáp ứng trọn vẹn quy trình Pet Shop & Spa"),
            ("RBAC + OAuth2", "Phân quyền theo vai trò & chủ sở hữu")
        ],
        "image": "docs/diagrams/01_usecase_tong_quan.png",
        "caption": "Biểu đồ Use Case tổng quan của Hệ thống Quản lý Thú cưng PetCare Hub",
        "notes": "Hệ thống được thiết kế cho 3 nhóm tác nhân chính: Khách vãng lai, Khách hàng đã đăng nhập và Quản trị viên. Điểm quan trọng trong thiết kế là sự cô lập dữ liệu cá nhân: khách hàng chỉ nhìn thấy và đặt lịch cho thú cưng của chính mình, trong khi Admin quản lý toàn bộ dữ liệu hệ thống."
    },
    {
        "num": 4,
        "section": "CHƯƠNG 3: KIẾN TRÚC & CÔNG NGHỆ",
        "title": "KIẾN TRÚC PHÂN TẦNG & STACK CÔNG NGHỆ SỬ DỤNG",
        "subtitle": "Sự kết hợp đồng bộ giữa ASP.NET Core 8.0, Vanilla JS SPA, SQL Server 2022 và bộ công cụ DevOps chuẩn công nghiệp",
        "bullets": [
            "Tầng Giao diện (Frontend SPA): HTML5, CSS3 Custom Variables (chuyển đổi tức thì Light/Dark Mode), Vanilla JavaScript ES6+ (wwwroot/js/app.js) giao tiếp qua Fetch REST API.",
            "Tầng Nghiệp vụ (Backend API): ASP.NET Core 8.0 Web API gồm 7 Controllers, cấu hình ReferenceHandler.IgnoreCycles chống vòng lặp JSON, tích hợp Swagger UI (/swagger).",
            "Tầng Dữ liệu Hybrid (EF Core 8.0.8): Kết nối chính tới Microsoft SQL Server 2022 Container (EnableRetryOnFailure), kèm cơ chế kiểm tra kết nối 3 giây tự động Fallback sang In-Memory DB khi chạy độc lập.",
            "Tầng Kiểm thử, CI/CD & Giám sát: GitHub, Jenkins LTS (Custom Image), xUnit + Coverlet OpenCover, SonarQube 26.x + PostgreSQL 15, Docker Compose, OpenSSH, Prometheus, Grafana, cAdvisor, Node Exporter."
        ],
        "highlights": [
            ("ASP.NET Core 8.0", "Hiệu năng cao, hỗ trợ chuẩn LTS"),
            ("SQL Server 2022", "Kèm cơ chế Auto-Fallback 3s thông minh"),
            ("Zero Conflict", "Đã kiểm toán tương thích toàn bộ thư viện")
        ],
        "image": "docs/diagrams/06_usecase_quan_tri_admin.png",
        "caption": "Các chức năng điều phối trung tâm trong phân hệ Quản trị (Admin Dashboard)",
        "notes": "Về kiến trúc kỹ thuật, dự án áp dụng mô hình RESTful Web API trên .NET 8 kết hợp giao diện SPA. Đặc biệt ở tầng cơ sở dữ liệu, hệ thống sử dụng SQL Server 2022 làm CSDL chính trong Docker và có cơ chế kiểm tra kết nối 3 giây khi khởi động để tự động chuyển sang In-Memory nếu chạy trên máy không bật SQL Server."
    },
    {
        "num": 5,
        "section": "CHƯƠNG 4: CƠ SỞ DỮ LIỆU",
        "title": "THIẾT KẾ CƠ SỞ DỮ LIỆU SQL SERVER 2022 (7 BẢNG THỰC THỂ)",
        "subtitle": "Xây dựng theo phương pháp EF Core Code-First (PetDbContext) với đầy đủ ràng buộc khóa ngoại và dữ liệu mẫu tự động",
        "bullets": [
            "1. Bảng Users: Lưu tài khoản Admin & Customer (Id, FullName, Email, PasswordHash, Role, Phone, Address, AvatarUrl, OAuthProvider, CreatedAt).",
            "2. Bảng Pets: Hồ sơ thú cưng (Id, Name, Species, Breed, AgeYears, WeightKg, Gender, HealthNotes, ImageUrl, OwnerId -> FK Users).",
            "3. Bảng Services: Danh mục gói dịch vụ Spa/Khám/Khách sạn (Id, Name, Category, Price, DurationMinutes, Description, ImageUrl, IsActive hỗ trợ Soft-Delete).",
            "4. Bảng Appointments: Lịch hẹn dịch vụ liên kết PetId, ServiceId, CustomerId theo vòng đời trạng thái: Pending -> Confirmed -> Completed / Cancelled.",
            "5. Bảng Products, 6. ProductOrders & 7. ContactMessages: Quản lý sản phẩm, đơn hàng thanh toán có khấu trừ tồn kho (StockQuantity) và tin nhắn liên hệ."
        ],
        "highlights": [
            ("7 Bảng Thực thể", "Users, Pets, Services, Appointments, Products, Orders, Contacts"),
            ("Data Seeding", "Tự động khởi tạo schema & nạp dữ liệu mẫu"),
            ("State Machine", "Quản lý chặt chẽ vòng đời trạng thái lịch hẹn")
        ],
        "image": "docs/diagrams/16_state_lich_hen.png",
        "caption": "Biểu đồ trạng thái (State Machine) vòng đời của Lịch hẹn dịch vụ",
        "notes": "Cơ sở dữ liệu PetManagementDb gồm 7 bảng thực thể được ánh xạ qua lớp PetDbContext. Khác với bản thiết kế sơ khởi, hệ thống thực tế đã bổ sung bảng ProductOrders lưu đơn hàng thanh toán thực tế, gắn với việc kiểm tra và khấu trừ số lượng tồn kho trong bảng Products."
    },
    {
        "num": 6,
        "section": "CHƯƠNG 5: MODULE CHỨC NĂNG (PHẦN 1)",
        "title": "MODULE XÁC THỰC OAUTH2 & QUẢN LÝ HỒ SƠ THÚ CƯNG",
        "subtitle": "Xác thực đa phương thức có đồng bộ phiên tự động và quản lý CRUD thú cưng toàn diện",
        "bullets": [
            "Xác thực Hybrid (AuthApiController - /api/auth): Hỗ trợ đăng ký, đăng nhập mật khẩu truyền thống, cấp phát Token kèm HTTP-Only Secure Cookie và xác thực Google ID Token qua Google.Apis.Auth.",
            "Đồng bộ phiên thông minh (POST /api/auth/sync): Tự động đồng bộ tài khoản đang lưu trên trình duyệt (localStorage) vào bảng dbo.Users của SQL Server, loại bỏ hoàn toàn lỗi xung đột khóa ngoại FK_Pets_Users_OwnerId.",
            "Tìm kiếm & Lọc Thú cưng (GET /api/pets): Phân trang tại tầng DB, tìm kiếm theo Tên/Giống/Ghi chú sức khỏe, lọc theo 4 loài (Chó, Mèo, Thỏ, Khác) và sắp xếp theo tuổi/cân nặng.",
            "Xóa Thú cưng linh hoạt (DELETE /api/pets/{id} & DELETE /api/pets/custom): Cho phép xóa trực tiếp trên từng thẻ thú cưng, xóa trong Modal sửa hoặc xóa nhanh toàn bộ thú cưng mới nhập kèm tự động dọn sạch lịch hẹn liên quan."
        ],
        "highlights": [
            ("Google OAuth 2.0", "Xác thực chữ ký số JWT chuẩn OpenID"),
            ("Session Sync", "Tự động đồng bộ UserId với SQL Server"),
            ("Cascade Delete", "Hỗ trợ xóa đơn lẻ & xóa hàng loạt Pet đã nhập")
        ],
        "image": "docs/diagrams/12_sequence_google_oauth.png",
        "caption": "Biểu đồ tuần tự (Sequence Diagram) luồng xác thực Google OAuth 2.0",
        "notes": "Ở phân hệ Xác thực và Quản lý Thú cưng, nhóm đã giải quyết hai bài toán thực tế rất quan trọng khi chạy với SQL Server thật: thứ nhất là API POST /api/auth/sync giúp đồng bộ tài khoản từ trình duyệt vào bảng Users; thứ hai là tính năng xóa thú cưng đơn lẻ và xóa hàng loạt pet mới nhập có tự động dọn các lịch hẹn liên quan."
    },
    {
        "num": 7,
        "section": "CHƯƠNG 5: MODULE CHỨC NĂNG (PHẦN 2)",
        "title": "ĐẶT LỊCH DỊCH VỤ, CỬA HÀNG PET SHOP & ADMIN CONSOLE",
        "subtitle": "Kiểm soát chặt chẽ quyền đặt lịch theo chủ nuôi, kiểm tra tồn kho khi thanh toán và thống kê doanh thu thời gian thực",
        "bullets": [
            "Đặt lịch thông minh (AppointmentsApiController): Khi khách hàng mở form Đặt lịch, hệ thống chỉ hiển thị danh sách thú cưng thuộc sở hữu của khách hàng đó; nếu chưa có thú cưng sẽ tự động nhắc tạo hồ sơ trước.",
            "Thanh toán kiểm soát tồn kho (POST /api/products/checkout): Kiểm tra điều kiện StockQuantity >= qty cho từng mặt hàng trong giỏ, trả về cảnh báo nếu vượt tồn kho, trừ số lượng tồn kho thực tế và khóa nút mua khi hết hàng.",
            "Bảng Quản trị Hệ thống (DashboardApiController - /api/dashboard/stats): Hợp nhất thời gian thực doanh thu từ các lịch hẹn đã hoàn thành (Appointments Completed) và doanh thu đơn hàng (ProductOrders).",
            "Chuẩn hóa tài liệu OpenAPI (Swagger UI): Toàn bộ 7 API Controllers được đặc tả trực quan tại http://localhost:5000/swagger giúp kiểm thử nhanh mọi endpoint."
        ],
        "highlights": [
            ("Stock Check", "Kiểm tra & trừ tồn kho thực tế khi Checkout"),
            ("Unified Revenue", "Tổng hợp doanh thu Dịch vụ + Bán hàng"),
            ("Swagger OpenAPI", "Tài liệu hóa toàn bộ RESTful Endpoints")
        ],
        "image": "docs/screenshots/07_app_swagger.png",
        "caption": "Giao diện Swagger UI đặc tả đầy đủ các nhóm RESTful API tại http://localhost:5000/swagger",
        "notes": "Đối với phân hệ Đặt lịch và Cửa hàng, hệ thống kiểm soát chặt chẽ nghiệp vụ: khách hàng chỉ đặt lịch cho thú cưng của mình, và khi thanh toán giỏ hàng, Backend kiểm tra tồn kho thực tế trước khi trừ số lượng và ghi nhận doanh thu lên Bảng quản trị Admin."
    },
    {
        "num": 8,
        "section": "CHƯƠNG 6: ĐÓNG GÓI DOCKER",
        "title": "KIẾN TRÚC CONTAINER HÓA & QUY HOẠCH 3 CỤM DOCKER COMPOSE",
        "subtitle": "Vận hành đồng bộ 9 Containers trên mạng ảo bridge chung 'petnet' chỉ với một kịch bản khởi chạy",
        "bullets": [
            "Kỹ thuật Multi-stage Dockerfile: Tách biệt giai đoạn biên dịch (mcr.microsoft.com/dotnet/sdk:8.0) và giai đoạn chạy thực tế (mcr.microsoft.com/dotnet/aspnet:8.0), giảm hơn 65% dung lượng image.",
            "Cụm 1 - Ứng dụng (docker-compose.yml): Gồm petmanagement_webapp (cổng 5000:80) và petmanagement_sqlserver (SQL Server 2022 cổng 1433, lưu trữ bền vững trên volume sqlserver_data, có healthcheck sqlcmd).",
            "Cụm 2 - CI/CD (docker-compose.ci.yml): Gồm petmanagement_jenkins (cổng 8090:8080), petmanagement_sonarqube (cổng 9000) và petmanagement_sonar_db (PostgreSQL 15).",
            "Cụm 3 - Giám sát (docker-compose.monitoring.yml): Gồm petmanagement_prometheus (cổng 9091), petmanagement_grafana (cổng 3001), petmanagement_cadvisor (cổng 8082) và petmanagement_node_exporter (cổng 9101)."
        ],
        "highlights": [
            ("3 Cụm Compose", "App Cluster • CI/CD Cluster • Monitoring Cluster"),
            ("Mạng ảo petnet", "Kết nối nội bộ theo tên service chuẩn RFC"),
            ("1-Click Start", "Khởi chạy toàn bộ qua .\\ci\\scripts\\start-cicd.ps1")
        ],
        "image": "docs/diagrams/15_deployment_docker.png",
        "caption": "Biểu đồ Triển khai (Deployment Diagram) giữa Trình duyệt, Web App Container và SQL Server 2022 Container",
        "notes": "Bước sang phần triển khai DevOps, toàn bộ hệ thống gồm 9 containers được quy hoạch thành 3 file Docker Compose tách biệt theo chức năng nhưng kết nối chung trên mạng bridge petnet. Dữ liệu SQL Server 2022 được lưu trữ bền vững trên Docker Volume kèm cơ chế healthcheck tự động."
    },
    {
        "num": 9,
        "section": "CHƯƠNG 6: CÀI ĐẶT JENKINS",
        "title": "XÂY DỰNG CUSTOM JENKINS IMAGE & CẤU HÌNH TỰ ĐỘNG",
        "subtitle": "Tích hợp sẵn .NET 8 SDK, SonarScanner, Docker CLI và OpenSSH Client bên trong container Jenkins",
        "bullets": [
            "Tùy biến Dockerfile riêng cho Jenkins (ci/jenkins/Dockerfile): Kế thừa từ jenkins/jenkins:lts-jdk17, cài đặt sẵn .NET 8.0 SDK, các thư viện hệ thống Debian (libicu, libssl3) và công cụ toàn cục dotnet-sonarscanner.",
            "Kỹ thuật Docker-outside-of-Docker (DooD): Cài đặt Docker CE CLI + Docker Compose Plugin và mount socket /var/run/docker.sock từ máy chủ Host, cho phép Jenkins trực tiếp đóng gói image và khởi chạy container.",
            "Cài đặt Plugin tự động (ci/jenkins/plugins.txt): Tự động nạp các plugin cốt lõi gồm git, workflow-aggregator, docker-workflow, sonar, ssh-agent, credentials-binding.",
            "Khởi tạo sẵn 2 Pipeline Jobs (init-jenkins.groovy): Tự động cấu hình kết nối SonarQube Server, Token xác thực và khởi tạo 2 luồng Pipeline: PetManagement-Local & PetManagement-Remote."
        ],
        "highlights": [
            ("Custom Image", "Jenkins LTS + .NET 8 SDK + SonarScanner"),
            ("DooD Socket", "Điều khiển trực tiếp Docker Engine qua docker.sock"),
            ("2 Pipelines", "PetManagement-Local & PetManagement-Remote")
        ],
        "image": "docs/screenshots/01_jenkins_dashboard.png",
        "caption": "Giao diện Jenkins Dashboard tại http://localhost:8090 với 2 Pipeline đều đạt trạng thái thành công",
        "notes": "Để Jenkins có thể biên dịch code C# .NET 8, quét SonarQube và chạy lệnh Docker, nhóm đã xây dựng một Dockerfile tùy biến riêng cho Jenkins và áp dụng kỹ thuật Docker-outside-of-Docker thông qua việc chia sẻ socket /var/run/docker.sock."
    },
    {
        "num": 10,
        "section": "CHƯƠNG 6: PIPELINE CI/CD (JENKINSFILE)",
        "title": "LUỒNG HOẠT ĐỘNG PIPELINE 8 STAGES & KIỂM CHỨNG THỰC TẾ",
        "subtitle": "Tự động hóa từ lúc kéo code GitHub, chạy Unit Test, kiểm định Quality Gate đến khi Deploy & Health Check",
        "bullets": [
            "Stage 1 (Checkout) & Stage 2 (Restore & Build): Kéo mã nguồn mới nhất từ GitHub, in mã Commit SHA và biên dịch dự án ở chế độ Release.",
            "Stage 3 (Unit Test) & Stage 4 (SonarQube Analysis): Chạy bộ kiểm thử xUnit xuất báo cáo độ phủ OpenCover XML, sau đó quét mã nguồn tĩnh và đẩy kết quả sang SonarQube.",
            "Stage 5 (Quality Gate - Chốt chặn chất lượng): Lệnh waitForQualityGate abortPipeline: true tự động dừng ngay pipeline nếu code không đạt chuẩn (như minh chứng thực tế ở Build #4 và Build #5).",
            "Stage 6 (Docker Build), Stage 7 (Deploy) & Stage 8 (Health Check): Khi vượt qua Quality Gate (như Build #6), Jenkins đóng gói image mới, chạy docker compose up -d và gọi /health xác nhận HTTP 200 OK."
        ],
        "highlights": [
            ("8 Stages", "Tự động hóa 100% từ GitHub tới Production"),
            ("Auto-Abort", "Tự động chặn đứng bản build lỗi ở Stage 3 & Stage 5"),
            ("Build #6 Green", "Hoàn tất toàn bộ 8/8 stages sau khi đạt chuẩn")
        ],
        "image": "docs/screenshots/02_jenkins_local_pipeline.png",
        "caption": "Giao diện Stage View của Pipeline PetManagement-Local hiển thị đầy đủ 8 stages và trạng thái Quality Gate Passed",
        "notes": "Đây là luồng hoạt động 8 bước trong Jenkinsfile. Trong quá trình phát triển, hệ thống đã chứng minh hiệu quả thực tế: khi code mới thiếu unit test hoặc có lỗi logic, Pipeline lập tức chặn lại ở Stage 3 hoặc Stage 5; chỉ khi toàn bộ test và SonarQube đạt chuẩn như ở bản Build mới nhất, Jenkins mới tiến hành đóng gói Docker và triển khai."
    },
    {
        "num": 11,
        "section": "CHƯƠNG 6: TÍCH HỢP SONARQUBE",
        "title": "PHÂN TÍCH MÃ NGUỒN TĨNH & KIỂM SOÁT SONARQUBE QUALITY GATE",
        "subtitle": "Tích hợp hai chiều giữa Jenkins và SonarQube qua Token xác thực & Webhook tự động",
        "bullets": [
            "Cơ chế giao tiếp nội bộ chuẩn RFC: Jenkins đẩy dữ liệu phân tích tới http://sonarqube:9000 kèm báo cáo độ phủ tests/PetManagement.Tests/coverage.opencover.xml; SonarQube trả kết quả về http://jenkins:8080/sonarqube-webhook/.",
            "Độ phủ kiểm thử tự động vượt trội (Code Coverage): Bộ kiểm thử xUnit bao phủ toàn bộ 7 API Controllers giúp độ phủ tổng thể đạt 91.2% (độ phủ trên code mới đạt 91.7%, vượt xa ngưỡng yêu cầu 80%).",
            "Đạt xếp hạng A tuyệt đối trên cả 4 trụ cột: Security Rating A (0 Vulnerabilities), Reliability Rating A (0 Bugs), Maintainability Rating A (0 Code Smells), Security Review Rating A (100%).",
            "Tỷ lệ trùng lặp mã nguồn (Duplications): Đạt mức tối ưu 0.0% (< 3%), trạng thái Quality Gate chính thức đạt PASSED."
        ],
        "highlights": [
            ("Quality Gate", "PASSED (100% đạt chuẩn kiểm định)"),
            ("91.2% Coverage", "Vượt ngưỡng 80% của chuẩn Clean as You Code"),
            ("4 Hạng A", "0 Bugs • 0 Vulnerabilities • 0.0% Duplications")
        ],
        "image": "docs/screenshots/05_sonarqube_dashboard.png",
        "caption": "Kết quả phân tích chất lượng mã nguồn trên SonarQube Dashboard tại http://localhost:9000",
        "notes": "Slide 11 trình bày kết quả tích hợp SonarQube vào Jenkins. Nhờ giao tiếp hai chiều qua Webhook và bộ kiểm thử xUnit + Coverlet, dự án đạt trạng thái Quality Gate: PASSED với độ phủ mã nguồn lên tới 91.2%, 0 lỗi bảo mật, 0 bug và đạt hạng A trên tất cả các chỉ số."
    },
    {
        "num": 12,
        "section": "CHƯƠNG 6: TRIỂN KHAI TỪ XA QUA SSH",
        "title": "TỰ ĐỘNG DEPLOY LÊN SERVER PUBLIC QUA SSH (JENKINSFILE.REMOTE)",
        "subtitle": "Cấu hình Pipeline thứ hai triển khai trực tiếp ứng dụng lên máy chủ từ xa và kiểm tra qua địa chỉ Public",
        "bullets": [
            "Thiết kế Pipeline PetManagement-Remote (Jenkinsfile.remote): Giữ nguyên 6 stage kiểm thử và phân tích SonarQube đầu tiên, nâng cấp Stage 7 và Stage 8 để triển khai qua giao thức SSH.",
            "Tham số hóa máy chủ đích (Build with Parameters): Cho phép nhập linh hoạt SERVER_HOST (IP hoặc Domain public của VPS/Cloud Server), SERVER_USER (tài khoản SSH), DEPLOY_DIR (/opt/petmanagement).",
            "Quy trình 4 bước tự động qua SSH Private Key (prod-server-ssh): (1) Tạo thư mục từ xa qua ssh mkdir -p; (2) Sao chép docker-compose.yml lên server qua scp; (3) Truyền trực tiếp Docker Image qua đường ống nén docker save | gzip | ssh 'gunzip | docker load'; (4) Thực thi từ xa lệnh docker compose up -d.",
            "Xác nhận hoạt động qua IP Public (Stage 8 - Public Health Check): Jenkins tự động truy vấn http://${SERVER_HOST}:5000/health để đảm bảo phần mềm truy cập thành công từ Internet."
        ],
        "highlights": [
            ("SSH + SCP", "Bảo mật bằng khóa bất đối xứng Private Key"),
            ("Direct Stream", "Truyền thẳng image qua docker save | ssh docker load"),
            ("Public Verify", "Tự động kiểm tra http://PUBLIC_IP:5000/health")
        ],
        "image": "docs/screenshots/04_jenkins_remote_pipeline.png",
        "caption": "Kết quả thực thi Pipeline PetManagement-Remote hoàn tất triển khai tự động qua SSH",
        "notes": "Đáp ứng yêu cầu tự động deploy lên server public qua SSH, nhóm đã xây dựng pipeline thứ hai trong file Jenkinsfile.remote. Điểm đặc biệt là quy trình sử dụng đường ống nén docker save kết hợp ssh docker load để truyền trực tiếp image vừa build sang máy chủ đích, khởi chạy docker compose và kiểm tra trực tiếp địa chỉ public của server."
    },
    {
        "num": 13,
        "section": "CHƯƠNG 7: GIÁM SÁT PROMETHEUS",
        "title": "GIÁM SÁT HỆ THỐNG ĐA TẦNG VỚI PROMETHEUS (4/4 TARGETS UP)",
        "subtitle": "Thu thập chỉ số vận hành thời gian thực từ Ứng dụng .NET 8, Docker Containers và Máy chủ Host",
        "bullets": [
            "1. Tầng Ứng dụng (petmanagement_webapp): Tích hợp thư viện prometheus-net.AspNetCore trong Program.cs (app.UseHttpMetrics() và app.MapMetrics()), xuất dữ liệu chuẩn OpenMetrics tại http://localhost:5000/metrics.",
            "2. Tầng Container (petmanagement_cadvisor - cổng 8082): Sử dụng Google cAdvisor đo lường mức sử dụng CPU, bộ nhớ RAM, băng thông mạng và I/O ổ đĩa của từng container trong thời gian thực.",
            "3. Tầng Máy chủ (petmanagement_node_exporter - cổng 9101): Thu thập thông số tài nguyên phần cứng và hệ điều hành của máy chủ Host.",
            "4. Máy chủ Prometheus (http://localhost:9091/targets): Cấu hình scrape_interval 10s-15s trong monitoring/prometheus/prometheus.yml; toàn bộ 4/4 Targets đều hoạt động ổn định ở trạng thái UP."
        ],
        "highlights": [
            ("4/4 Targets UP", "webapp • cadvisor • node_exporter • prometheus"),
            ("10s Interval", "Chu kỳ thu thập metrics ứng dụng thời gian thực"),
            ("/metrics & /health", "Tích hợp trực tiếp trong ASP.NET Core 8.0")
        ],
        "image": "docs/screenshots/08_prometheus_targets.png",
        "caption": "Giao diện Prometheus Status -> Targets tại http://localhost:9091/targets xác nhận cả 4/4 điểm thu thập đều UP",
        "notes": "Sau khi ứng dụng được triển khai, hệ thống giám sát Prometheus sẽ liên tục thu thập thông số ở cả 3 tầng: tầng ứng dụng .NET 8 thông qua endpoint /metrics, tầng container qua cAdvisor và tầng máy chủ qua Node Exporter. Trên giao diện Prometheus Targets, cả 4 trên 4 mục tiêu đều đạt trạng thái UP màu xanh."
    },
    {
        "num": 14,
        "section": "CHƯƠNG 7: TRỰC QUAN HÓA GRAFANA",
        "title": "BẢNG ĐIỀU KHIỂN GRAFANA AUTO-PROVISIONING (8 BIỂU ĐỒ)",
        "subtitle": "Tự động nạp sẵn Datasource và Dashboard giám sát toàn diện tại http://localhost:3001",
        "bullets": [
            "Cơ chế Auto-Provisioning (monitoring/grafana/provisioning/): Tự động kết nối nguồn dữ liệu Prometheus (http://prometheus:9090) và nạp sẵn Dashboard ngay khi container Grafana khởi động.",
            "4 Biểu đồ Trạng thái nhanh (Stat Panels): (1) Trạng thái Ứng dụng PetManagement (UP); (2) Tổng số HTTP Requests đã xử lý; (3) Tổng số Containers đang hoạt động; (4) Dung lượng RAM tiêu thụ của tiến trình .NET 8.",
            "4 Biểu đồ Chuỗi thời gian (Time-Series Panels): (5) Lưu lượng HTTP Requests/giây phân loại theo mã trạng thái (2xx, 4xx, 5xx); (6) Độ trễ phản hồi phân vị thứ 95 (P95 Latency); (7) Mức tải CPU theo thời gian thực; (8) Lưu lượng mạng Nhận/Gửi (Network I/O).",
            "Giá trị vận hành: Giúp đội ngũ quản trị phát hiện tức thì các điểm nghẽn hiệu năng, các API có độ trễ cao hoặc sự cố tăng đột biến lỗi HTTP 5xx."
        ],
        "highlights": [
            ("8 Panels", "4 Stat Panels + 4 Time-Series Charts"),
            ("Auto-Provisioned", "Tự động nạp cấu hình JSON không cần cài tay"),
            ("Real-time P95", "Theo dõi độ trễ API, lưu lượng HTTP, CPU & RAM")
        ],
        "image": "docs/screenshots/09_grafana_dashboard.png",
        "caption": "Giao diện Grafana Dashboard tại http://localhost:3001 hiển thị trực quan 8 biểu đồ giám sát hệ thống",
        "notes": "Từ dữ liệu của Prometheus, Grafana được cấu hình Auto-Provisioning để tự động hiển thị bảng điều khiển gồm 8 biểu đồ trực quan tại cổng 3001. Quản trị viên có thể theo dõi theo thời gian thực trạng thái sống của dịch vụ, tốc độ request trên giây, độ trễ P95 cũng như mức tiêu thụ CPU, RAM và băng thông mạng."
    },
    {
        "num": 15,
        "section": "CHƯƠNG 8: TỔNG KẾT & HƯỚNG PHÁT TRIỂN",
        "title": "TỔNG KẾT KẾT QUẢ ĐẠT ĐƯỢC & ĐỊNH HƯỚNG PHÁT TRIỂN",
        "subtitle": "Hoàn thành trọn vẹn hệ thống phần mềm Quản lý Thú cưng gắn liền với quy trình DevOps CI/CD hiện đại",
        "bullets": [
            "Kết quả phần mềm: Hoàn thiện ứng dụng Web PetCare Hub (.NET 8 + SQL Server 2022 + SPA) với 7 bảng dữ liệu chuẩn hóa, xác thực Google OAuth2 có đồng bộ phiên, xóa thú cưng linh hoạt và thanh toán kiểm soát tồn kho thực tế.",
            "Kết quả CI/CD & Đảm bảo chất lượng: Vận hành ổn định 2 Pipeline trên Jenkins (Local & Remote SSH), tích hợp bộ kiểm thử xUnit đạt độ phủ 91.2% và vượt qua SonarQube Quality Gate với xếp hạng A tuyệt đối.",
            "Kết quả Đóng gói & Giám sát: Quy hoạch chuẩn 9 Docker Containers trên 3 cụm Compose; giám sát 24/7 với Prometheus (4/4 Targets UP) và Grafana Dashboard 8 biểu đồ.",
            "Hướng phát triển tương lai: (1) Tích hợp cổng thanh toán trực tuyến VNPay/VietQR tự động đối soát Webhook; (2) Tích hợp SignalR & gửi Email nhắc lịch tiêm phòng tự động; (3) Mở rộng cảnh báo Prometheus Alertmanager qua Telegram/Slack và triển khai trên cụm Kubernetes (K8s)."
        ],
        "highlights": [
            ("100% Hoàn thành", "Đáp ứng đầy đủ mọi yêu cầu Nghiệp vụ & CI/CD"),
            ("Sẵn sàng Mở rộng", "Hướng tới tích hợp VietQR, SignalR & Kubernetes"),
            ("Cảm ơn Thầy/Cô!", "Nhóm sẵn sàng thực hiện Demo trực tiếp & Vấn đáp")
        ],
        "image": "docs/screenshots/03_jenkins_local_console.png",
        "caption": "Nhật ký Console Output xác nhận toàn bộ quy trình CI/CD thực thi thành công",
        "notes": "Tổng kết lại, dự án đã hoàn thành toàn diện cả về mặt nghiệp vụ phần mềm lẫn hạ tầng tự động hóa CI/CD và giám sát hệ thống. Toàn bộ mã nguồn, báo cáo tổng kết và kịch bản CI/CD đều đã được đồng bộ đầy đủ trên GitHub. Em xin cảm ơn thầy/cô đã lắng nghe và xin phép chuyển sang phần Demo trực tiếp trên hệ thống!"
    }
]


def generate_markdown_slides():
    lines = [
        "# BỘ SLIDE THUYẾT TRÌNH TỔNG QUAN DỰ ÁN & CI/CD (15 SLIDES)",
        "**Đề tài**: Hệ thống Quản lý & Chăm sóc Thú cưng (PetCare Hub - PetManagement) kết hợp Triển khai Tự động CI/CD & Giám sát Hệ thống",
        "- **File PowerPoint (.pptx)**: `Slide_Thuyet_Trinh_Du_An_PetManagement_CICD.pptx`",
        "- **File Web Slide tương tác (HTML)**: `Slide_Thuyet_Trinh_Du_An.html` (hoặc `http://localhost:5000/slides.html`)",
        "\n---\n"
    ]
    for s in SLIDES_DATA:
        lines.append(f"## Slide {s['num']:02d}/15: {s['title']}")
        lines.append(f"**Phân mục**: `{s['section']}`  ")
        lines.append(f"*{s['subtitle']}*\n")
        lines.append("### Nội dung chính trên Slide:")
        for b in s["bullets"]:
            lines.append(f"- {b}")
        lines.append("\n### Điểm nhấn (Key Metrics):")
        lines.append("| " + " | ".join([f"**{h[0]}**: {h[1]}" for h in s["highlights"]]) + " |")
        lines.append("| " + " | ".join(["---"] * len(s["highlights"])) + " |")
        lines.append(f"\n![{s['caption']}]({s['image']})")
        lines.append(f"*{s['caption']}*\n")
        lines.append(f"> **Lời thuyết trình mẫu (Speaker Notes):**  \n> \"{s['notes']}\"\n")
        lines.append("---\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[OK] Đã tạo kịch bản Slide Markdown: {OUT_MD}")


def generate_html_slides():
    slide_sections = []
    for idx, s in enumerate(SLIDES_DATA):
        abs_img = os.path.join(ROOT_DIR, s["image"].replace("/", os.sep))
        img_src = s["image"]
        if os.path.exists(abs_img):
            with open(abs_img, "rb") as img_f:
                b64 = base64.b64encode(img_f.read()).decode("ascii")
                img_src = f"data:image/png;base64,{b64}"

        bullets_html = "".join([f"<li>{escape(b)}</li>" for b in s["bullets"]])
        badges_html = "".join([
            f'<div class="metric-card"><div class="metric-val">{escape(h[0])}</div><div class="metric-lbl">{escape(h[1])}</div></div>'
            for h in s["highlights"]
        ])
        active_cls = " active" if idx == 0 else ""
        slide_sections.append(f"""
        <section class="slide{active_cls}" data-index="{idx}">
          <div class="slide-header">
            <div class="slide-tag">{escape(s['section'])}</div>
            <div class="slide-num">Slide {s['num']:02d} / {len(SLIDES_DATA)}</div>
          </div>
          <h1 class="slide-title">{escape(s['title'])}</h1>
          <p class="slide-subtitle">{escape(s['subtitle'])}</p>
          <div class="slide-body">
            <div class="slide-left">
              <ul class="slide-bullets">{bullets_html}</ul>
              <div class="metrics-row">{badges_html}</div>
            </div>
            <div class="slide-right">
              <div class="img-frame">
                <img src="{img_src}" alt="{escape(s['caption'])}">
              </div>
              <div class="img-caption">{escape(s['caption'])}</div>
            </div>
          </div>
          <div class="speaker-notes">
            <strong>Gợi ý lời thuyết trình:</strong> "{escape(s['notes'])}"
          </div>
        </section>
        """)

    html_doc = f"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Slide Thuyết Trình Dự Án PetCare Hub & CI/CD (15 Slides)</title>
  <style>
    :root {{
      --bg-dark: #0b1120;
      --bg-card: #131c31;
      --primary: #10b981;
      --accent: #38bdf8;
      --text-main: #f8fafc;
      --text-muted: #94a3b8;
      --border: rgba(148, 163, 184, 0.18);
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
      background: var(--bg-dark);
      color: var(--text-main);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }}
    .deck-container {{
      flex: 1;
      position: relative;
      width: 100%;
      max-width: 1520px;
      margin: 0 auto;
      padding: 22px 36px 10px;
      display: flex;
    }}
    .slide {{
      display: none;
      flex-direction: column;
      width: 100%;
      height: 100%;
      background: linear-gradient(145deg, #111827 0%, #0f172a 100%);
      border: 1px solid var(--border);
      border-radius: 18px;
      padding: 26px 34px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.55);
    }}
    .slide.active {{ display: flex; }}
    .slide-header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 10px;
    }}
    .slide-tag {{
      background: rgba(16, 185, 129, 0.15);
      color: var(--primary);
      border: 1px solid rgba(16, 185, 129, 0.35);
      padding: 4px 14px;
      border-radius: 999px;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.05em;
    }}
    .slide-num {{
      color: var(--accent);
      font-weight: 700;
      font-size: 0.9rem;
    }}
    .slide-title {{
      font-size: 1.72rem;
      font-weight: 800;
      color: #ffffff;
      margin-bottom: 6px;
      line-height: 1.25;
    }}
    .slide-subtitle {{
      font-size: 0.98rem;
      color: var(--accent);
      margin-bottom: 18px;
      font-weight: 500;
    }}
    .slide-body {{
      display: grid;
      grid-template-columns: 1.18fr 0.95fr;
      gap: 26px;
      flex: 1;
      min-height: 0;
      align-items: center;
    }}
    .slide-left {{
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
      gap: 14px;
    }}
    .slide-bullets {{
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 11px;
    }}
    .slide-bullets li {{
      position: relative;
      padding: 10px 14px 10px 34px;
      background: rgba(30, 41, 59, 0.55);
      border-left: 4px solid var(--primary);
      border-radius: 8px;
      font-size: 0.93rem;
      line-height: 1.48;
      color: #e2e8f0;
    }}
    .slide-bullets li::before {{
      content: "✔";
      position: absolute;
      left: 12px;
      top: 10px;
      color: var(--primary);
      font-weight: bold;
    }}
    .metrics-row {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 12px;
      margin-top: auto;
    }}
    .metric-card {{
      background: rgba(15, 23, 42, 0.85);
      border: 1px solid rgba(56, 189, 248, 0.28);
      border-radius: 10px;
      padding: 10px 12px;
      text-align: center;
    }}
    .metric-val {{
      font-size: 1.05rem;
      font-weight: 800;
      color: var(--primary);
      margin-bottom: 3px;
    }}
    .metric-lbl {{
      font-size: 0.78rem;
      color: var(--text-muted);
      line-height: 1.25;
    }}
    .slide-right {{
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 100%;
      background: rgba(15, 23, 42, 0.65);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 14px;
    }}
    .img-frame {{
      flex: 1;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 100%;
      min-height: 0;
      overflow: hidden;
    }}
    .img-frame img {{
      max-width: 100%;
      max-height: 360px;
      object-fit: contain;
      border-radius: 8px;
      background: #ffffff;
      padding: 4px;
    }}
    .img-caption {{
      margin-top: 8px;
      font-size: 0.8rem;
      color: var(--text-muted);
      text-align: center;
      font-style: italic;
    }}
    .speaker-notes {{
      margin-top: 14px;
      padding: 10px 16px;
      background: rgba(16, 185, 129, 0.08);
      border: 1px dashed rgba(16, 185, 129, 0.35);
      border-radius: 10px;
      font-size: 0.85rem;
      color: #cbd5e1;
      line-height: 1.45;
    }}
    .speaker-notes strong {{ color: var(--primary); }}
    .controls-bar {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1520px;
      width: 100%;
      margin: 0 auto;
      padding: 8px 36px 16px;
    }}
    .nav-btns {{ display: flex; gap: 10px; align-items: center; }}
    button.ctrl-btn {{
      background: #1e293b;
      color: #f8fafc;
      border: 1px solid var(--border);
      padding: 8px 16px;
      border-radius: 8px;
      cursor: pointer;
      font-weight: 600;
      font-size: 0.86rem;
      transition: all 0.15s;
    }}
    button.ctrl-btn:hover {{
      background: var(--primary);
      color: #0b1120;
    }}
    .progress-dots {{
      display: flex;
      gap: 6px;
    }}
    .dot {{
      width: 26px;
      height: 26px;
      border-radius: 6px;
      background: #1e293b;
      color: #94a3b8;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.75rem;
      font-weight: 700;
      cursor: pointer;
      border: 1px solid var(--border);
    }}
    .dot.active {{
      background: var(--primary);
      color: #0b1120;
    }}
    @media print {{
      body {{ height: auto; overflow: visible; background: #0b1120; }}
      .deck-container {{ display: block; padding: 0; }}
      .slide {{ display: flex !important; page-break-after: always; height: 96vh; margin-bottom: 20px; }}
      .controls-bar {{ display: none; }}
    }}
  </style>
</head>
<body>
  <div class="deck-container">
    {"".join(slide_sections)}
  </div>
  <div class="controls-bar">
    <div class="nav-btns">
      <button class="ctrl-btn" onclick="prevSlide()">⬅ Slide Trước (←)</button>
      <button class="ctrl-btn" onclick="nextSlide()">Slide Tiếp (→) ➡</button>
      <button class="ctrl-btn" onclick="toggleFullscreen()">⛶ Toàn màn hình (F)</button>
      <button class="ctrl-btn" onclick="window.print()">🖨 In / Xuất PDF</button>
    </div>
    <div class="progress-dots" id="dotsContainer"></div>
  </div>
  <script>
    let current = 0;
    const slides = document.querySelectorAll('.slide');
    const dotsContainer = document.getElementById('dotsContainer');

    slides.forEach((_, idx) => {{
      const d = document.createElement('div');
      d.className = 'dot' + (idx === 0 ? ' active' : '');
      d.textContent = idx + 1;
      d.onclick = () => showSlide(idx);
      dotsContainer.appendChild(d);
    }});

    function showSlide(n) {{
      current = (n + slides.length) % slides.length;
      slides.forEach((s, i) => s.classList.toggle('active', i === current));
      document.querySelectorAll('.dot').forEach((d, i) => d.classList.toggle('active', i === current));
    }}
    function nextSlide() {{ showSlide(current + 1); }}
    function prevSlide() {{ showSlide(current - 1); }}
    function toggleFullscreen() {{
      if (!document.fullscreenElement) document.documentElement.requestFullscreen();
      else document.exitFullscreen();
    }}
    document.addEventListener('keydown', (e) => {{
      if (e.key === 'ArrowRight' || e.key === ' ') nextSlide();
      if (e.key === 'ArrowLeft') prevSlide();
      if (e.key === 'f' || e.key === 'F') toggleFullscreen();
    }});
  </script>
</body>
</html>"""

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_doc)
    shutil.copy2(OUT_HTML, OUT_WWW_HTML)
    print(f"[OK] Đã tạo Web Slide tương tác (15 slides): {OUT_HTML} & {OUT_WWW_HTML}")


def make_pptx_shape_textbox(shape_id, name, x, y, cx, cy, paragraphs_xml, fill_hex=None, border_hex=None, radius_adj=None):
    prst = "roundRect" if radius_adj else "rect"
    av_lst = f'<a:avLst><a:gd name="adj" fmla="val {radius_adj}"/></a:avLst>' if radius_adj else "<a:avLst/>"
    fill_xml = f'<a:solidFill><a:srgbClr val="{fill_hex}"/></a:solidFill>' if fill_hex else "<a:noFill/>"
    ln_xml = f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{border_hex}"/></a:solidFill></a:ln>' if border_hex else "<a:ln><a:noFill/></a:ln>"

    return (
        f'<p:sp>'
        f'<p:nvSpPr><p:cNvPr id="{shape_id}" name="{escape(name)}"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>'
        f'<p:spPr>'
        f'<a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="{prst}">{av_lst}</a:prstGeom>'
        f'{fill_xml}{ln_xml}'
        f'</p:spPr>'
        f'<p:txBody>'
        f'<a:bodyPr wrap="square" lIns="110000" tIns="80000" rIns="110000" bIns="80000" anchor="ctr"/>'
        f'<a:lstStyle/>'
        f'{paragraphs_xml}'
        f'</p:txBody>'
        f'</p:sp>'
    )


def make_a_p(text, size_hundredths=1600, bold=False, italic=False, color="F8FAFC", align="l", space_after_pts=600):
    b_attr = ' b="1"' if bold else ""
    i_attr = ' i="1"' if italic else ""
    return (
        f'<a:p>'
        f'<a:pPr algn="{align}"><a:spcAft><a:spcPts val="{space_after_pts}"/></a:spcAft></a:pPr>'
        f'<a:r>'
        f'<a:rPr lang="vi-VN" sz="{size_hundredths}"{b_attr}{i_attr} dirty="0">'
        f'<a:solidFill><a:srgbClr val="{color}"/></a:solidFill>'
        f'<a:latin typeface="Segoe UI"/><a:ea typeface="Segoe UI"/><a:cs typeface="Segoe UI"/>'
        f'</a:rPr>'
        f'<a:t>{escape(text)}</a:t>'
        f'</a:r>'
        f'</a:p>'
    )


def make_pptx_picture(pic_id, rid, x, y, cx, cy):
    return (
        f'<p:pic>'
        f'<p:nvPicPr>'
        f'<p:cNvPr id="{pic_id}" name="Picture {pic_id}"/>'
        f'<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
        f'<p:nvPr/>'
        f'</p:nvPicPr>'
        f'<p:blipFill>'
        f'<a:blip r:embed="{rid}"/>'
        f'<a:stretch><a:fillRect/></a:stretch>'
        f'</p:blipFill>'
        f'<p:spPr>'
        f'<a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm>'
        f'<a:prstGeom prst="rect"><a:avLst/></a:prstGeom>'
        f'</p:spPr>'
        f'</p:pic>'
    )


def generate_pptx():
    """Tạo file PowerPoint .pptx chuẩn OpenXML (16:9 Widescreen - 12192000 x 6858000 EMUs) gồm 15 slides."""
    slide_w = 12192000
    slide_h = 6858000

    slides_xml = {}
    slides_rels = {}
    notes_xml = {}
    notes_rels = {}
    media_files = {}  # media_name -> abs_path

    for idx, s in enumerate(SLIDES_DATA, start=1):
        shapes = []

        # 1. Nền tối hiện đại (Dark Navy Background Card)
        shapes.append(make_pptx_shape_textbox(
            2, "Background", 0, 0, slide_w, slide_h,
            make_a_p(""), fill_hex="0B1120"
        ))

        # 2. Thanh Header Banner trên cùng
        shapes.append(make_pptx_shape_textbox(
            3, "TopBar", 0, 0, slide_w, 380000,
            make_a_p(f"  {s['section']}   |   HỆ THỐNG QUẢN LÝ THÚ CƯNG (PETCARE HUB) & CI/CD DEVOPS",
                     size_hundredths=1100, bold=True, color="10B981", align="l", space_after_pts=0),
            fill_hex="131C31"
        ))

        # 3. Nhãn số trang góc phải trên
        shapes.append(make_pptx_shape_textbox(
            4, "SlideNumberBadge", slide_w - 1750000, 45000, 1500000, 290000,
            make_a_p(f"SLIDE {s['num']:02d} / 15", size_hundredths=1100, bold=True, color="38BDF8", align="r", space_after_pts=0)
        ))

        # 4. Tiêu đề chính & Phụ đề của Slide
        title_p = (
            make_a_p(s["title"], size_hundredths=2200, bold=True, color="FFFFFF", align="l", space_after_pts=300) +
            make_a_p(s["subtitle"], size_hundredths=1300, italic=True, color="38BDF8", align="l", space_after_pts=0)
        )
        shapes.append(make_pptx_shape_textbox(
            5, "TitleBox", 380000, 460000, slide_w - 760000, 1020000, title_p
        ))

        # 5. Khung Nội dung bên trái (Bullets)
        left_x = 380000
        left_y = 1560000
        left_w = 6650000
        left_h = 3850000

        bullet_ps = []
        for b in s["bullets"]:
            bullet_ps.append(make_a_p("✔  " + b, size_hundredths=1320, bold=False, color="E2E8F0", align="l", space_after_pts=700))

        shapes.append(make_pptx_shape_textbox(
            6, "BulletsCard", left_x, left_y, left_w, left_h,
            "".join(bullet_ps), fill_hex="131C31", border_hex="1E293B", radius_adj=3000
        ))

        # 6. Ba ô Điểm nhấn (3 Key Metric Badges) phía dưới bên trái
        card_gap = 140000
        card_w = (left_w - 2 * card_gap) // 3
        card_y = 5540000
        card_h = 960000
        for h_idx, (h_val, h_lbl) in enumerate(s["highlights"]):
            cx_pos = left_x + h_idx * (card_w + card_gap)
            badge_p = (
                make_a_p(h_val, size_hundredths=1550, bold=True, color="10B981", align="ctr", space_after_pts=150) +
                make_a_p(h_lbl, size_hundredths=1050, bold=False, color="94A3B8", align="ctr", space_after_pts=0)
            )
            shapes.append(make_pptx_shape_textbox(
                10 + h_idx, f"Badge_{h_idx}", cx_pos, card_y, card_w, card_h,
                badge_p, fill_hex="111827", border_hex="0284C7", radius_adj=6000
            ))

        # 7. Khung Hình ảnh minh họa bên phải
        right_x = 7220000
        right_y = 1560000
        right_w = 4590000
        right_h = 4940000

        shapes.append(make_pptx_shape_textbox(
            20, "ImageCardFrame", right_x, right_y, right_w, right_h,
            make_a_p(""), fill_hex="131C31", border_hex="1E293B", radius_adj=3000
        ))

        abs_img = os.path.join(ROOT_DIR, s["image"].replace("/", os.sep))
        slide_rel_items = [
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>',
            f'<Relationship Id="rIdNotes" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide{idx}.xml"/>'
        ]
        if os.path.exists(abs_img):
            media_name = f"slide_{idx:02d}_{os.path.basename(abs_img)}"
            media_files[media_name] = abs_img
            slide_rel_items.append(
                f'<Relationship Id="rIdImg1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="../media/{media_name}"/>'
            )
            img_w, img_h = get_png_dimensions(abs_img)
            box_w = right_w - 260000
            box_h = right_h - 760000
            draw_w = box_w
            draw_h = int(box_w * img_h / img_w)
            if draw_h > box_h:
                draw_h = box_h
                draw_w = int(box_h * img_w / img_h)
            draw_x = right_x + (right_w - draw_w) // 2
            draw_y = right_y + 140000 + (box_h - draw_h) // 2
            shapes.append(make_pptx_picture(21, "rIdImg1", draw_x, draw_y, draw_w, draw_h))

        # Chú thích ảnh bên dưới khung phải
        shapes.append(make_pptx_shape_textbox(
            22, "ImageCaption", right_x + 100000, right_y + right_h - 560000, right_w - 200000, 480000,
            make_a_p(s["caption"], size_hundredths=1020, italic=True, color="94A3B8", align="ctr", space_after_pts=0)
        ))

        slides_xml[idx] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            '<p:cSld><p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            f'{"".join(shapes)}'
            '</p:spTree></p:cSld>'
            '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>'
            '</p:sld>'
        )

        slides_rels[idx] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'{"".join(slide_rel_items)}'
            '</Relationships>'
        )

        # Speaker Notes cho từng Slide
        notes_xml[idx] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
            'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
            '<p:cSld><p:spTree>'
            '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            '<p:sp>'
            '<p:nvSpPr><p:cNvPr id="2" name="Notes Placeholder"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph type="body" idx="1"/></p:nvPr></p:nvSpPr>'
            '<p:spPr/>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/>{make_a_p(s["notes"], size_hundredths=1200, color="000000")}</p:txBody>'
            '</p:sp>'
            '</p:spTree></p:cSld>'
            '</p:notes>'
        )
        notes_rels[idx] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide{idx}.xml"/>'
            '</Relationships>'
        )

    # Xây dựng presentation.xml, slideMaster1.xml, slideLayout1.xml, theme1.xml
    sld_id_entries = [
        f'<p:sldId id="{255 + i}" r:id="rIdSld{i}"/>'
        for i in range(1, len(SLIDES_DATA) + 1)
    ]
    presentation_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rIdMaster1"/></p:sldMasterIdLst>'
        f'<p:sldIdLst>{"".join(sld_id_entries)}</p:sldIdLst>'
        f'<p:sldSz cx="{slide_w}" cy="{slide_h}" type="screen16x9"/>'
        '<p:notesSz cx="6858000" cy="9144000"/>'
        '</p:presentation>'
    )

    pres_rels_entries = [
        '<Relationship Id="rIdMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>',
        '<Relationship Id="rIdTheme1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="theme/theme1.xml"/>'
    ] + [
        f'<Relationship Id="rIdSld{i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide{i}.xml"/>'
        for i in range(1, len(SLIDES_DATA) + 1)
    ]
    presentation_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        f'{"".join(pres_rels_entries)}'
        '</Relationships>'
    )

    slide_layout_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank" preserve="1">'
        '<p:cSld name="Blank"><p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        '</p:spTree></p:cSld>'
        '<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>'
        '</p:sldLayout>'
    )
    slide_layout_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>'
        '</Relationships>'
    )

    slide_master_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
        'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
        'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">'
        '<p:cSld><p:bg><p:bgRef idx="1001"><a:schemeClr val="bg1"/></p:bgRef></p:bg>'
        '<p:spTree>'
        '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
        '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
        '</p:spTree></p:cSld>'
        '<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
        '<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>'
        '</p:sldMaster>'
    )
    slide_master_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
        '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>'
        '</Relationships>'
    )

    theme_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="PetCareHubTheme">'
        '<a:themeElements>'
        '<a:clrScheme name="PetCareHub">'
        '<a:dk1><a:srgbClr val="0B1120"/></a:dk1>'
        '<a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>'
        '<a:dk2><a:srgbClr val="1E293B"/></a:dk2>'
        '<a:lt2><a:srgbClr val="F8FAFC"/></a:lt2>'
        '<a:accent1><a:srgbClr val="10B981"/></a:accent1>'
        '<a:accent2><a:srgbClr val="38BDF8"/></a:accent2>'
        '<a:accent3><a:srgbClr val="6366F1"/></a:accent3>'
        '<a:accent4><a:srgbClr val="F59E0B"/></a:accent4>'
        '<a:accent5><a:srgbClr val="EC4899"/></a:accent5>'
        '<a:accent6><a:srgbClr val="14B8A6"/></a:accent6>'
        '<a:hlink><a:srgbClr val="38BDF8"/></a:hlink>'
        '<a:folHlink><a:srgbClr val="818CF8"/></a:folHlink>'
        '</a:clrScheme>'
        '<a:fontScheme name="SegoeUI">'
        '<a:majorFont><a:latin typeface="Segoe UI"/><a:ea typeface="Segoe UI"/><a:cs typeface="Segoe UI"/></a:majorFont>'
        '<a:minorFont><a:latin typeface="Segoe UI"/><a:ea typeface="Segoe UI"/><a:cs typeface="Segoe UI"/></a:minorFont>'
        '</a:fontScheme>'
        '<a:fmtScheme name="Office">'
        '<a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>'
        '<a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="25400"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln><a:ln w="38100"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>'
        '<a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>'
        '<a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>'
        '</a:fmtScheme>'
        '</a:themeElements>'
        '</a:theme>'
    )

    root_rels_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>'
        '</Relationships>'
    )

    ct_overrides = [
        '<Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>',
        '<Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>',
        '<Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>',
        '<Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>'
    ]
    for i in range(1, len(SLIDES_DATA) + 1):
        ct_overrides.append(
            f'<Override PartName="/ppt/slides/slide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>'
        )
        ct_overrides.append(
            f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>'
        )

    content_types_xml = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="application/xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Default Extension="jpg" ContentType="image/jpeg"/>'
        f'{"".join(ct_overrides)}'
        '</Types>'
    )

    with zipfile.ZipFile(OUT_PPTX, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", content_types_xml)
        zf.writestr("_rels/.rels", root_rels_xml)
        zf.writestr("ppt/presentation.xml", presentation_xml)
        zf.writestr("ppt/_rels/presentation.xml.rels", presentation_rels_xml)
        zf.writestr("ppt/slideMasters/slideMaster1.xml", slide_master_xml)
        zf.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", slide_master_rels_xml)
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", slide_layout_xml)
        zf.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", slide_layout_rels_xml)
        zf.writestr("ppt/theme/theme1.xml", theme_xml)

        for i in range(1, len(SLIDES_DATA) + 1):
            zf.writestr(f"ppt/slides/slide{i}.xml", slides_xml[i])
            zf.writestr(f"ppt/slides/_rels/slide{i}.xml.rels", slides_rels[i])
            zf.writestr(f"ppt/notesSlides/notesSlide{i}.xml", notes_xml[i])
            zf.writestr(f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels", notes_rels[i])

        for media_name, abs_path in media_files.items():
            zf.write(abs_path, f"ppt/media/{media_name}")

    shutil.copy2(OUT_PPTX, OUT_WWW_PPTX)
    print(f"[OK] Đã tạo file PowerPoint (.pptx) 15 slides chuẩn 16:9 tại:")
    print(f"     - {OUT_PPTX} ({os.path.getsize(OUT_PPTX):,} bytes)")
    print(f"     - {OUT_WWW_PPTX} ({os.path.getsize(OUT_WWW_PPTX):,} bytes)")


if __name__ == "__main__":
    generate_markdown_slides()
    generate_html_slides()
    generate_pptx()
