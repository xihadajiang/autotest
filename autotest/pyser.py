#coding:utf-8
import socket
from const import *
from log_lp import *
from views import *
from urls import *
from utils import *

import datetime
today = datetime.datetime.today()
rq = today.strftime('%Y%m%d')

host=HOST
port=PORT
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))

def getTraceStackMsg():
    tb = sys.exc_info()[2]
    msg = ''
    for i in traceback.format_tb(tb):
        msg += i
    return msg
    
logger = InitLog(LOGPATH)
logger.error("create socket failed")
txt_content_head = """HTTP/1.0 200 OK
Content-Type:text/html

"""
while 1:
    s.listen(1)
    clientsock,clientaddr = s.accept()
    #print ("Got connection from", clientsock.getpeername())
    data = clientsock.recv(4096)
    if len(data) > 2:
        req = datatoreq(data)
        if 'index_files' in req.get('url'):
            if '.png' in req.get('url') or '.gif' in req.get('url') or '.jpg' in req.get('url'):
                content = getimage(".%s"%req.get('url'))
            else:
                content = getformfile(".%s"%req.get('url'))
        else:
            str2 = url.get(req.get('url'))
            if str2:
                c2 = compile(str2+'(req)','','eval')        # 编译为表达式 
                content = eval(c2)                    # 执行
            else:
                ht_404 = "输入url:%s不存在，请使用以下url:<br>"%req.get('url')
                for k,v in url.items():
                    ht_404 = ht_404 + "%s<br>"%k
                content = txt_content_head + ht_404
            content =   content
    try:
        n=clientsock.send(content)
    except:
        n=clientsock.send(content.encode('gbk'))
    clientsock.close()