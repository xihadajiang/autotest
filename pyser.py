#coding:gbk
import socket, logging
host='127.0.0.1'
port=8080
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))

def getTraceStackMsg():
    tb = sys.exc_info()[2]
    msg = ''
    for i in traceback.format_tb(tb):
        msg += i
    return msg
##################user config ##################
logger = logging.getLogger("/home/p2p/apache-tomcat-6.0.9/logs/network-server")
#############################################
def InitLog():
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler("network-server.log")
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

InitLog()
logger.error("create socket failed")

def FindHostPort(datas):
    host_s = -1
    host_e = -1
    host_str = None
    host = ""
    port = ""
    if not datas.startswith("CONNECT"):
        host_s = datas.find("Host:")
        if host_s < 0:
            host_s = datas.find("host:")
        if host_s > 0:
            host_e = datas.find("\r\n", host_s)
        if host_s > 0 and host_e > 0:
            host_str = datas[host_s+5:host_e].strip()
            add_list = host_str.split(":")
            if len(add_list) == 2:
                host = add_list[0]
                port = add_list[1]
            else:
                host = add_list[0]
                port = 80
            first_seg = datas.find("\r\n")
            first_line = datas[0:first_seg]
            first_line = first_line.replace(" http://%s" % host_str, " ")
            datas = first_line + datas[first_seg:]
    else:
        first_seg = datas.find("\r\n")
        head_e = datas.find("\r\n\r\n")
        if first_seg > 0 and head_e > 0:
            first_line = datas[0:first_seg]
            com,host_str,http_version = re.split('\s+', first_line)
            add_list = host_str.split(":")
            if len(add_list) == 2:
                host = add_list[0]
                port = add_list[1]
            else:
                host = add_list[0]
                port = 443
            host_s = 1
            host_e = 1
    return host_str,host_s,host_e,host,port,datas
 
content="""HTTP/1.0 200 OK
Content-Type:text/html
<html>
<h1>hello world</h1>
<br /> <a href="http://www.baidu.com">baidu</a>
</html>"""
txt_content_head = """HTTP/1.0 200 OK
Content-Type:text/html

"""
#f = open('query.htm','r')
#txt_content = txt_content_head + f.read()
pic_content_head = """HTTP/1.0 200 OK
Content-Type:image/jpg

"""
#f = open(r'D:\学习资料\python程序\未分类\kankancai\BAE版\kankancai\favicon.ico','rb')
#pic_content = pic_content_head + f.read()
f.close()
def readfile(filename):
    BUF_SIZE = 4
    bigfile = open(filename,'r') 
    tmp_lines = bigfile.readlines(BUF_SIZE) 
    while tmp_lines: 
       for line in tmp_lines:
            print line
       tmp_lines = bigfile.readlines(BUF_SIZE) 
import read_last_file
lines = read_last_file.get_last_n_lines('/home/p2p/apache-tomcat-6.0.9/logs/catalina.out', 50)
cont = txt_content_head + "<html><head><style type='text/css'><!--body { line-height: 10pt; font-size: 10pt}--></style></head><body bgcolor='#c0c0c0'><a href='http://127.0.0.1/log/'><font color = '#0000ff'>主页</font></a><br><br>"
for line in lines:
    cont = cont + "<font color='#000000'>%s</font><br></b>\n"%line
cont = cont + '</body></head></html>'
while 1:
    s.listen(1)
    clientsock,clientaddr = s.accept()
    #process the connection
    print clientsock,clientaddr
    print ("Got connection from", clientsock.getpeername())
    data = clientsock.recv(4096)
    print data
    if len(data) > 2:
        method = data.split(' ')[0]
        src = data.split(' ')[1]
        if method == 'GET':
            if src == '/test':
                content = pic_content
            elif src == '/log':
                content = cont
            elif src == '/--GAPS-LOGVIEW--':
                url = data.split(' ')[-1]
                content = txt_content
                print url,'url\n'
            else:
                content = txt_content
                print src
        elif method == 'POST':
            if src == '/--GAPS-LOGVIEW--':
                url = data.split(' ')[-1]
                content = txt_content
                print url,'url\n'
            else:
                content = txt_content
                print src
        print FindHostPort(data),'ppppppppppppp'
    print data
    n=clientsock.send(content)
    clientsock.close()