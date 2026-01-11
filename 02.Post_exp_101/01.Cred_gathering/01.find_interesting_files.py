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
