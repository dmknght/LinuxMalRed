# LinuxMalRed
Self-learn project about malware development for Redteam Operation on Linux

Personal hobby. It's going to use Python (might be Nim) to learn from scratch basic concept of Malware development, to (hopefully) more advanced skills. The point is to learn the mindset and concept rather than actual malicious activity, so Python might be a good choice.

# TODO add dbus to credential access and further exploitation

TODO:
# Strat:
Clean-Up Discipline: Tự động hóa việc xóa dấu vết sau mỗi bước thực thi.
- Assume Breach Mentality: Luôn giả định hệ thống đã bị giám sát, mọi hành động đều có thể bị ghi log.

# Advanced credential collection:
- memory dump, DPAPI & Keyring Exploitation: Trên Linux desktop environments (GNOME Keyring, KWallet).
Kernel Keyring: Khai thác kernel key retention service (/proc/keys, keyctl).

Browser Credential Extraction: Trích xuất password từ Firefox, Chrome profiles.

Password Managers: Tấn công các trình quản lý mật khẩu như KeePass, pass (gnupg).

Hardware Security Modules (HSM): Tìm cách extract key từ HSM nếu có.


# Lateral movement
- AD / kerberos
- Containerized Environment Movement: Kỹ thuật di chuyển giữa container, Kubernetes clusters, và host.


- SSH Hijacking & Agent Forwarding: Khai thác SSH agent socket (SSH_AUTH_SOCK).

# Priv esc
Hardening Bypass: Kỹ thuật bypass SELinux, AppArmor, seccomp.

Hardware-Based Escalation: Khai thác lỗi phần cứng (CPU, PCI devices).


Cách học: (đây chỉ là guideline )
- Mục đích là học lập trình + security để hiểu rõ hơn về lập trình, hệ thống (linux), vấn đề security
- Sử dụng mindset tấn công có thể tìm ra cách phòng thủ (dựa trên dấu vết, phương thức tấn công, ...)
- Mỗi tactic được sử dụng đều là 1 bài toán. Mục đích của project này là đưa ra tư duy giải quyết vấn đề (mindset) + phương hướng giải quyết (context, features, resources, ...). Cách giải quyết **không** nên giới hạn trong một ngôn ngữ lập trình cụ thể. Recommend nên sử dụng một ngôn ngữ lập trình ngoài python để thử giải quyết bài toán.

