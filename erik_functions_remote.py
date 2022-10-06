#!/usr/bin/env python3

from . import erik_functions_init as e
from . import erik_functions_files as e_fil
from . import erik_functions_support as e_sup

import os,time, wget
import paramiko
from time import sleep
import socket
import subprocess, pipes



def ip_mine():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_local=False
    try:
        s.connect(('192.168.1.1' , 80))
        ip_local = s.getsockname()[0]
    except:
        print("Error Ip")
        s.close()
    s.close()

    return ip_local



##################################                          SSH                             ######################################




def createSSHClient(host, port = 22, user= 'root',password = ' none'):
    sshclient = paramiko.SSHClient()
    sshclient.load_system_host_keys()
    sshclient.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    sshclient.connect(host, port, user) # ,password)
    #scp = SCPClient(ssh.get_transport())
    sleep(0.1)
    return sshclient



#   execute command over ssh
def ssh_command(host, command , delay0 = 0.3, user = 'root'):
    command_ssh = 'ssh ' + user + '@' + host + """ '""" + command + """'"""
    print(command_ssh)
    try :
        os.system(command_ssh)
        time.sleep(delay0)
    except:
        print('SSH error, could not execute: ' + command_ssh)




def ssh_command2(sshclient, command_list):
    sshshell = sshclient.invoke_shell()

    for command in command_list:
        try:
            sshshell.exec_command(command)

            sleep(0.3)
        except:
            print ('Error , could not execute ' + command)

    sshshell.close()



def ssh_command3(sshclient, command , sleeps = 0.2):
    try:
        sshclient.exec_command(command)
        sleep(10)
    except:
        print('SSHcommand error' + command)

    sleep(sleeps)




def sshpass_remote(host, command, pathfile_username, username=e.USER_ROOT, sshpass_type = 'ssh'):
    if e_fil.file_exists(pathfile_username):
        command_sshpass_start = 'sshpass -f ' + pathfile_username + ' '
    else:
        print('No username file detected')
        return False

    if sshpass_type == 'ssh':
        command_sshpass_end = 'ssh ' + username + '@' + host + ' ' + command
    elif sshpass_type == 'scp':
        command_sshpass_end = command
    else:
        command_sshpass = False
        command_sshpass_end = ''

    command_sshpass = command_sshpass_start + command_sshpass_end

    try:
        if command_sshpass:
            print(command_sshpass)
            e_fil.execute_command(command_sshpass)
    except:
        print('Error sshpass_remote : command ' + command_sshpass)
        return False

    return True




def sshpass_scp(host, pathfile_pw, DIR_SRC, path_dst, user='root'):

    scp_command = 'scp -r ' + user + '@' + host + ':' + DIR_SRC + ' ' + path_dst

    sshpass_remote(host, scp_command, pathfile_pw, user, 'scp')





##################################                          SCP                         ######################################




# transfer one file with scp
def scp_file_remote(ip_src , ip_dst , pathfile_src , path_dst , user_src='root' , user_dst = 'root' , password_src ='' , password_dst = ''):
    command = 'scp -r ' + user_src + '@' + ip_src + """:/""" + pathfile_src + ' ' + user_dst + '@' + ip_dst + """:/""" + path_dst
    print(command)
    try:
        os.system(command)
        time.sleep(2)
    except:
        print ('Error, could not scp ' + command)



# transfer one file with scp
def scp_file(host , pathfile_src , path_dst, user='root' , file_upload = True):
    success = True
    if file_upload:
        command = 'scp -r ' + pathfile_src + ' ' + user +'@' + str(host) + ':' + path_dst
        print(command)
        try:
            os.system(command)
            time.sleep(0.1)
        except:
            print ('Error, could not scp ' + pathfile_src + ' to ' + str(host) + ' to path ' + path_dst)
            success = False
    else:
        command = 'scp -r ' + user + '@' + str(host) + ':' + pathfile_src + ' ' + path_dst
        print(command)
        try:
            os.system(command)
            time.sleep(0.1)
        except:
            print('Error, could not scp ' + pathfile_src + ' to ' + str(host) + ' to path ' + path_dst)
            success = False

    return success



#   transfer  files from a list with scp
def scp_list_of_files(host, list_files, path_to):
    for file0 in list_files:
        scp_file(host, file0, path_to)


