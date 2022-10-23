#!/usr/bin/env python3

#from helper \
import shutil

from helper import erik_functions_support as e_sup

import os, tarfile, pathlib, time
import wget
import pickle
import subprocess
import cv2
#import yaml
from os import listdir
from os.path import isfile, join
import json
import random




######################################                 path manipulations                  ##########################################

def pathfile_make(dir_src ,file_src):
    path_created = os.path.join(dir_src, file_src)

    return path_created


def dir_path_full(dir_src, dirs_last):
    return_dirs = []
    for sub_dir in dirs_last:
        return_dirs.append(os.path.join(dir_src, sub_dir))
    if not return_dirs:
        return False
    return return_dirs

def dirs_in_dir(dir_files, full_path=False):
    if os.path.exists(dir_files):
        dirs = [f for f in listdir(dir_files) if os.path.isdir(join(dir_files, f))]
    else:
        print(r'''Error, directory doesn't exist:''' + dir_files)
        return False

    if full_path:
        dirs = dir_path_full(dir_files, dirs)
    return dirs

def dir_parent(path):
    dir_from_path = os.path.split(os.path.abspath(path))[0]
    #dir_parent = path.parent.absolute(dir_from_path)
    return dir_from_path

def dir_parent_basename(path):
    dir_par = dir_parent(path)
    dir_base = os.path.basename(path)
    return dir_par, dir_base

#
def file_split_from_path(path, must_exist=True):
    file_base = os.path.basename(path)
    file_name, file_ext = os.path.splitext(file_base)
    if must_exist:
        if file_exists(path):
            return file_name, file_ext
    else:
        return file_name, file_ext
    return False, False


def file_and_dir_from_path(pathfile):
    dirname, filename = os.path.split(pathfile)
    return dirname,filename

def path_split_from_path(path):
    if file_exists(path):
        dir_name = os.path.dirname(path)
        file_base = os.path.basename(path)
        file_name, file_ext = os.path.splitext(file_base)
        return dir_name, file_name, file_ext
    return False, False, False

#   get all folders in a path
def get_subfolders(dir_src):
    folders = [f.path for f in os.scandir(dir_src) if f.is_dir()]
    return folders

def filename_from_path(path):
    return os.path.basename(path)

def file_exists(path, supress_not_found=False):
    if os.path.exists(path):
        return True
    else:
        if not(supress_not_found):
            print('ERROR cannot find file ' + path)
        return False

def path_exists(dir_src):
    bExist = os.path.exists(dir_src)
    return bExist

def path_get_dir_and_file(path):
    filename = os.path.basename(path)
    directory = os.path.dirname(path)
    return directory, filename

#   check if a path is a directory
def is_directory(path):
    if os.path.isdir(path):
        return True
    return False

# read lines in a file into list
def get_filelines_to_list(dir_src, file_src):
    list_lines = []

    pathfile = pathfile_make(dir_src, file_src)

    if file_exists(pathfile):
        try:
            list_lines = []
            with open(pathfile) as f:
                list_lines = f.read().splitlines()
        except:
            print ("Error get_filelines_to_list: " + pathfile)
            return False
    else:
        print("Error file doesn't exist : get_filelines_to_list: " + str(pathfile))
        return False

    if file_length_lines(dir_src, file_src)==1:
        list_new=[]
        list_new.append(list_lines[0])
        #list_new.append(list_lines)
        list_lines=list_new

    if not list_lines:
        list_lines=[]

    return list_lines




######################################                    path contents                    ##########################################


#   find filename in path_search return pathfile
def find_path_filename(dir_search, filename):
    for root,dirs,files in os.walk(dir_search):
        for file in files:
            if file.strip() == filename:
                ret_string =  root + '/' + file.strip()
                return ret_string.replace('//','/')

    return False



# return all files in a directory
def files_in_dir(dir_files, full_path=False):
    if os.path.exists(dir_files):
        files = [f for f in listdir(dir_files) if isfile(join(dir_files, f))]
    else:
        print(r'''Error, directory doesn't exist:''' + dir_files)
        return False

    if full_path:
        return_files = []
        for file_unique in files:
            return_files.append(os.path.join(dir_files, file_unique))
    else:
        return_files = files
    return return_files


def files_images_in_dir(dir_files, extensions=['.jpg','.png','.jpeg']):
    path_images = []
    files = files_in_dir_full_path(dir_files)
    for file_iter in files:
        for ext in extensions:
            _, file_ext = file_split_from_path(file_iter)
            if file_ext.lower() == ext:
                path_images.append(file_iter)
    return path_images


