#coding:gbk
import socket, logging
from const import *
import datetime
today = datetime.datetime.today()
rq = today.strftime('%Y%m%d')

host=HOST
port=PORT
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
s.bind((host,port))

iso85 = {
0   :"��Ϣ����"                    , 
1   :"λͼ"                        , 
2   :"���˺�"                      , 
3   :"���״�����"                  , 
4   :"���׽��"                    , 
5   :"NO USE"                      , 
6   :"NO USE"                      , 
7   :"�������ں�ʱ��"              , 
8   :"NO USE"                      , 
9   :"NO USE"                      , 
10  :"NO USE"                      , 
11  :"�ܿ���ϵͳ���ٺ�"            , 
12  :"�ܿ������ڵ�ʱ��"            , 
13  :"�ܿ������ڵ�����"            , 
14  :"����Ч��"                    , 
15  :"��������"                    , 
16  :"NO USE"                      , 
17  :"��ȡ����"                    , 
18  :"�̻�����"                    , 
19  :"NO USE"                      , 
20  :"NO USE"                      , 
21  :"NO USE"                      , 
22  :"��������뷽ʽ��"            , 
23  :"�����к�"                    , 
24  :"NO USE"                      , 
25  :"�������������"              , 
26  :"�����PIN��ȡ��"             , 
27  :"NO USE"                      , 
28  :"field27"                     , 
29  :"NO USE"                      , 
30  :"NO USE"                      , 
31  :"NO USE"                      , 
32  :"������ʶ��"                , 
33  :"��Ȩ������ʶ��"              , 
34  :"NO USE"                      , 
35  :"2�ŵ�����"                   , 
36  :"3�ŵ�����"                   , 
37  :"�����ο���"                  , 
38  :"��Ȩ��ʶӦ����"              , 
39  :"Ӧ����"                      , 
40  :"NO USE"                      , 
41  :"�ܿ����ն˱�ʶ��"            , 
42  :"�ܿ�����ʶ��"                , 
43  :"�տ��̻�λ��"                , 
44  :"������Ӧ����"                , 
45  :"NO USE"                      , 
46  :"NO USE"                      , 
47  :"field47"                     , 
48  :"˽�и�������"                , 
49  :"���׻��Ҵ���"                , 
50  :"������Ҵ���"                , 
51  :"NO USE"                      , 
52  :"���˱�ʶ��PIN"               , 
53  :"��ȫ������Ϣ"                , 
54  :"���ӽ��"                    , 
55  :"IC��������"                  , 
56  :"NO USE"                      , 
57  :"NO USE"                      , 
58  :"PBOC����Ǯ����׼������Ϣ"    , 
59  :"NO USE"                      , 
60  :"�Զ�����"                    , 
61  :"ԭʼ��Ϣ��"                  , 
62  :"�Զ�����"                    , 
63  :"�Զ�����"                    , 
64  :"��Ϣȷ����"                  , 
65  :"NO USE"                      , 
66  :"NO USE"                      , 
67  :"NO USE"                      , 
68  :"NO USE"                      , 
69  :"NO USE"                      , 
70  :"������Ϣ��"                  , 
71  :"NO USE"                      , 
72  :"NO USE"                      , 
73  :"NO USE"                      , 
74  :"���ǽ��ױ���"                , 
75  :"�����Զ��������ױ���"        , 
76  :"��ǽ��ױ���"                , 
77  :"����Զ��������ױ���"        , 
78  :"ת�ʽ��ױ���"                , 
79  :"ת���Զ��������ױ���"        , 
80  :"��ѯ���ױ���"                , 
81  :"��Ȩ���ױ���"                , 
82  :"NO USE"                      , 
83  :"���ǽ��׷ѽ��"              , 
84  :"NO USE"                      , 
85  :"��ǽ��׷ѽ��"              , 
86  :"���ǽ��׽��"                , 
87  :"�����Զ��������"            , 
88  :"��ǽ��׽��"                , 
89  :"����Զ��������׽��"        , 
90  :"ԭ���׵�����Ԫ��"            , 
91  :"�ļ��޸ı���"                , 
92  :"NO USE"                      , 
93  :"NO USE"                      , 
94  :"����ָʾ��"                  , 
95  :"������"                    , 
96  :"NO USE"                      , 
97  :"��������"                  , 
98  :"NO USE"                      , 
99  :"���������"                  , 
100 :"���ջ�����"                  , 
101 :"�ļ���"                      , 
102 :"�ʺ�1"                       , 
103 :"�ʺ�2"                       , 
104 :"NO USE"                      , 
105 :"NO USE"                      , 
106 :"NO USE"                      , 
107 :"NO USE"                      , 
108 :"NO USE"                      , 
109 :"NO USE"                      , 
110 :"NO USE"                      , 
111 :"NO USE"                      , 
112 :"NO USE"                      , 
113 :"NO USE"                      , 
114 :"NO USE"                      , 
115 :"NO USE"                      , 
116 :"NO USE"                      , 
117 :"NO USE"                      , 
118 :"NO USE"                      , 
119 :"NO USE"                      , 
120 :"NO USE"                      , 
121 :"NO USE"                      , 
122 :"NO USE"                      , 
123 :"����������"                  , 
124 :"NO USE"                      , 
125 :"NO USE"                      , 
126 :"NO USE"                      , 
127 :"NO USE"                      , 
128 :"��Ϣȷ����"                   
}
def getTraceStackMsg():
    tb = sys.exc_info()[2]
    msg = ''
    for i in traceback.format_tb(tb):
        msg += i
    return msg
