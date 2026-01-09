import os
import posix
import bitops

const list_check_dir = ["/bin", "/sbin", "/usr/bin", "/usr/sbin", "/usr/local/bin", "/opt/"]


proc current_user_can_execute(file_stat: Stat): bool =
    let file_mode = cast[cint](file_stat.st_mode)
    
    if bitand(file_mode, S_IXUSR) != 0:
        return true
    return false
    
    
proc owner_not_current_user(file_stat: Stat): bool =
    let current_user: Uid = getuid()

    if file_stat.st_uid != current_user:
        return true
    return false


proc file_has_uid_bit(file_stat: Stat): bool =
    let file_mode = cast[cint](file_stat.st_mode)
    
    if (bitand(file_mode, S_ISUID) != 0 or bitand(file_mode, S_ISGID) != 0):
        return true
    return false
    

proc find_suid_binary(path: string) =
    for file_path in walkDirRec(path, yieldFilter={pcFile}): # We only get files
        var file_stat: Stat
        if stat(cstring(file_path), file_stat) != 0:
            echo "Error getting stat of file ", file_path
            continue

        if file_has_uid_bit(file_stat) and current_user_can_execute(file_stat) and owner_not_current_user(file_stat):
            echo file_path


for each_dir in list_check_dir:
    if dirExists(each_dir) and getFileInfo(each_dir, false).kind == pcDir: # Do not follow symlink
        find_suid_binary(each_dir)
