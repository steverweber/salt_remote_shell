salt_remote_shell
=================

salt remote shell tty hacking


master or frontend runs
----------------------------
```
nc -l 4444
```
or wip

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





minion runs
----------------------------
```
# run program (bash, sh, cmd, powershell)
cat > srv_shell_ep.py <<EOF
## deamon
import socket, subprocess
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('salt.host', 4444))
pip = s.makefile("rw")
p = subprocess.call("/bin/bash -i".split(' '), stdin=pip, stdout=pip, stderr=pip)
EOF
python srv_shell_ep.py
```
