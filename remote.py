__virtualname__ = 'remote'

import socket
import subprocess
import multiprocessing

'''
copy file(s) to:
/srv/salt/base/_modules/remote

run:
salt-call saltutil.sync_all
'''

def _run_proccess(queue, cmd, remote_system, remote_port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((remote_system, remote_port))
    except socket.error as msg:
        s.close()
        msg = "connect error: you must first run 'nc -l {1}' on {0}".format(remote_system, remote_port)
        queue.put(msg)
        return 
    pip = s.makefile("rw")
    p = subprocess.call(cmd.split(' '), stdin=pip, stdout=pip, stderr=pip)
    queue.put('command finished')


def shell_unsafe(cmd='/bin/bash -i', remote_system=None, remote_port=4444):
    '''
    starts streaming a program to a remote server.
    traffic is in clear text and unsafe!
    
    first start a listen on the remote system:
        nc -l 4444
    
    args:
        cmd='/bin/sh -i'
        cmd='cmd.exe'
    '''
    if not remote_system:
        remote_system = __opts__['master']
    queue = multiprocessing.Queue()
    ps = multiprocessing.Process(target=_run_proccess, args=(queue, cmd, remote_system, remote_port))
    ps.start()
    pid = ps.pid
    msg = 'pid {3} streaming {0} to {1}:{2}'.format(cmd, remote_system, remote_port, pid)
    try:
        msg = queue.get(timeout=0.5)
    except Exception:
        pass
    return msg
