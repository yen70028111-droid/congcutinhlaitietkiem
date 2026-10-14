Ứng dụng AI dự báo giá cổ phiếu bằng Streamlit
Ứng dụng dùng mô hình LSTM để dự báo tham khảo từ dữ liệu giá đóng cửa lịch sử lấy qua Yahoo Finance.
Chạy trên máy tính
pip install -r requirements.txt
streamlit run app.py
Mở địa chỉ local do Streamlit cung cấp trên trình duyệt.
Đưa lên GitHub và Streamlit Community Cloud
Tạo một repository mới trên GitHub.
Tải lên app.py, requirements.txt, README.md.
Vào https://share.streamlit.io/ và đăng nhập bằng GitHub.
Chọn Create app, chọn repository, branch và file app.py.
Nhấn Deploy.
Cách nhập mã
Việt Nam: VNM, FPT, VCB, HPG (ứng dụng tự thêm .VN).
Mỹ: AAPL, MSFT (nên dùng mã Yahoo Finance có dấu chấm nếu cần).
Lưu ý
Ứng dụng cần Internet để tải dữ liệu.
Lần đầu chạy mô hình có thể mất vài phút.
Ngày dự báo là ngày làm việc dự kiến, không bảo đảm khớp lịch nghỉ của từng sàn.
Đây là dự báo tham khảo, không phải lời khuyên đầu tư.
