# file functions that is on a higher level hence not small help functions
import os
import shutil

from helper import erik_functions_files



# takes a path, all child directorys in path is truncated to a fixed amount of files
def dirs_truncate_to_out_dir(dir_from, dir_to, nr_files_per_dir = 100, randomize_files = True, remove_old_dir_to=True):
    if remove_old_dir_to:
        shutil.rmtree(dir_to, ignore_errors=True)

    dirs = erik_functions_files.dirs_in_dir(dir_from)

    for sub_dir in dirs:
        sub_dir_full_path = os.path.join(dir_from, sub_dir)     # full path to the subdir
        dir_out = os.path.join(dir_to, sub_dir)                 # copy to dir

        sub_dir_files = erik_functions_files.get_nr_files_from_dir(sub_dir_full_path, nr_files_per_dir=nr_files_per_dir, randomize_list=randomize_files)
        erik_functions_files.copy_files(sub_dir_files, dir_out)
    return True



if __name__=='__main__':

    dir_from = r'C:\ai\datasets\eurosat\EuroSAT\2750_32'
    dir_to = r'C:\ai\datasets\eurosat\EuroSAT\2750_32_1000images'

    # test truncate dirs with lots of files to a small one
    dirs_truncate_to_out_dir(dir_from, dir_to, 1000, randomize_files=True)

