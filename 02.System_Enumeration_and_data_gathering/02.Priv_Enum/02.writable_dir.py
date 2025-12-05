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