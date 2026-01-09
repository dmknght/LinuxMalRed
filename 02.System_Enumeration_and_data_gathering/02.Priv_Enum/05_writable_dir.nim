import os
import posix

const list_dir_check = ["/opt/", "/usr/", "/var/", "/home/", "/etc/"]

for each_dir in list_dir_check:
    for sub_dir in walkDirRec(each_dir, yieldFilter={pcDir}):
        if access(cstring(sub_dir), W_OK) == 0: # Writable
            var dir_stat: Stat
            if stat(cstring(sub_dir), dir_stat) == 0: # We are able to get stat
                if dir_stat.st_uid != getuid(): # Different user
                    echo sub_dir
                else:
                    continue
            else:
                continue
        else:
            continue