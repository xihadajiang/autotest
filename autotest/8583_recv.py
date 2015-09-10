# coding: gbk
import socket
import re
import struct
from iso8583 import *
import os
import threading
import binascii
from log_lp import *
from const import *
logger = InitLog(LOGPATH)
logger.error("create socket failed")

#��ʽ����(�������Ƿ�䳤��־0-�� 2-2λ�䳤 3-3λ�䳤 �������򳤶ȣ��䳤�ֱ�Ϊ99 999 ��
#�������ͣ�0-string 1-int 2-binary , �������ͣ�BCD BIN ASC ����BCD���룬���Ⱦ�Ϊ�Ҷ��룬����LΪ����룬RΪ�Ҷ���)
#YL2_8583 = {
ISO8583 = {
0   :("��Ϣ����"                    , 0 , 4     , 0 , 'BCDL')    ,
1   :("λͼ"                        , 0 , 8     , 2 , 'BIN')    ,
2   :("���˺�"                      , 2 , 19    , 0 , 'BCDL')    ,
3   :("���״�����"                  , 0 , 6     , 0 , 'BCDL')    ,
4   :("���׽��"                    , 0 , 12    , 1 , 'BCDL')    ,
5   :("NO USE"                      , 0 , 12    , 0 , '')   ,
6   :("NO USE"                      , 0 , 12    , 0 , '')   ,
7   :("�������ں�ʱ��"              , 0 , 10    , 0 , '')   ,
8   :("NO USE"                      , 0 , 8     , 0 , '')   ,
9   :("NO USE"                      , 0 , 8     , 0 , '')   ,
10  :("NO USE"                      , 0 , 8     , 0 , '')   ,
11  :("�ܿ���ϵͳ���ٺ�"            , 0 , 6     , 1 , 'BCDL')    ,
12  :("�ܿ������ڵ�ʱ��"            , 0 , 6     , 0 , 'BCDL')    ,
13  :("�ܿ������ڵ�����"            , 0 , 4     , 0 , 'BCDL')    ,
14  :("����Ч��"                    , 0 , 4     , 0 , 'BCDL')    ,
15  :("��������"                    , 0 , 4     , 0 , 'BCDL')    ,
16  :("NO USE"                      , 0 , 4     , 0 , '')   ,
17  :("��ȡ����"                    , 0 , 4     , 0 , '')   ,
18  :("�̻�����"                    , 0 , 4     , 0 , '')   ,
19  :("NO USE"                      , 0 , 3     , 0 , '')   ,
20  :("NO USE"                      , 0 , 3     , 0 , '')   ,
21  :("NO USE"                      , 0 , 3     , 0 , '')   ,
22  :("��������뷽ʽ��"            , 0 , 3     , 0 , 'BCDL')    ,
23  :("�����к�"                    , 0 , 3     , 0 , 'BCDR')    ,
24  :("NO USE"                      , 0 , 3     , 0 , '')   ,
25  :("�������������"              , 0 , 2     , 0 , 'BCDL')    ,
26  :("�����PIN��ȡ��"             , 0 , 2     , 0 , 'BCDL')    ,
27  :("NO USE"                      , 0 , 1     , 0 , '')   ,
28  :("field27"                     , 0 , 6     , 0 , '')   ,
29  :("NO USE"                      , 1 , 8     , 0 , '')   ,
30  :("NO USE"                      , 1 , 8     , 0 , '')   ,
31  :("NO USE"                      , 1 , 8     , 0 , '')   ,
32  :("������ʶ��"                , 2 , 11    , 0 , 'BCDL')    ,
33  :("��Ȩ������ʶ��"              , 2 , 11    , 0 , '')   ,
34  :("NO USE"                      , 2 , 28    , 0 , '')   ,
35  :("2�ŵ�����"                   , 2 , 37    , 0 , 'BCDL')    ,
36  :("3�ŵ�����"                   , 3 , 104   , 0 , 'BCDL')    ,
37  :("�����ο���"                  , 0 , 12    , 0 , 'ASC')    ,
38  :("��Ȩ��ʶӦ����"              , 0 , 6     , 0 , 'ASC')    ,
39  :("Ӧ����"                      , 0 , 2     , 0 , 'ASC')    ,
40  :("NO USE"                      , 0 , 3     , 0 , '')   ,
41  :("�ܿ����ն˱�ʶ��"            , 0 , 8     , 0 , 'ASC')    ,
42  :("�ܿ�����ʶ��"                , 0 , 15    , 0 , 'ASC')    ,
43  :("�տ��̻�λ��"                , 0 , 40    , 0 , '')   ,
44  :("������Ӧ����"                , 2 , 25    , 0 , 'ASC')    ,
45  :("NO USE"                      , 2 , 76    , 0 , '')   ,
46  :("NO USE"                      , 3 , 999   , 0 , '')   ,
47  :("field47"                     , 3 , 999   , 0 , '')   ,
48  :("˽�и�������"                , 3 , 999   , 0 , 'BCDL')    ,
49  :("���׻��Ҵ���"                , 0 , 3     , 0 , 'ASC')    ,
50  :("������Ҵ���"                , 0 , 3     , 0 , '')   ,
51  :("NO USE"                      , 0 , 3     , 0 , '')   ,
52  :("���˱�ʶ��PIN"               , 0 , 8     , 2 , 'BIN')    ,
53  :("��ȫ������Ϣ"                , 0 , 16    , 0 , 'BCDL')    ,
54  :("���ӽ��"                    , 3 , 40    , 0 , 'BASC')   ,
55  :("IC��������"                  , 3 , 999   , 0 , 'BIN')   ,
56  :("NO USE"                      , 3 , 999   , 0 , '')   ,
57  :("NO USE"                      , 3 , 999   , 0 , '')   ,
58  :("PBOC����Ǯ����׼������Ϣ"    , 3 , 999   , 0 , '')   ,
59  :("NO USE"                      , 3 , 999   , 0 , '')   ,
60  :("�Զ�����"                    , 3 , 13    , 0 , 'BCDL')    ,
61  :("ԭʼ��Ϣ��"                  , 3 , 999   , 0 , '')   ,
62  :("�Զ�����"                    , 3 , 512   , 0 , 'BCDL')    ,
63  :("�Զ�����"                    , 3 , 163   , 0 , 'ASC')    ,
64  :("��Ϣȷ����"                  , 0 , 8     , 2 , 'BIN')    ,
}

