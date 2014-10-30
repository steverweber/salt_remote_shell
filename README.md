salt_remote_shell
=================

**My development has halted, no time :(**


salt remote shell tty hacking

this is crap and unsafe! dont use in production!

Next steps
 - use salt as the communication transport vs directly using socket.
   - perhaps salt creates a /var/salt/minion_streams/minionid_cmdpid.socket
 - creating salt-tty to automate standing and connecting to remote program stream
 - support terminal things like changing screensize, keyboard cmds like ctrl+c


perhaps helpfull to review:
 - https://github.com/saltstack/salt/blob/develop/salt/utils/vt.py
 

master or frontend runs
----------------------------
```
nc -l 4444
```
or use python as the shell...but my code blocks and dont work :(

```
cat > srv.py <<EOF
import socket, sys, time
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 4444))
s.listen(1)
(conn, addr) = s.accept()
print 'Connected by', addr
## blocks :(
sys.stdout = conn.makefile("r")
sys.stdin = conn.makefile("w", 0)
while 1:
   time.sleep(1)
EOF
python srv.py
```





minion runs somthing like
----------------------------
```
# run program (bash, sh, cmd, powershell)
cat > srv_shell_ep.py <<EOF
import socket, subprocess
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('salt.host', 4444))
pip = s.makefile("rw")
p = subprocess.call("/bin/bash -i".split(' '), stdin=pip, stdout=pip, stderr=pip)
EOF
python srv_shell_ep.py
```