def files_in_dir_full_path(dir_files):
    files = files_in_dir(dir_files)
    path_full = []
    for filename in files:
        path_file = os.path.join(dir_files, filename)
        path_full.append(path_file)
    return path_full


def get_nr_files_from_dir(path, nr_files_per_dir=1000, randomize_list=True):
    files = files_in_dir(path, full_path=True)
    if randomize_list:
        random.shuffle(files)

    nr_files = min(len(files), nr_files_per_dir)
    return files[:nr_files]



# Find files in subdirs with correct extension
def files_in_dirs(base_dir, extension='.csv'):
    return_files = []
    for path, current_directory, files in os.walk(base_dir):
        for file in files:
            if file.endswith(extension):
                return_files.append(os.path.join(path, file))
    return return_files




#   get all filenames of an extension in a directory
def get_filenames_in_dir(dir_src, extension ='NONE', full_path = False):
    files=[]
    dir_clean = return_dir_with_slash(dir_src)

    if path_exists(dir_clean):
        try:
            filenames = os.listdir(dir_clean)
            for filename in filenames:
                if os.path.isfile(dir_clean + filename):
                    if full_path:
                        filename = os.path.join(dir_src, filename)
                    if extension == 'NONE':
                        files.append(filename)
                    else:
                        if filename.endswith(extension):
                                files.append(filename)
        except:
            print ("Error get_files_in_dir")
            return False
    return files

#   find filename in path_search return pathfile
def find_string_in_file(dir_search, dir_dst, search_string):
    count = 0
    for root,dirs,files in os.walk(dir_search):
        for file in files:
            count +=1
            if count%1000==0:
                print(str(count))
            command = 'string'
    return False


#   get total size of a dir
def dir_size(dir_in):
    total_size = 0

    #for path,dirs,files in os.walk(dir):
    #    for f in files:
    #        fp = os.path.join(path,f)
    #        total_size += os.path.getsize(fp)

    total_size = subprocess.check_output(['du', '-sb', dir_in]).split()[0].decode('utf-8')
    return total_size




######################################                    write, read                      ##########################################

#   create a new file and overwrite it , add lines to it from list
#   ToDo quick dirty hack. It works for small config files but needs to be reimplemented
def create_file_from_list(dir_dst, file_dst, lista , chmod = '644'):
    create_missing_dirs(dir_dst)

    pathfile = pathfile_make(dir_dst , file_dst)
    remove_file2(dir_dst, file_dst)

    os.system('touch ' + pathfile)
    os.system('chmod ' + str(chmod) + ' ' + pathfile)

    for line0 in lista:
        append_line_to_file(pathfile,line0)


def json_load(path_json):
    if file_exists(path_json):
        try:
            with open(path_json) as json_file:
                json_data = json.load(json_file)
                return json_data
        except Exception as e:
            print('ERROR Could not read json file : ' + str(path_json) + ' error: ' + str(e))
            return False


def json_dump(path_json, json_data):
    try:
        with open(path_json, 'w') as outfile:
            json.dump(json_data, outfile, indent=2)
    except Exception as e:
        print('ERROR Could not write json file : ' + str(path_json) + ' error: ' + str(e))
        return False


def pickle_write(data, pathfile):
    with open(pathfile, 'wb') as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)

def pickle_read(pathfile):
    with open(pathfile, 'rb') as handle:
        data = pickle.load(handle)


#   get config
def get_config(path, filename , type_file):

    pathfile = pathfile_make(path, filename)

    config_files = get_filenames_in_dir(path, type_file)
    config_file_name = config_files[0]
    config = readfile_to_dict(config_file_name , pathfile)

    return config


def image_read_from_file(path):
    try:
        img = cv2.imread(path)
    except:
        print('Could not find file : ' + str(path))
        return False
    return img

def load_images_from_folder(path):
    images = []
    path_images = []
    for filename in os.listdir(path):
        img = cv2.imread(os.path.join(path,filename))
        if img is not None:
            images.append(img)
            path_images.append((filename))
    return images, path_images


# copy all files in a dir to another and possibly remove all the old files
def copy_files_from_dir_to_dir(dir_from, dir_save, delete_old_save=False, delete_old_src=False):
    files = get_filenames_in_dir(dir_from, full_path=True)
    copy_files(files, dir_save=dir_save, delete_old_save=delete_old_save, delete_old_src= delete_old_src)
    return True


