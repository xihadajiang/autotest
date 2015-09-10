#coding:gbk
import socket
#from const import *
#from log_lp import *
import datetime
today = datetime.datetime.today()
rq = today.strftime('%Y%m%d')

host=HOST
port=PORT
host='192.168.30.137'
port=8008
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))
content = """HTTP/1.0 200 OK
Content-Type:text/html
<html>
<h1>hello world</h1>
<br /> <a href="http://www.baidu.com">baidu</a>
</html>"""

while 1:
    s.listen(1)
    clientsock,clientaddr = s.accept()
    data = clientsock.recv(4096)
    if len(data) > 2:
        print data
        lport = data.split(' ')[1].split('/')[1]
        lhost,lport_1 = data.split()[4].split(':')
        print lhost,'---------------',lport_1
        print lport
        if lport.isdigit():
            data_r = data.replace('/%s'%lport,'').replace(str(PORT),lport)
            print data_r
            tgt_ip = lhost
            tgt_port = int(lport)
        else:
            tgt_ip = lhost
            tgt_port = int(lport_1)
            data_r = data
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
        sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)      
        sock.connect( ( tgt_ip , tgt_port ) )
        head = sock.send( data_r )
        content = sock.recv(int(head))
        print content
    n=clientsock.send(content)
    clientsock.close()