MAC_FIELDS = {  '0100,0110,0200,0210,0220,0230,0420,0430,0422,0432' : \
                    [0,2,3,4,7,11,18,25,28,32,33,38,39,41,42,90,102,103] , 
                '0520,0530,0522,0532' : \
                    [0,7,11,66,82,84,86,87,88,89,97] , 
                '0800,0810' : \
                    [0,7,11,39,53,70,100] , 
             }

MAK = None

def _msg_recv( sock , length = 4 , body_len = None , timeout = None ):
    print '_msg_recv'
    sock.settimeout( timeout ) # ���ó�ʱʱ�� �ȴ���ʱ�򣬲�ʵ�ó�ʱ
    print length,type(length)
    if type( length ) is int:
        buflen = sock.recv( length )
        print 'buflen',buflen
        if not buflen:
            raise RuntimeError( -1 , '�Է��ر�����' )
        buflen = int( buflen )
    elif type( length ) is str:
        l = struct.calcsize( length )
        buflen = sock.recv( l )
        if not buflen:
            raise RuntimeError( -1 , '�Է��ر�����' )
        buflen = struct.unpack( length , buflen )[0] # ȡ����
    print buflen,'lllllllllllllllll'
    print buflen,'lllllllllllllllll'
    
    if buflen == 0:
        # ���ĳ���Ϊ�㣬����
        return buflen
        raise RuntimeError( 1002 , '���ĳ���Ϊ�㣬���б���' )
    
    if callable( body_len ):
        buflen = body_len( buflen )
    
    # ��ʼ���ձ���
    rcv_len = 0
    buf = ''
    sock.settimeout( 30 ) # һ�鱨���30�볬ʱ
    while rcv_len < buflen:
        try:
            tbuf = sock.recv( buflen - rcv_len )  # ����ʣ���ֽ�
        except socket.timeout:
            raise RuntimeError( 1003 , '���ܱ��Ĺ����г�ʱ' )
        if tbuf is '':
            raise RuntimeError( -1 , '�Է��ر�����' )
        buf += tbuf
        rcv_len += len( tbuf )
    
    return buf

def recv( sock , prefix ):
    """
    �������Ľ��պ�����
    """
    try:
        buf = _msg_recv( sock , '>H' , timeout = 10 * 60 )
    except socket.timeout:
        raise RuntimeError( -2 , '����10����δ�յ����ģ�������ʧЧ��������' )
    # ���Ľ�����ϣ���ʼISO8583���
    print( 'yl2' , '[%s]���յ��ı���' ,  buf )
    rsp = False
    # �ⱨ����
    # ������ı��ģ�0���ǽ����룬1����bitmap��֮����������
    fields , ori_fields = unpack8583( buf[46:] , isomap = YL2_ZD_8583 )
    fields['HEADER'] = buf[:6] # ����ͷ��Ҫ�ͻأ���Ϊ����������ʱ������ͷ�еĹؼ���Ҫ�ͻ�
    # TODO Ӧ������ͷ�Ĵ���
    output_msg_body( fields , prefix )
    # ����MACУ��
    if not check_mac( ori_fields , prefix ):
        if fields[0][2] in ( '1' , '3' ): #��Ӧ����
            fields['ORI39'] = fields[39]
            fields[39] = 'A0'       # TODO ��Ҫ�����Զ�������Կ
        else: # ����������½���
            raise RuntimeError( 1004 , '����У���' , fields ) # �ᵼ��ϵͳ������Կ����
    
    if fields[0][2] in ( '1' , '3' ):
        # ��Ӧ����
        rsp = True
            
    return pickle_dumps( fields ) , rsp