#   transfer list of files to many nodes
def scp_files_to_nodes(hosts, list_files, path_to):
    for host in hosts:
        scp_file(host, list_files, path_to)





##################################                      DOWNLOAD  FROM  INTERNET                           ######################################

#   download file
def download_file(link_src , path_to , filename):
    print('Downloading ' + link_src)
    success = False
    try:
        wget.download(link_src, path_to + filename)
        success = True
    except:
        print('Error downloading ' + link_src)
    return success


#   download a list of files
def download_files_from_list(link_list , path_to):
    success = []
    for link in link_list:
        var, filename = link.rsplit('/', 1)

        if download_file(link , path_to , filename):
            success.append(True)
        else:
            success.append(False)


def download_if_not_exist(link , path_to , filename):
    if not(e_fil.file_exists(path_to + filename)):
        download_file(link, path_to, filename)
    else:
        print('File already exist' +  path_to + filename)


def wget_download(url, save_dir, force_overwrite=False):
    try:
        wget.download(url, out=save_dir)
    except Exception as e:
        print('ERROR could not download ' + url)
        return False
    return True


##################################                                                                          ######################################





# ToDo move to functions
def cronjob_create_remote(host , cronjob):
    sshclient = createSSHClient(host)

    cron_send = 'echo ' + e_sup.string_quote(cronjob) +'>> /var/spool/cron/crontabs/root'

    print(cronjob)

    ssh_command3(sshclient, cron_send)
    sshclient.close()

    pass


# ToDo move to functions
def cronjob_create_remote_list(host , list_cronjobs_name):
    list_cronjobs = [] #e_fil.get_filelines_to_list(c.DIR_CONFIGS_LISTS, list_cronjobs_name)
    for cronjob in list_cronjobs:
        cronjob_create_remote(host, cronjob)

# ToDo move to functions
def cronjob_create_remote_nodes(hosts , list_cronjobs_name):
    for host in hosts:
        cronjob_create_remote(host, list_cronjobs_name)




def makedir_remote(host, dir0, user = e.USER_ROOT):
    command = 'mkdir -p ' + dir0
    ssh_command(host, command, 0.1, user)


# ToDo move to functions
#   make dirs remotely via ssh
def makedirs_remote_host(host, list_dir, user = e.USER_ROOT):
    for dir0 in list_dir:
        makedir_remote(host, dir0, user)


#   make dirs remotely via ssh
def makedirs_remote_hosts(hosts, list_dir, user = e.USER_ROOT):
    for host in hosts:
        for dir0 in list_dir:
            makedir_remote(host, dir0, user)



# ToDo move to functions
def remote_extract_tar(host, dir_dst , file_dst):
    sshclient = createSSHClient(host)

    command = 'cd ' + dir_dst + ';tar -xzf ' + file_dst
    command_quote = e_sup.string_quote(command)
    ssh_command3(sshclient , command_quote)

    sshclient.close()


def tar_remote_create_bash(host, pathfile_tar, DIR_TAR_src):
    command = 'tar czf ' + pathfile_tar + ' ' + DIR_TAR_src
    command_remote(host, command)


def tar_remote_extract_bash(host, pathfile_tar, dir_dst = False):
    if not dir_dst:
        command = 'tar xzf ' + pathfile_tar
        command_remote(host, command)
    else:
        pass        #ToDo



# ToDo not needed for now
def remote_create_tar(node , tar_name , tar_path):
    sshclient = createSSHClient(node)
    command = 'tar -czf ' + tar_name + ' ' + tar_path
    sshclient.close()


def service_check_host(host, host_port=22, dir_test = '/root/'):
    success = False
    if service_available(host, host_port):
        flag_put_remote(host, dir_test, e.FLAG_TESTING)
        if exists_remote(host, dir_test + e.FLAG_TESTING):
            flag_remove_remote(host, dir_test, e.FLAG_TESTING)
            success = True
    return success



