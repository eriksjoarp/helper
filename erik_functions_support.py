#!/usr/bin/env python3

import os,time, shutil
import subprocess, psutil
import difflib, random

from datetime import datetime
from multiprocessing.pool import ThreadPool

from helper import erik_functions_init as e


#   get key in dictionary, if it does not exist return the alternative
def return_key_dict(dict,key_name, alternative = 'Error'):
    result = dict.get(key_name , alternative)
    return result



def cronjob_string(command_cronjob  , schedule_cronjob  , username):
    cronjob_ret = """'""" + schedule_cronjob + ' ' + username + ' ' + command_cronjob + """'"""
    return cronjob_ret



#   Move this to erik_functions #ToDo
def seconds_since_event(lista , event_name , when = 'latest' , default_event = 'started' ,separator = ','):

    event_time = False
    if when == 'latest':
        for line in lista:
            post = line.split(separator)
            if post[0] == event_name:
                event_time = int(post[2])
    elif when == 'first':
        for line in lista:
            post = line.split(separator)
            if post[0] == event_name:
                event_time = int(post[2])
                break

    if not(event_time):
        return 'never'

    difference = epoch_time() - event_time
    return difference




def dir_size(dir):
    total_size = 0

    #for path,dirs,files in os.walk(dir):
    #    for f in files:
    #        fp = os.path.join(path,f)
    #        total_size += os.path.getsize(fp)

    total_size = subprocess.check_output(['du', '-sb', dir]).split()[0].decode('utf-8')

    return total_size





##################################                      TIME                        ######################################



#   main time calculate function

def time_get(time_type, short_time = True):
    if time_type == e.TIME_TYPE_SECONDS_EPOCH:
        return int(time.time())
    elif time_type == e.TIME_TYPE_TODAY:
        return datetime.today().strftime('%Y-%m-%d')
    elif time_type == e.TIME_TYPE_TODAY_LONG:
        pass
    elif time_type == e.TIME_TYPE_HOURS():
        if short_time:
            return datetime.today().strftime('%H-%M')
        else:
            return datetime.today().strftime('%H-%M-%S')
    else:
        print('No such time type')
        return False


def time_epoch():
    return time_get(e.TIME_TYPE_SECONDS_EPOCH)

def time_today():
    return time_get(e.TIME_TYPE_TODAY)

def time_hours(short = True):
    if short:
        return time_get(e.TIME_TYPE_HOURS, True)
    else:
        return time_get(e.TIME_TYPE_HOURS, False)

def time_today_long():
    return time_get(e.TIME_TYPE_TODAY) + '-' + time_get(e.TIME_TYPE_HOURS)


def time_epoch_to_datetime(epochtime):
    ret_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(epochtime))
    return ret_time



def time_length_seconds(value, period='hours'):
    seconds = False
    if period == 'seconds':
        seconds = float(value)
    elif period == 'minutes':
        seconds = float(value) * 60
    elif period == 'hours':
        seconds = float(value) * 60 * 60
    elif period == 'days':
        seconds = float(value) * 60 * 60 * 24
    elif period == 'years':
        seconds = float(value) * 60 * 60 * 24 * 365
    return int(seconds)



###########         OLD     ###########

def epoch_time():
    seconds = int(time.time())
    return seconds


#   return todays date
def today():
    idag = datetime.today().strftime('%Y-%m-%d')
    return idag


def hours(short = True):
    if short:
        hours = datetime.today().strftime('%H-%M')
    else:
        hours = datetime.today().strftime('%H-%M-%S')
    return hours


def today_long():
    return today() + '-' + hours()


def epoch_time_to_datetime(epochtime):
    ret_time = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(epochtime))
    return ret_time


def length_seconds(value, period='hours'):
    seconds = False
    if period == 'seconds':
        seconds = float(value)
    elif period == 'minutes':
        seconds = float(value) * 60
    elif period == 'hours':
        seconds = float(value) * 60 * 60
    elif period == 'days':
        seconds = float(value) * 60 * 60 * 24
    elif period == 'years':
        seconds = float(value) * 60 * 60 * 24 * 365
    return int(seconds)





##################################                      LISTS                       ######################################

#   print everything in list
def print_all(lista):
    for i in lista:
        print(i)



# ToDo
def list_work_on(lista, search_string, work_type):  # work types  exists remove return_lines
    success = False
    if work_type == e.LIST_WORKTYPE_EXISTS:
        for item in lista:
            if search_string in item:
                success = True
    elif work_type == e.LIST_WORKTYPE_REMOVE:
        pass

    return success


def list_string_exists(lista, string):
    result = list_work_on(lista, string, e.LIST_WORKTYPE_EXISTS)
    return result

def list_remove_items_from(lista, string, exact=False):
    pass


def search_substring(string_to_search_in, search_string):
    result = string_to_search_in.find(search_string)

    if result == -1:
        return False
    else:
        return True


def substring_nr_in_list(lista, search_string, nr_apperance = 1):
    count_found = 0
    count = 0

    for item in lista:
        if search_substring(item, search_string):
            count_found +=1
            if nr_apperance == count_found:
                return count
        count +=1

    return e.NOT_FOUND







#############           OLD         #############




def highest_value_in_list(lista , event_name , type='number', separator=','):
    ret_value = 0

    if type=='number':
        for i in lista:
            post = i.split(separator)
            if post[0] == event_name:
                if ret_value < post[1]:
                    ret_value=post[1]

    return ret_value


def number_of_times(lista , key_word, separator =','):
    count = 0

    for line in lista:
        post = line.split(separator)
        if post[0] == key_word:
            count = count +1
    return count






##################################                      STRINGS                         ######################################



# SPLITS string in all its part by SEPARATOR
def string_split(string_to_split, separator = '.', place='all'):
    mylist = string_to_split.split(separator)

    if place == 'all':
        return mylist
    else:
        if len(mylist) < int(place):
            return False
        else:
            return mylist[place]



#   check if string ends with a supplied char
def string_end_swith_char(string0 , char):
    result = string0.endswith(char)
    return result

#   return string with quotes
def string_quote(string):
    string_new = """'""" + string + """'"""
    return string_new

def string_quote3(string):
    string_new = """'''""" + string + """'''"""
    return string_new







##########    OLD   REMOVE when changed in source


def split_string(string_to_split, separator = '.', place='all'):
    mylist = string_to_split.split(separator)

    if place == 'all':
        return mylist
    else:
        if len(mylist) < int(place):
            return False
        else:
            return mylist[place]

#   check if string ends with a supplied char
def check_string_endswith_char(string0 , char):
    result = string0.endswith(char)
    return result



#########################################################################################


#def processes_count(proc_name):
#    proc_list = processes()
#    count = proc_list.count(proc_name)
#    return count


def processes():
    proc_list = []
    for proc in psutil.process_iter():
        try:
            proc_list.append(proc.name())
        except:
            pass

    return proc_list



def ip_last_octet(ip_address, last_octet = True):
    #str(e_rem.ip_mine()).rsplit('.',1)
    ip_first_part , ip_return = str(ip_address).rsplit('.',1)

    if last_octet:
        return ip_return
    else:
        return ip_first_part


def threads_concurrent(target_function, commands, threads = 8):
    list_shuffle(commands,10)

    pool = ThreadPool(threads)
    results = pool.map(target_function, commands)
    pool.close()
    pool.join()

    return results


#   check if tool is on path and executable
def is_tool(toolname):
    from shutil import which

    return which(toolname) is not None


def list_shuffle(lista, nr_times = 10):
    for i in range(1,nr_times):
        random.shuffle(lista)
    return lista
