# Drop4_AI
Mô phỏng game đối kháng Drop 4 bằng thuật toán MINIMAX và cắt tỉa alpha-beta

Chính là trò chơi cờ caro, chỉ khác là các quân cờ thay vì được đánh ở một vị trí bất kì, thì bị thả rơi xuống dưới đáy bảng

# Cách xem
## Update giữa kì

Bao gồm:
- Một ClassicPlay thể hiện một lượt chơi kinh điển đánh hòa với máy
- File main.py trong thư mục UpdateGiuaKi là file chính để chạy chương trình theo cách hướng đối tượng. 3 file nữa cũng dùng để cài đặt chương trình nằm trong UpdateGiuaki/Drop4/
- Báo cáo giữa kì bản word tạm thời


## Update cuối kì

Bao gồm:

- Các classicplay có 11 nước đi của máy tương ứng với độ sâu 4, 5 và 8.
- Các biểu đồ so sánh
- Dữ liệu thuần sau khi chạy trực tiếp trên máy tính để lưu vào Excel
- Một file main.py theo cách hướng thủ tục duy nhất thể hiện mô phỏng bài tập lớn (không bao gồm các folder và các file rườm rà khác nữa cho dễ bảo vệ)
- Báo cáo dạng Jupyter Notebook theo yêu cầu của giáo viên

# Một số chú ý

- Cần bổ sung sự so sánh giữa việc có và không có cắt tỉa alpha-beta sẽ tăng/giảm tốc độ chương trình như thế nào
- Nên có sự so sánh so với trò caro thông thường
- Nên thể hiện sự so sánh thuật toán trong bài tập lớn với một thứ gì đó khác (chứ không nên để con người làm đối thủ, tại vì với độ sâu tìm kiếm bằng 6 thì máy thắng người là cái chắc)
- Làm giao diện đẹp đẹp cũng được. Thực ra thầy chỉ kiểm tra mình có hiểu bài hay không thôi.

# Các câu hỏi quan trọng để bảo vệ bài tập lớn

- Giải thích xem tại vị trí node lá thì giá trị hàm lượng giá được xác định thế nào?
- Tại sao lại phải đặt bộ 3 có hệ số điểm nhiều hơn bộ 2?
- Tính được số lần cắt tỉa bằng cách nào?
- Không gian trạng thái của trò chơi này so với caro thông thường là ít hơn/nhiều hơn bao nhiêu lần đối với bảng 10x10?
- Thử xóa hàm lượng giá này xong code lại xem có code lại được không (thực hiện trong 10 phút)?