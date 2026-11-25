# Trùm Sub Like — cài iPhone qua GitHub Pages

Kho này chỉ chứa bộ Web Clip iOS được cho phép công khai.
Không có mã nguồn Android, APK, khóa ký hoặc thông tin đăng nhập.

## Cách bật lần đầu

1. Vào **Settings → Pages** của kho này.
2. Trong **Build and deployment → Source**, chọn **GitHub Actions**.
3. Vào **Actions → Publish iPhone install page → Run workflow → main → Run workflow**.
4. Chờ chạy thành công. Mở link trong phần **github-pages** / **Deployments** hoặc
   **Settings → Pages → Visit site**.
5. Gửi link trang đó cho người dùng iPhone. Mở bằng Safari, tải hồ sơ và xác nhận
   trong Cài đặt. Không gửi link file nguồn `splash.template.html` hay link GitHub `/blob/…`.

Nếu lần chạy đầu báo chưa bật Pages, hoàn thành bước 1–2 rồi chạy lại bước 3.
Không phải thay website trumsublike.com, không chạy PHP và không cần Cloudflare.

## Khi bấm biểu tượng iPhone

Hồ sơ mở `launch.html` trên Pages, hiển thị splash logo/ánh sáng/chữ phát triển rồi
chuyển sang `https://trumsublike.com` sau khoảng 1,8 giây.
Trong cùng phiên, `sessionStorage` tránh lặp splash; iOS có thể khôi phục phiên cũ
khi quay lại app thay vì chạy splash lần nữa.

URL trong hồ sơ được lấy từ metadata chính thức của `actions/configure-pages`,
không đoán hostname hoặc ghi cứng link website cũ.
Artifact công khai chỉ có `index.html`, `launch.html`, `icon.png`,
`trumsublike.mobileconfig` và `.nojekyll`; không xuất PHP hoặc mã Android.

GitHub Pages không cho đặt HTTP header PHP như hosting riêng.
Trang tải dùng link trực tiếp đến file `.mobileconfig`. Cần kiểm tra HTTP thật sau
khi Pages hoạt động và xác nhận thông báo cài hồ sơ bằng Safari/iPhone; không coi
workflow xanh là bằng chứng đã cài thành công trên mọi bản iOS.
Nếu máy chủ trả MIME không phù hợp hoặc Safari không nhận hồ sơ, phải báo rõ
giới hạn này thay vì hứa đã sửa được bằng thuộc tính HTML hay `_headers`.

Hồ sơ chưa ký có thể hiện “Chưa được xác minh”. Chỉ chứa Web Clip, không có MDM,
VPN hoặc chứng chỉ gốc. Web Clip không phải app native, không hỗ trợ bỏ kiểm tra
chứng chỉ Safari. Hành vi toàn màn hình và chuyển liên kết ngoài do iOS kiểm soát.
