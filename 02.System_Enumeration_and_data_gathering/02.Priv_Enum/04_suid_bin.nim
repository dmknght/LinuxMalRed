import os
import posix
import bitops

const list_check_dir = ["/bin", "/sbin", "/usr/bin", "/usr/sbin", "/usr/local/bin", "/opt/"]
    
    
proc owner_not_current_user(file_stat: Stat): bool =
    let current_user: Uid = getuid()

    if file_stat.st_uid != current_user:
        return true
    return false


proc excutable_uid_file(file_stat: Stat): bool =
    let file_mode = cast[cint](file_stat.st_mode)
    
    if (bitand(file_mode, S_ISUID) != 0 or bitand(file_mode, S_ISGID) != 0) and bitand(file_mode, S_IXUSR) != 0:
        return true
    return false
    

proc find_suid_binary(path: string) =
    for file_path in walkDirRec(path, yieldFilter={pcFile}): # We only get files
        var file_stat: Stat
        if stat(cstring(file_path), file_stat) != 0:
            echo "Error getting stat of file ", file_path
            continue

        if excutable_uid_file(file_stat) and owner_not_current_user(file_stat):
            echo file_path


for each_dir in list_check_dir:
    if dirExists(each_dir) and getFileInfo(each_dir, false).kind == pcDir: # Do not follow symlink
        find_suid_binary(each_dir)
