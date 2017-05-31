import os
import paramiko
from scp import SCPClient
from config import host

def ssh_execute(cmd, host=host):
    """
    INPUT:
    cmd = 'ls -la /home/deploy/'
    host = {
        'hostname': '172.0.0.1',  # Ensure host works in ssh
        'user': 'someone', 
        'pwd': 'secret'
    } 
    
    OUTPUT:
    ================================================================================
    [INFO]
    someone@172.0.0.1
    [EXECUTE]
    ls -la /home/
    [Output]
    total 16
    drwxr-xr-x  4 root   root   4096 May  8 17:20 .
    drwxr-xr-x 24 root   root   4096 May 17 08:59 ..
    drwxr-xr-x 11 deploy deploy 4096 May 26 13:31 deploy
    """
    def print_ouput(in_out_err_turple):
        def to_string(std):
            return(str(std.read().decode('utf-8').strip()))
        def have_(std_string):
            if len(std_string)>0:
                return std_string
            else:
                return None
        stdin, stdout, stderr = (in_out_err_turple)
        stdout_string = to_string(stdout)
        stderr_string = to_string(stderr)
        if have_(stdout_string):
            print('[Output]\n{}\n'.format(stdout_string))
        if have_(stderr_string):
            print('[Error]\n{}\n'.format(stderr_string))
    
    
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host['hostname'], username=host['user'], password=host['pwd'])
        print('='*80)
        print('[INFO]\n{}\n'.format(host['user']+'@'+host['hostname']))
        print('[EXECUTE]\n{}\n'.format(cmd))
        print_ouput(ssh.exec_command(cmd))


def scp_put_file(local_path, remote_path, host=host, recursive=False):
    """
    INPUT:
    local_path = './data'
    remote_path = '/home/deploy/'
    host = {
        'hostname': '172.0.0.1',  # Ensure host works in ssh
        'user': 'someone', 
        'pwd': 'secret'
    }
    
    OUTPUT:
    ================================================================================
    [Put]
    ./data
    [To]
    someone@172.0.0.1:/home/deploy/
    """
    def print_output():
        print('='*80)
        print('[Put]')

        if isinstance(local_path, list):
            for f in local_path:
                print(f)
        else:
            print(local_path)
            
        print('\n[To]')
        print('{info}:{remote_path}\n'.format(info=host['user']+'@'+host['hostname'],
                                              remote_path=remote_path))

    
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host['hostname'], username=host['user'], password=host['pwd'])
        
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(local_path, remote_path, recursive=recursive)
            print_output()

if __name__ == '__main__':
    from datetime import datetime
    local_path = './data/{}'.format(datetime.strftime(datetime.now(), '%Y%m%d'))
    remote_path = '/volume1/dstore/Projects/GDELT/gdelt-keywords/data/'

    scp_put_file(local_path, remote_path, recursive=True)