def service_available(host_ip, host_port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    is_online = True
    sock.settimeout(0.02)
    try:
        sock.connect((str(host_ip), host_port))
    except:
        is_online = False

    sock.close()
    return is_online



def ips_service_available_subnet(host_port, host_ip = False):
    ips_available = []

    if host_ip == False:
        ip_first = e_sup.ip_last_octet(str(ip_mine()) , False)
    else:
        ip_first = e_sup.ip_last_octet(str(host_ip) , False)

    for i in range(1,254):
        ip_addr = ip_first + '.' + str(i)

        if service_available(ip_addr, host_port):
            ips_available.append(ip_addr)

    return ips_available



def command_remote(host ,command, sleep_seconds=0.1):

    proc_communicate = subprocess.Popen(['ssh', e.USER_ROOT + '@' + host , command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #proc_communicate = subprocess.Popen(['ssh', c.USER_ROOT + '@' + host, command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=int(timeout_seconds))

    out,err = proc_communicate.communicate()
    time.sleep(sleep_seconds)

    return out.decode("utf-8")


def command_remote2(host ,command, sleep_seconds=0.1):

    command = 'ssh ' + e.USER_ROOT + '@' + str(host) + ' ' + command #e_sup.string_quote(command)
    e_fil.execute_command(command)

    time.sleep(sleep_seconds)


def remote_filenames_in_dir(host, dir):
    command = 'ls -p ' + dir + ' | grep -v /'

    filenames = command_remote2(host ,command)
    return filenames


######################################                   KEY MANAGEMENT                    ########################################


def deploy_key(key, server, username0, password0):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(server, username=username0, password=password0)
    client.exec_command('mkdir -p ~/.ssh/')
    client.exec_command('echo "%s" > ~/.ssh/authorized_keys' % key)
    client.exec_command('chmod 644 ~/.ssh/authorized_keys')
    client.exec_command('chmod 700 ~/.ssh/')


def ssh_generate_new_key(host, pathfile_username, username = e.USER_ROOT):
    command_start = 'sshpass -f ' + pathfile_username
    #command = command_start + ' ssh ' + username + '@' + host + """ \"ssh-keygen -f /root/.ssh/id_rsa -t rsa <<<$'y\n'\""""
    #command = command_start + ' ssh ' + username + '@' + host + """ yes|ssh-keygen -t rsa"""
    #command = """ \"ssh-keygen -f /root/.ssh/id_rsa -t rsa <<<$'y\n'\""""

    if not exists_remote(host, e.DIR_SSH_ROOT + e.FILE_ID_RSA):
        command = command_start + """ ssh-keygen -N '' -f ~/.ssh/id_rsa -t rsa"""
        command_remote(host, command)


def ssh_prepare_node(host, pathfile_username, dir_sshconfigs_src, username = e.USER_ROOT):
    command_start = 'sshpass -f ' + pathfile_username
    command_next = e_sup.string_quote(' ssh ' + username + '@' + host + ' apt-get install -y sshpass')
    e_fil.execute_command(command_start + command_next, 0.1)
    # transfer good ssh_configs and restart ssh then use ssh-copy-id

    command = command_start + ' scp ' + dir_sshconfigs_src + e.FILE_SSH_CONFIG + ' ' + username + '@' + host + ':' + e.DIR_SSH_CONFIGS
    e_fil.execute_command(command, 0.1)
    command = command_start + ' scp ' + dir_sshconfigs_src + e.FILE_SSHD_CONFIG + ' ' + username + '@' + host + ':' + e.DIR_SSH_CONFIGS
    e_fil.execute_command(command, 0.1)
    command = command_start + ' ssh ' + username + '@' + host + ' systemctl restart ssh'
    e_fil.execute_command(command,0.1)

    command = command_start + ' ssh-copy-id ' + username + '@' + host
    e_fil.execute_command(command, 0.2)


def ssh_keys_setup(ip_src, ip_dst, pathfile_username, user0=e.USER_ROOT):
    command_start = 'sshpass -f ' + pathfile_username

    command = command_start + ' ssh-copy-id ' + user0 + '@' + ip_dst
    print('setting up ssh keys between ' + ip_src + ' and ' + ip_dst)
    command_remote(ip_src, command)


def ssh_setup_keys_all(hosts, pathfile_username, user0=e.USER_ROOT):
    for host_src in hosts:
        for host_dst in hosts:
            ssh_keys_setup(host_src, host_dst, pathfile_username, user0)

def setup_ssh_keys_node_to_others(host, hosts, pathfile_username, user0=e.USER_ROOT):
    for host_dst in hosts:
        ssh_keys_setup(host, host_dst, pathfile_username, user0)
    for host_src in hosts:
        ssh_keys_setup(host_src, host, pathfile_username, user0)


'''
def setup_ssh_keys_master(host):
    print('setting up ssh keys from master to ' + host)
    setup_host_keys_node(host)

def setup_ssh_keys_master_all(hosts):
    # setup for all ips
    for host in hosts:
        try:
            setup_host_keys_master(host)
        except:
            pass
'''

##########################################################################################


###########################                   FLAGS                     ######################

def flag_put_remote(host, dir_dst, flagname):
    if not exists_remote(host, dir_dst + flagname):
        command = 'touch ' + dir_dst + flagname
        command_remote(host, command)
        print('put flag ' + dir_dst + flagname + ' on host ' + str(host))

        #if exists_remote(host, dir_dst + flagname):


def flag_remove_remote(host, dir_dst, flagname):
    if exists_remote(host, dir_dst + flagname):
        command = 'rm ' + dir_dst + flagname
        command_remote(host, command)

        print('removed flag ' + dir_dst + flagname + ' on host ' + str(host))


def flag_exists_remote(host, dir_dst, flagname):
    if exists_remote(host, dir_dst + flagname):
        return True
    else:
        return False






##############################################################################################





'''
key = open(os.path.expanduser('~/.ssh/id_rsa.pub')).read()
username = os.getlogin()
password = getpass()
hosts = ["hostname1", "hostname2", "hostname3"]
for host in hosts:
    deploy_key(key, host, username, password)
    
    -----------------
    
for server in `cat server.txt`;  
do  
    sshpass -p "password" ssh-copy-id -i ~/.ssh/id_rsa.pub user@$server  
done
    
'''



def exists_remote(host, pathfile, type_resource = e.TYPE_FILE):
    if type_resource == e.TYPE_FILE:
        status = subprocess.call(['ssh', host, 'test -f {}'.format(pipes.quote(pathfile))])
    #elif type == e.TYPE_DIR:
    #    status = subprocess.call(['ssh', host, '[ -d ' + path + '] ' + 'echo 0])
    else:
        return False

    if status == 0:
        return True
    if status == 1:
        return False

    return False
    #return e.VALUE_ERROR



def rm_dir_remote(host, dir, inside = False):
    command = 'rm -rf ' + dir

    if inside:
        command_= command + '*'

    command_remote(host, command)


def rm_file_remote(host, dir, filename):
    command = 'rm -f ' + dir + filename

    command_remote(host, command)


def node_reboot(host):
    command = 'init 6'
    command_remote(host, command)


def file_remove_remote(host, pathfile):
    if exists_remote(host, pathfile):
        command = 'rm -f ' + pathfile
        command_remote2(host, command)
    if exists_remote(host, pathfile):
        return False
    else:
        return True

def file_remove_remote2(host, dir_src, file_src):
    pathfile = e_fil.pathfile_make(dir_src, file_src)
    file_remove_remote(host, pathfile)
    if exists_remote(host, pathfile):
        return False
    else:
        return True

def file_copy_remote(host, dir_src, file_src, dir_dst, file_dst = e.VALUE_DEFAULT):
    pathfile_src = e_fil.pathfile_make(dir_src, file_src)
    if file_dst == e.VALUE_DEFAULT:
        pathfile_dst = e_fil.pathfile_make(dir_dst, file_src)
    else:
        pathfile_dst = e_fil.pathfile_make(dir_dst, file_dst)

    command = 'cp -f ' + pathfile_src + ' ' + pathfile_dst
    command_remote(host, command)

    if exists_remote(host, pathfile_dst):
        return True
    else:
        return False

def file_move_remote(host, dir_src, file_src, dir_dst, file_dst = e.VALUE_DEFAULT):
    pathfile_src = e_fil.pathfile_make(dir_src, file_src)
    if file_dst == e.VALUE_DEFAULT:
        pathfile_dst = e_fil.pathfile_make(dir_dst, file_src)
        file_dst = file_src
    else:
        pathfile_dst = e_fil.pathfile_make(dir_dst, file_dst)

    if exists_remote(host, pathfile_src):
        file_copy_remote(host, dir_src, file_src, dir_dst, file_dst)

        #   check if success
        if file_remove_remote(host, pathfile_src):
            if exists_remote(host, pathfile_dst):
                return True
            else:
                return False
        else:
            return False
    else:
        print('File to move does not exist')
        return False



