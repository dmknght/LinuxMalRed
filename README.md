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