def create_socket( timeout = 30 ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    if 'SO_REUSEPORT' in dir( socket ):
        s.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEPORT , 1 )
        
    s.setsockopt( socket.SOL_SOCKET , socket.SO_KEEPALIVE , 1 )
    s.settimeout( timeout ) # �趨��ʱʱ��Ϊ30��
    return s

def server_rsp( q_rsp , lock , socks ):
    # ���߳�
    print( 'yl2' , '[S1]��Ӧ�������߳�����' )
    while True:
        print( 'yl2' , '[S1]�ȴ���Ӧ����....' )
        try:
            buf = q_rsp.get() 
            print( 'yl2' , '[S1]���յ���Ӧ����: ' , buf  )
            # ��ȡ�ؼ���Ϣ�����ڹ���Ψһ������7��11����ΪΨһ����
            i8583 = pickle_loads( buf ) 
            key = '%s_%s' % ( i8583[7] , i8583[11] )
            with lock:
                conn = socks.pop( key , None )
            
            if conn is None:
                print( 'yl2' , '[S1]��ȡ�����sockʧ�ܣ��ý����п������ڲ��Զ�����' )
                continue
            try:
                # ��֯����
                buf2 = '%04d' % ( 20 + len( buf ) ) + conn[1] + buf
                conn[0].send( buf2 )
            except:
                print( 'yl2' , '[S1]��Ӧ���ķ���ʧ��' )
            finally:
                conn[0].close()
        except ( IOError , SystemExit ):
            print( 'yl2' , '[S1]�յ���ֹ�źţ���Ӧ�����߳��˳�' )
            break
        except:
            print( 'yl2' , '[S1]������Ӧ����ʱ����' )
            

def server( svr_ip ,svr_port  ):
    # ���̼߳���tongserʹ��socket�����ӷ��͹����ı��ģ������������Ӻͱ��Ķ�Ӧ��ϵ��Ȼ��ת��q_snd
    # ���̼߳���q_rsp��������Ӧ�ı��ģ������ͨ�������Ķ����ӽ����ķ��ء�
    pid = os.getpid()
    print 'yl2' , '[S1]�����ӽ���������%d��pid: %s' %( svr_port , pid )
    
    # ��ʼ�����߳�
#    LOCK = threading.Lock()
#    socks = {}
#    t = threading.Thread( target = server_rsp , args = ( q_rsp , LOCK , socks ) )
#    t.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)      
    #sock = create_socket( None ) # ���޳�ʱ
    print 'yl2' , '[S1]����socket�����ɹ�' 
    sock.bind( (svr_ip , svr_port ) )
    #sock.bind( ('127.0.0.1' , 3306 ) )
    sock.listen( 5 )
#    try:
    while True:
        print 'yl2' , '[S1]���׷����ӽ��̿�ʼ����...' 
        conn, addr = sock.accept()
        print addr 
        conn.settimeout( 30 ) # ���ó�ʱʱ��
        #buflen = conn.recv( 4 )
        #print '=====',buflen
        try:
            #buflen = conn.recv( length )
            #print '=====',buflen
            buf = _msg_recv( conn , 4  ) # 20�ֽ�ͷ+pickle������������Լ�
            # ��������ǣ�RESTART�����ʾϵͳҪ������
            print buf,'-------------------'
            if buf == 'RESTART':
                print 'yl2' , '[S1]�����ӽ����յ����������ź�' 
                conn.close()
                break
            elif buf == 0:
                continue
            print '0000000',binascii.b2a_hex( buf )
            res = unpack8583( buf   )
            for k,v in res[0].items():
                print k,v
                logger.info("%s%s"%(k,v))
#            fields = buf[16:]
#            # ��ȡ�ؼ���Ϣ�����ڹ���Ψһ������7��11����ΪΨһ����
#            i8583 = pickle_loads( fields ) 
#            key = '%s_%s' % ( i8583[7] , i8583[11] )
#            with LOCK:
#                socks[ key ] = ( conn , buf[:16] ) # ������Ӧ
        except :
            print 'yl2' , '[S1]���ձ���ʧ�ܣ�������: %d����������: %s'
            conn.close() # Ӧ�ر�����
#    except:
#        print 'yl2' , '[S1]�����ӽ����쳣, pid: %s' % pid 
#    finally:
#        sock.close()
#        print 'yl2' , '[S1]�����ӽ�����ֹ��pid: %s' % pid 
#        #RESTART.set()
    


svr_ip = '127.0.0.1'
svr_port = 33062
server( svr_ip ,svr_port  )