# copy list of files into dir_save, removes everything in save dir and everything in src dir if the flags are set to True
def copy_files(path_files, dir_save, delete_old_src=False, delete_old_save=False):
    # remove old files in save directory
    if delete_old_save:
        shutil.rmtree(dir_save, ignore_errors=True)

    os.makedirs(dir_save, exist_ok=True)
    for path_file in path_files:                            # copy files
        shutil.copy2(path_file, dir_save)

    # remove old files in src directory
    if delete_old_src:
        dir_remove, _ = path_get_dir_and_file(path_files[0])
        shutil.rmtree(dir_remove, ignore_errors=True)
        os.makedirs(dir_remove)
    return True


# write a list to file
def write_list_to_file(path,my_list):
    try:
        os.remove(path)
    except Exception as e:
        pass

    try:
        with open(path, 'w') as f:
            f.write("\n".join(my_list))
        return True
    except Exception as e:
        pass
    return False


#   read fileconfig into dictionary
def readfile_to_dict(dir_src , file_src, separator=','):
    lines = get_filelines_to_list(dir_src, file_src)

    ordbok = {}
    for i in lines:
        mylist = i.split(separator)
        keyword = mylist[0].strip()
        dictword = mylist[1].strip()
        ordbok[keyword] = dictword
    return ordbok



######################################                        operate on files                      ##########################################


#   make tarfile
def make_tarfile(output_filename , dir_src):
    try:
        with tarfile.open(output_filename , 'w:gz') as tar:
            tar.add(dir_src , arcname=os.path.basename(dir_src))
            tar.close()
    except:
        print('Error making tarfile :' + output_filename)
        tar.close()
        return False
    return True


def extract_tar(dir_src,filename_src, path_dest):
    try:
        tf = tarfile.open(pathfile_make(dir_src, filename_src))
        tf.extractall(path_dest)
        tf.close()
        return True
    except:
        print ('Extract error')
        return False



######################################                  compatibility                   ##############################################


def execute_command(command, sleep_secs = 0.2):
    try:
        print(command)
        results = os.system(command)
        time.sleep(sleep_secs)
    except:
        print('Error executing :' + command)
        return False
    return results



######################################                  linux                           ##############################################

#   Linux
#   append string to last line in file
#   ToDo quick dirty hack. It works for small config files but needs to be reimplemented
def append_line_to_file(pathfile, appendage):
    execute_command('echo ' + appendage + '>>' + pathfile)


def cronjob_create(command_cronjob , schedule_cronjob , username ='root'):
    cronjob_write = e_sup.cronjob_string(command_cronjob , schedule_cronjob = """* * * * *""" , username = """root""")
    append_line_to_file("""/etc/crontab""" , cronjob_write)




########################                  DELETE
def create_missing_dirs(pathfile):
    # check if it ends with / then its a dir
    #dir_src = pathfile
    #if not(e_sup.check_string_endswith_char(pathfile , '/')):
    #    dir_src, file_Src  = pathfile.rsplit('/',1)
    dir_src, file_Src = path_get_dir_and_file(pathfile)

    if not path_exists(path_exists(dir_src)):
        make_dir(dir_src)


def bash_copy_file(pathfile_src, path_dst):
    success = True
    create_missing_dirs(path_dst)

    if file_exists(pathfile_src):
        command = 'cp ' + pathfile_src + ' ' + path_dst
        execute_command(command)
    else:
        print('Error : file does not exist Bash_copy_file ' + str(pathfile_src))
        success = False
    return success


def bash_move_file(pathfile_src, path_dst):
    success = True
    create_missing_dirs(path_dst)

    if file_exists(pathfile_src):
        command = 'mv -f ' + pathfile_src + ' ' + path_dst
        os.system(command)
    else:
        print('Error : file does not exist bash_move_file ' + str(pathfile_src))
        success = False
    return success


def bash_rm_dir(dir_src , inside = False):
    if inside:
        command = 'rm -rf ' + dir_src + '*'
    else:
        command = 'rm -rf ' + dir_src

    try:
        execute_command(command, 0.1)
    except:
        print('Directory does not exist Bash_rm_dir' + str(dir_src))

def bash_rm_file(dir_src , file_src):
    pathfile = pathfile_make(dir_src, file_src)

    if file_exists(pathfile):
        command = 'rm -f' + pathfile
        execute_command(command,0.1)
    if not file_exists(pathfile):
        return True
    else:
        return False