##################user config ##################
logger = logging.getLogger(LOGPATH)
#############################################
def InitLog():
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(LOGPATH)
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

def fmt(datas):
    jyzd = {}
    req = datas.split('\n')
    for line in req:
        if 'Host:' in line:
            add_list = line.split(":")
            print add_list,'add_list'
            if len(add_list) >= 2:
                host = add_list[1]
                port = add_list[2]
            else:
                host = add_list[1]
                port = '80'
            jyzd['Host'] = host.strip()
            jyzd['Port'] = port.strip()
        elif ': ' in line:
            k,v = line.split(': ')
            jyzd[k] = v.strip()
    return jyzd
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
def logindex():
    f = open(INDEX_HTML,'r')
    txt_content = txt_content_head + f.read().replace('20050101',rq)
    f.close()
    return  txt_content
pic_content_head = """HTTP/1.0 200 OK
Content-Type:image/jpg

"""
def image():
    f = open(r'D:\ѧϰ����\python����\δ����\kankancai\BAE��\kankancai\favicon.ico','rb')
    pic_content = pic_content_head + f.read()
    f.close()
    return pic_content
def mon(req,jyzd):
    fml = {}
    import urllib
    req = urllib.unquote(req)
    req = req.split('\n')[-1]
    for key_value in req.split('&'):
        if '=' in key_value:
            k,v = key_value.split('=')
            fml[k] = v
    logname = fml.get( 'logname' , '' )
    if logname !='':
        sysname ,monname , n = logname.split('@')
    else:
        sysname ,monname , n = "","",""
    lsh = fml.get( 'lsh' , '' )
    backbs = fml.get( 'backbs' , '' )
    logmode = fml.get( 'logmode' , '' )
    listtime = fml.get( 'listtime' , '' )
    logdate = fml.get( 'logdate' , '' )
    href="http://%s:%s/getlog?mode=%s&date=%s&log=%s&lsh="%(jyzd.get('Host','127.0.0.1'),jyzd.get('Port','8080'),logmode,logdate,sysname)
    now = datetime.datetime.now()
    err = ''
#    if len(log_list) < 3:
#        err =u" ����ܾ�����ǰ��ϵͳ[%s]ָ���ļ����Դ��Ϊ��,���޸�query.htm��Ϊ%s@XXX@Nģʽָ�������Դ��,��ˮ���ֶ����"%(log_list[0],log_list[0])
#        return err
    result =txt_content_head + "<html><head><style type='text/css'><!--body { line-height: 10pt; font-size: 10pt}--></style></head><body bgcolor='#c0c0c0'><a href='http://138.138.2.130:8105/'><font color = '#0000ff'>��ҳ</font></a><br>"
    try:
        f = open(MONPATH + r'\%s\%s.mon'%(logdate,monname),'r')
        content = f.readlines()
        for line in content:
