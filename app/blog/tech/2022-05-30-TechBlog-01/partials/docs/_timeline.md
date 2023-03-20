### 07:00 - 31/05/2022

- Heroku đã chính thức khôi phục lại toàn bộ việc kết nối với Github sau sự cố liên quan đến OAuth 2.0. Toàn bộ các tài khoản đã được bật xác thực hai bước để đảm bảo an toàn.

- Travis CI cũng đã thực hiện các biện pháp mạnh để thực hiện khôi phục lại tính an toàn cho hệ thống.

- Cho đến thời điểm hiện tại, dịch vụ Youtube Downloader đã có thể cho phép truy cập trở lại thông qua hệ thống của Heroku. Do đó trong thời gian sớm nhất, tôi sẽ tiến hành khôi phục lại việc kết nối và trang web chính thức chạy trên Heroku cho dịch vụ này. Bài đăng này sẽ được đóng cập nhật vào hôm nay.

- Trân trọng cảm ơn sự đồng hành của quý độc giả. Thông tin chi tiết về sự trở lại của Youtube Downloader trên website của Heroku sẽ được đăng tải dự kiến vào ngày **_01/07/2022_**. Xin chào.

### 18:40 - 07/05/2022

- Heroku đã thông báo về việc thiết lập lại mật khẩu cho tài khoản của tôi. Xác thực 2 bước đã được thực hiện. Tuy nhiên, cho đến khi tình hình được kiểm soát hoàn toàn, việc kết nối đến Heroku sẽ bị tạm dừng.

- Tôi đã kích hoạt cơ chế dự phòng cho Youtube Downloader, bao gồm việc tiến hành đưa dịch vụ lên trên **Github Packages** (sử dụng công nghệ **_Docker_**). Mọi người có thể tải xuống Packages này qua lệnh `docker pull ghcr.io/anthony2708/youtube_downloader:latest` sau khi cài đặt Docker. Chi tiết xin xem tại website này: [Github Packages](https://github.com/anthony2708/anthony2708/pkgs/container/youtube_downloader).

- Tôi sẽ theo dõi sát sao tình hình tiếp theo và sẽ tiếp tục cập nhật thông tin trên bài viết này trong thời gian sớm nhất.

### 15:40 - 28/04/2022

- Hiện tại, tôi đã nhận được email liên quan đến vụ rò rỉ OAuth của Heroku và Github.

- Cho đến thời điểm hiện tại, tôi có thể xác nhận ít nhất **MỘT** trong số các kho lưu trữ (Repository) của tôi có liên quan đến Heroku và thông tin có thể đã bị rò rỉ ở mức độ **nghiêm trọng**. Trang web chính thức của tôi đã được đóng lại để đảm bảo an toàn. Do đó, chức năng **_Youtube Downloader_** trên website cũng đã được **TẠM DỪNG** cho đến khi có thông báo mới nhất.

- Tôi đang theo dõi sát sao tình hình của sự việc này và sẽ liên tục cập nhật thông tin trên bài viết này trong thời gian sớm nhất.

### 19:00 - 18/04/2022

- Github xác nhận vào ngày 12/04/2022 rằng các tin tặc đang lợi dụng OAuth 2.0 để tải xuống trái phép dữ liệu bí mật của một số tổ chức. Một trong số các dịch vụ chịu ảnh hưởng là **_Heroku_**, nơi trang web của tôi đang đặt máy chủ. Thông tin chi tiết sẽ liên tục cập nhật trong thời gian sớm nhất trên bài viết này.
