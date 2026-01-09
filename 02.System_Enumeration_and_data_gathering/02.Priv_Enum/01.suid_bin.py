#!/usr/bin/env python3
import os
import stat

LIST_CHECK_DIR = ["/bin", "/sbin", "/usr/bin", "/usr/sbin", "/usr/local/bin", "/opt/"]


def owner_not_current_user(file_stat):
    """Kiểm tra owner khác user hiện tại"""
    current_user = os.getuid()
    return file_stat.st_uid != current_user


def excutable_uid_file(file_stat):
    """Kiểm tra file có SUID hoặc SGID bit"""
    file_mode = file_stat.st_mode
    return (file_mode & stat.S_ISUID) or (file_mode & stat.S_ISGID)


def find_suid_binary(path):
    """Tìm các file SUID/SGID trong thư mục"""
    for root, dirs, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)
            
            # Kiểm tra quyền execute trước bằng access() - chính xác hơn stat()
            if not os.access(file_path, os.X_OK):
                continue
            
            try:
                file_stat = os.lstat(file_path)
                
                # Chỉ xử lý file thông thường
                if not stat.S_ISREG(file_stat.st_mode):
                    continue
                
                if excutable_uid_file(file_stat) and owner_not_current_user(file_stat):
                    print(file_path)
                    
            except (OSError, PermissionError):
                continue


def main():
    for each_dir in LIST_CHECK_DIR:
        if os.path.isdir(each_dir) and not os.path.islink(each_dir):
            find_suid_binary(each_dir)


if __name__ == "__main__":
    main()