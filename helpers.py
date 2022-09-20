#!/usr/bin/env python3

import wget
import os
import bz2

# Find files in subdirs with correct extension
def files_in_dirs(base_dir, extension='.csv'):
    return_files = []
    for path, current_directory, files in os.walk(base_dir):
        for file in files:
            if file.endswith(extension):
                return_files.append(os.path.join(path, file))
    return return_files

# Check if file exists
def file_exists(path):
    if os.path.exists(path):
        return True
    else:
        print('ERROR cannot find file ' + path)
        return False

# Download file from url to a local path
def download_file(url, dst_dir, update=False):
    print('Downloading ' + url)
    wget.download(url, out=dst_dir)
    #wget.download(url)
    print('Downloaded ' + url)

# Extract bz2 file to dst_path ToDo
def bz2_extract(src_path, dst_dir):
    pass

def test():
    return 'test'

# join paths
def j(path1, path2):
    return os.path.join(path1, path2)

