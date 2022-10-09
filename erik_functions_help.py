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
functions_help  helper to make functions small and easy to use
functions       top level, more complex funtions


'''

from helper import erik_functions_init as e
from helper import erik_functions_files as e_fil
from helper import erik_functions_support as e_sup
from helper import erik_functions_remote as e_rem


# works for root no sudo etc        RAMDISK
def ramdisk(ip_node, create, ramdisk_size=6000, mnt_dir='/root/fuzzing', temporary = False):
    e_fil.make_dir_bash('~/tmp')

    dir_fstab_tmp = '/root/tmp/'
    filename_fstab = 'fstab'
    pathfile_fstab_tmp = dir_fstab_tmp + filename_fstab
    dir_fstab = '/etc/'
    pathfile_fstab = dir_fstab + filename_fstab

    e_fil.remove_file(pathfile_fstab_tmp)

    if create:
        created_new = False
        if not temporary:
            print('Creating ramdisk in fstab')

            #   move fstab to local dir
            if ip_node == 'local':
                e_fil.bash_copy_file(pathfile_fstab, pathfile_fstab_tmp)
                e_fil.make_dir(mnt_dir)
            else:
                e_rem.scp_file(ip_node, pathfile_fstab, dir_fstab_tmp, e.USER_ROOT, False)
                e_rem.makedirs_remote_host(ip_node, [mnt_dir])

            if not e_fil.file_exists(pathfile_fstab_tmp):
                print('Could not get fstab and hence not create a ramdisk')
                return False

            lines = e_fil.get_filelines_to_list(dir_fstab_tmp, filename_fstab)

            #check if ramdisk is already in fastab
            if not e_sup.list_string_exists(lines, ' ' + mnt_dir + ' '):
                # add to fstab
                ramdisk_line = 'tmpfs    ' + mnt_dir + '    tmpfs    nodev,nosuid,noatime,nodiratime,size=' + str(ramdisk_size) + 'M    0    0'
                print (ramdisk_line)

                e_fil.append_line_to_file(pathfile_fstab_tmp, e_sup.string_quote(ramdisk_line))

                #move file back
                if ip_node=='local':
                    e_fil.move_overwrite_file(dir_fstab_tmp, filename_fstab,dir_fstab)
                else:
                    e_rem.scp_file(ip_node, pathfile_fstab_tmp, dir_fstab)

                e_fil.remove_file(pathfile_fstab_tmp)

                created_new = True

        return created_new

    else:
        #Remove ramdisk
        pass





#ToDo
def cronjob():
    pass

def cronjob_create(ip_node='local'):
    pass

def cronjob_remove():
    pass


def keys_values_from_dict(dictionary_src):
    keys = []
    values = []

    if isinstance(dictionary_src,dict):
        for key, value in dictionary_src.items():
            keys.append(key)
            values.append(value)
    else:
        return [],[]

    return keys, values


def similarity(items1, items2):
    comparison_possible = False

    if not (return_type(items1) == return_type(items2)):
        return 0

    if return_type(items1) == e.TYPE_DICT:
        comparison_possible = True
        keys1, values1 = keys_values_from_dict(items1)
        keys2, values2 = keys_values_from_dict(items2)
    elif return_type(items1) == e.TYPE_LIST:
        comparison_possible = True
        keys1 = items1
        keys2 = items2
    else:
        return 0

    smilarity_lists = lists_percentage_similarity(keys1,keys2)

    return smilarity_lists



def return_type(item0):
    if isinstance(item0, list):
        return e.TYPE_LIST
    if isinstance(item0, dict):
        return e.TYPE_DICT
    if isinstance(item0, int):
        return e.TYPE_INTEGER
    if isinstance(item0, float):
        return e.TYPE_FLOAT
    if isinstance(item0, str):
        return e.TYPE_STRING



def lists_percentage_similarity(list1,list2):
    nr_hits = 0
    nr_keys = 0.000001

    for item_list1 in list1:
        found = False
        for item_list2 in list2:
            if item_list1 == item_list2:
                found = True

        nr_keys +=1
        if found: nr_hits +=1

    similarity0 = float(nr_hits) / float(nr_keys)

    return similarity0
