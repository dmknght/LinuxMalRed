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