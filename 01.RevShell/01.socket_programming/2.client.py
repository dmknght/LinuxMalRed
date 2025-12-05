import socket

# Cấu hình Host và Port của Server
HOST = '127.0.0.1'  # Địa chỉ server
PORT = 9191         # Cổng server

# 1. Tạo socket (AF_INET cho IPv4, SOCK_STREAM cho TCP)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 2. Kết nối đến Server
    client_socket.connect((HOST, PORT))
    print(f"[*] Đã kết nối đến Server {HOST}:{PORT}")

    # Vòng lặp chính để gửi dữ liệu
    while True:
        # Nhận input từ người dùng
        message = input("Nhập tin nhắn để gửi đến server (gõ 'quit' để thoát): ")
        
        if message.lower() == 'quit':
            break
        
        # Mã hóa và gửi dữ liệu đến server
        client_socket.sendall(message.encode('utf-8'))
        
        # (Tùy chọn) Nhận phản hồi từ server
        response = client_socket.recv(1024)
        print(f"Server phản hồi: {response.decode('utf-8')}")
        
except ConnectionRefusedError:
    print("Lỗi: Không thể kết nối. Hãy đảm bảo Server đang chạy.")
except Exception as e:
    print(f"Lỗi xảy ra: {e}")
finally:
    # Đóng socket
    client_socket.close()
    print("[*] Client đã tắt.")