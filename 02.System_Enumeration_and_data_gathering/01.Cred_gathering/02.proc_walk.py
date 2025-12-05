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
