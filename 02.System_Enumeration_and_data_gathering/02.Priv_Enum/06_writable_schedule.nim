import os
import posix

const dir_units = [
    # Cronjob Files
    "/etc/crontab",
    "/etc/cron.d",
    "/etc/cron.hourly",
    "/etc/cron.daily",
    "/etc/cron.weekly",
    "/etc/cron.monthly",
    
    # Systemd Service Files
    "/etc/systemd/system",
    "/lib/systemd/system",
    
    # Init.d/SysVinit Files
    "/etc/init.d",
    
    # At Job Files (ít phổ biến hơn)
    "/var/spool/cron/atjobs", 
]


for each_dir in dir_units:
    for each_file in walkDirRec(each_dir, yieldFilter = {pcFile}):
        if access(cstring(each_file), W_OK) == 0:
            echo each_file