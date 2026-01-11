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
