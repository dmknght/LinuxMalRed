import socket

HOST = '127.0.0.1'  # Giao diện loopback tiêu chuẩn (localhost)
PORT = 9191         # Cổng để lắng nghe

# 1. Tạo socket (AF_INET cho IPv4, SOCK_STREAM cho TCP)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. Gán socket với địa chỉ và cổng
server_socket.bind((HOST, PORT))

# 3. Bắt đầu lắng nghe kết nối đến (tối đa 1 kết nối đang chờ)
server_socket.listen(1)
print(f"[*] Server đang lắng nghe trên {HOST}:{PORT}")

# Chờ và chấp nhận kết nối từ client
conn, addr = server_socket.accept()
print(f"[*] Đã chấp nhận kết nối từ: {addr[0]}:{addr[1]}")

try:
    # Vòng lặp chính để nhận và xử lý dữ liệu
    while True:
        # Nhận dữ liệu (tối đa 1024 bytes)
        data = conn.recv(1024)
        if not data:
            # Client đóng kết nối
            print("[-] Client đã đóng kết nối.")
            break

        # Giải mã dữ liệu nhận được (từ bytes sang string)
        client_data = data.decode('utf-8')

        # In ra màn hình theo yêu cầu
        print(f"Client gửi: <{client_data}>")

        # (Tùy chọn) Gửi phản hồi lại client
        conn.sendall(f"Server đã nhận: {client_data}".encode('utf-8'))

except Exception as e:
    print(f"Lỗi xảy ra: {e}")
finally:
    # Đóng kết nối và socket
    conn.close()
    server_socket.close()
    print("[*] Server đã tắt.")