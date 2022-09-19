#!/usr/bin/env python3

#####################################
#
#
#
#           FUNCTIONS
#
#
#
#####################################

'''

erik_functions_

support         is lowest level
files           imports support
remote_help     imports support,files
remote          imports files,support, remote_help
functions_help
functions       top level, more complex funtions

'''

import sys
#sys.path.append('.')

import erik_functions_init as e
import erik_functions_files as e_fil
import erik_functions_remote as e_rem
import erik_functions_support as e_sup
import erik_functions_help as e_help



def remove_ramdisk(ip_node='local', mnt_dir = '/root/fuzzing', temporary=False):
    success = e_help.ramdisk(ip_node, False, 0, mnt_dir, temporary)
    return success

def create_ramdisk(ip_node='local', ramdisk_size=6000, mnt_dir='/root/fuzzing', temporary=False):
    success = e_help.ramdisk(ip_node, True, ramdisk_size, mnt_dir, temporary)
    return success

#   replaces first instance of found search_string with line_insert nr_lines_relative means directly after first find
def add_line_into_file(dir_src, filename_src, dir_dst, filename_dst, line_insert, search_string , nr_lines_relative=0, after = True, remove_old_line = True, nr_times_appearance=1):
    filelines_old = e_fil.get_filelines_to_list(dir_src, filename_src)

    line_nr_found = e_sup.substring_nr_in_list(filelines_old, search_string)

    if line_nr_found == e.NOT_FOUND:
        return False

    line_nr_insert = line_nr_found + nr_lines_relative
    if not after:
        line_nr_found -=1

    filelines_new = []

    inserted = False
    count = 0
    for fileline in filelines_old:
        if line_nr_insert < count and not inserted:
            filelines_new.append(line_insert)
            inserted = True
        filelines_new.append(fileline)
        count +=1

    pathfile_remove = e_fil.pathfile_make(dir_dst, filename_dst)
    e_fil.remove_file(pathfile_remove)
    e_fil.create_file_from_list(dir_dst, filename_dst, filelines_new)

    return True


def file_remove_duplicates(dir_src, file_src):
    pathfile = e_fil.pathfile_make(dir_src, file_src)
    if e_fil.file_exists(pathfile):
        filelines = e_fil.get_filelines_to_list(dir_src, file_src)
        filelines_new = set(filelines)

        if len(filelines) > len(filelines_new):
            print('SANITIZING PROBLEM CONFIG ' + file_src)
            e_fil.create_file_from_list(dir_src, file_src, filelines_new)