#&nbsp;&nbsp;-->20140707|131026|<a href='http://138.138.2.130:8105/getlog?mode=1&date=20140413&log=sys_smqt&lsh=10461'>10461|</a>300001|ģ����ѯ������ʶ��|||||000000|��ѯ�ɹ�|191|
            t=""
            #print line
            line_list = line.split('|')
            line_list[int(n)-1] =  "<a href='%s%s'>%s</a>"%(href,line_list[int(n)-1],line_list[int(n)-1])
            t = "&nbsp;&nbsp;-->"+'|'.join(line_list) + "<br>"
            result = result + t
    except:
        err =  "open mon [D:\Django\data\mon\%s\%s.mon] failed"%(logdate,monname)
    return result + "</body></head></html>"
def getlog(req,jyzd):
    fml = {}
    import urllib
    req = urllib.unquote(req)
    req = req.split('?')[-1]
    for key_value in req.split('&'):
        if '=' in key_value:
            k,v = key_value.split('=')
            fml[k] = v
    log = fml.get( 'log' , '' )
    date = fml.get( 'date' , '' )
    lsh = fml.get( 'lsh' , '' )
    lsh = lsh.replace('$','')
    filename = LOG + r'\%s\%s_%s.log'%(date,log,date)
    nr = getcontent(filename,date,lsh)
#    now = datetime.datetime.now()
#    f = open(LOG + r'\%s\%s_%s.log'%(date,log,date),'r')
#    content = f.read()
#    #print content
#    import re
#    p = re.compile(r'<<\[\d+\]BUFF')
#    contents = p.split(content)
#    i = 0
    res = txt_content_head + """<html><head><style type='text/css'><!--body { line-height: 10pt; font-size: 10pt}--></style></head><body bgcolor='#c0c0c0'><a href='http://%s:%s/log/'><font color = '#0000ff'>��ҳ</font></a><br><br>
<a href='http://%s:%s/getbw/?mode=1&date=%s&log=%s&lsh=%s'><font color = '#0000ff'>�鿴����</font></a><br><br>"""%(jyzd.get('Host','127.0.0.1'),jyzd.get('Port','8080'),jyzd.get('Host','127.0.0.1'),jyzd.get('Port','8080'),date,log,lsh)
#    for line in contents:
#        i = i + 1
#        if '��ǰ��ˮ��=[' + str(lsh) in line:
#            import re
#            nr = line.split('\n')
    for j in nr:
        try:
            #j = j.decode('gb2312')
            j = j.replace('>','&gt;')
            j = j.replace('<','&lt;')
            if "[ִ�����:[" in j and "������н��״̬:[0]" in j :
                t = "<font color='#0000ff'>%s</font><br></b>"%j
            elif  "[ִ�����:[" in j and "������н��״̬:[1]" in j:
                t = "<font color='#ff00ff'>%s</font><br></b>"%j
            elif  "[ִ�����:[" in j and "������н��״̬:[-1]" in j :
                t = "<font color='#ff0000'>%s</font><br></b>"%j
            else :
                t = "<font color='#000000'>%s</font><br></b>"%j
        except:
            t = j
        res = res + t
    return res + "</body></head></html>"