def gcp_copy(dir_src, path_dst):
    #create_missing_dirs(return_dir_with_slash(path_dst))

    command = 'gcp -r ' + dir_src + ' ' + path_dst
    os.system(command)

def bash_copy_dir(dir_src, path_dst):
    #create_missing_dirs(return_dir_with_slash(path_dst))
    command = 'cp -r ' + dir_src + ' ' + path_dst
    os.system(command)

def rename_file(dir_src,file_src, dir_dst, file_dst):
    success = True

    old_file = os.path.join(dir_src, file_src)
    new_file = os.path.join(dir_dst, file_dst)

    try:
        os.rename(old_file, new_file)
    except:
        print("could not rename " + old_file)
        success = False

    return success




#   make new dirs
def make_dir(dir_new):
    dir_dst = return_dir_with_slash(dir_new)
    os.makedirs(dir_dst, exist_ok=True)

def make_dir_bash(dir_new):
    command = 'mkdir -p ' + dir_new
    execute_command(command)

def remove_file(pathfile):
    success = True
    if file_exists(pathfile):
        try:
            os.remove(pathfile)
        except:
            print('could not remove existing file ' + str(pathfile))
            success = False
    return success

def remove_file2(dir_src ,file_src):
    success = True
    pathfile = pathfile_make(dir_src , file_src)

    if file_exists(pathfile):
        try:
            os.remove(pathfile)
        except:
            print('could not remove existing file ' + str(pathfile))
            success = False
    return success


#   return path with /
def return_dir_with_slash(dir_src):
    result = dir_src
    if not(e_sup.check_string_endswith_char(dir_src , '/')):
        result = dir_src + '/'
    return result


# move and overwrite file
def move_overwrite_file(dir_src, file_src, dir_dst):
    remove_file2(dir_dst, file_src)

    pathfile_src = pathfile_make(dir_src, file_src)
    bash_copy_file(dir_src + file_src, dir_dst)
    remove_file(pathfile_src)

    pathfile_dst = pathfile_make(dir_dst, file_src)
    success = file_exists(pathfile_dst)

    return success




def copy_and_extract_tar_into_empty_dir_return_folderpath(dir_src, filename_src, path_dst):
    command = 'rm -rf ' + path_dst + '*'
    execute_command(command)

    bash_copy_file(dir_src + filename_src, path_dst)
    extract_tar(path_dst, filename_src, path_dst)

    lista = get_subfolders(path_dst)
    if len(lista)>0:
        return lista[0] + '/'



############                        OTHER                       ############

def get_dir(path_file):
    dir_src , file_src = path_file.rsplit('/', 1)
    return dir_src

def get_file(path_file):
    dir_src , file_src = path_file.rsplit('/', 1)
    return file_src


def file_length_lines(path ,filename):
    i= -1
    pathfile = pathfile_make(path , filename)
    try:
        with open(pathfile) as f:
            for i,l in enumerate(f):
                pass
    except:
        print("""Error counting file_length, file probably doesn't exist""")
    return i + 1


def escape_chars(name):
    new_name = ''
    for char in name:
        if char == ':':
            new_name = new_name + '\:'
        elif char == ',':
            new_name = new_name + '\,'
        #elif char == """/""":
        #    new_name = new_name + """//"""
        elif char == "'":
            new_name = new_name + """\'"""
        else:
            new_name = new_name + char

    return new_name






############                  FLAG handling                   ###############


def touch_filename(path , filename):
    if not path_exists(path):
        create_missing_dirs(path)
    pathfile = pathfile_make(path, filename)
    if not file_exists(pathfile):
        pathlib.Path(pathfile).touch()

def check_if_flag(path , flagname):
    pathfile = pathfile_make(path, flagname)
    if not path_exists(path):
        create_missing_dirs(path)
    bExist = file_exists(pathfile)
    return bExist

def put_flag(path , flagname):
    pathfile = pathfile_make(path, flagname)
    if not path_exists(path):
        create_missing_dirs(path)
    if not file_exists(pathfile):
        pathlib.Path(pathfile).touch()

def remove_flag(path, flagname):
    #if not path_exists(path):
    #    create_missing_dirs(path)
    pathfile = pathfile_make(path, flagname)
    if file_exists(pathfile):
        remove_file(pathfile)





'''
# read yaml file
def load_config_yaml(dir_yaml, filename):
    path = os.path.join(dir_yaml, filename)
    with open(path) as file:
        try:
            yaml_data = yaml.safe_load(file)
        except:
            print('ERROR cannot open file ' + path)
            return False
    return yaml_data
'''






