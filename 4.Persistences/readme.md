# Linux system persistence
- **Objectives:**
  - Locations in Linux that can trigger custom commands

- **Activities:**
  - Logon persistence
    - System daemon
    - X-11 auto start
  - Schedule persistence:
    - systemd timer
    - cron
  - Event trigger persistence:
    - Shell config modification (`.bashrc`)
    - Udev rules
    - Hooking scripts (network hooking script for example)


**Resources**:
  - **MySQL Plugin Load:** https://dev.mysql.com/doc/refman/8.4/en/plugin-loading.html
  - **Systemd as user**: https://serverfault.com/questions/841099/systemd-grant-an-unprivileged-user-permission-to-alter-one-specific-service
  - **System hook script locations:**
    - `/etc/needrestart/hook.d/`
    - `/etc/network/if-down.d/`
    - `/etc/update-motd.d`