def getbw(req):
    fml = {}
    import urllib
    req = urllib.unquote(req)
    req = req.split('?')[-1]
    for key_value in req.split('&'):
        if '=' in key_value:
            k,v = key_value.split('=')
            fml[k] = v
    log = fml.get( 'log' , '' )
    date = fml.get( 'date' , '' )
    lsh = fml.get( 'lsh' , '' )
    lsh = lsh.replace('$','')
    filename = LOG + r'\%s\%s_%s.log'%(date,log,date)
    nr = getcontent(filename,date,lsh)
    res = txt_content_head + """<html><head><style type='text/css'><!--body { line-height: 10pt; font-size: 10pt}--></style></head><body bgcolor='#c0c0c0'><a href='http://{{host}}/log/'><font color = '#0000ff'>��ҳ</font></a><br><br>
<a href='http://{{host}}/getbw/?mode=1&date=%s&log=%s&lsh=%s'><font color = '#0000ff'>�鿴����</font></a><br><br>"""%(date,log,lsh)
    import re
    import iso8583
    #import xmlext
    bwsx = ['��������-sys_smqt-������','--�ӳ���������������--','--�ӳ���������Ӧ����--','��������-sys_smqt']
    for line in nr:
        for sx in bwsx:
            p1 = re.compile(r'\]%s'%sx)
            bw = p1.split(line)
            if len(bw) > 1:
                bw = bw[1].split(']')[0]
                bw = bw.split('[')[1]
                if '����' in sx:
                    bw_dict = iso8583.unpack8583(bw.decode('gb2312'))
                    print bw_dict
                    bw_dict = iso8583.unpack8583(bw.decode('gb2312'))[1]
                    d_tmp = {}
                    for k,v in bw_dict.items():
                        kk = '��[%3s]%s'%(k,iso85.get(k))
                        d_tmp[kk.decode('gb2312')] = v
                    bw_dict = d_tmp
                    bw_dict = sorted(bw_dict.items(), key=lambda bw_dict:bw_dict[0])
                else:
                    print 'ppp'
                    #bw_dict = xmlext.xmltojyzd(bw)
                    #bw_dict = sorted(bw_dict.items(), key=lambda bw_dict:bw_dict[0])
                #d = {sx.decode('gb2312'):bw_dict}
    return res + "</body></head></html>"

def getcontent(filename,rq,lsh):
    BUF_SIZE = 1024
    bigfile = open(filename,'r') 
    tmp_lines = bigfile.readlines(BUF_SIZE) 
    content = []
    flag = 0
    tmp_content = []
    tmp_flag = 0
    while tmp_lines: 
        i = 0
        for line in tmp_lines:
            #print line
            if flag == 0:
                if "--------------��ʼ�ּ���־" in line:
                    tmp_flag = 1
                    tmp_content = []
                elif '��ǰ��ˮ��=[5511' in line:
                    flag = 1
                    content = tmp_content
                tmp_content.append(line)
            else:
                if "--------------�ύ������־" in line:
                    content.append(line)
                    return content
                else:
                    content.append(line)
            i = i + 1
        tmp_lines = bigfile.readlines(BUF_SIZE)
    bigfile.close()
    return content
def readfile(filename):
    BUF_SIZE = 4
    bigfile = open(filename,'r') 
    tmp_lines = bigfile.readlines(BUF_SIZE) 
    while tmp_lines: 
       for line in tmp_lines:
            print line
       tmp_lines = bigfile.readlines(BUF_SIZE) 
import read_last_file
lines = read_last_file.get_last_n_lines('network-server.log', 5)
cont = txt_content_head + "<html><head><style type='text/css'><!--body { line-height: 10pt; font-size: 10pt}--></style></head><body bgcolor='#c0c0c0'><a href='http://127.0.0.1/log/'><font color = '#0000ff'>��ҳ</font></a><br><br>"
for line in lines:
    cont = cont + "<font color='#000000'>%s</font><br></b>\n"%line
cont = cont + '</body></head></html>'
while 1:
    s.listen(1)
    clientsock,clientaddr = s.accept()
    print ("Got connection from", clientsock.getpeername())
    data = clientsock.recv(4096)
    if len(data) > 2:
        jyzd = fmt(data)
        method = data.split(' ')[0]
        src = data.split(' ')[1]
        if method == 'GET':
            if src == '/test':
                content = image()
            elif '/getlog'in src :
                content = getlog(src,jyzd)
            elif '/getbw'in src :
                content = getbw(src)
            elif src == '/log':
                content = logindex()
            elif src == '/--GAPS-LOGVIEW--':
                url = data.split(' ')[-1]
                content = logindex()
                print url,'url\n'
            else:
                content = logindex()
                print src
        elif method == 'POST':
            if src == '/--GAPS-LOGVIEW--':
                url = data.split(' ')[-1]
                content = mon(url,jyzd)
                print url,'url\n'
            else:
                content = logindex()
                print src
    n=clientsock.send(content)
    clientsock.close()