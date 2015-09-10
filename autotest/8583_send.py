# coding: gbk
import socket
import re
import struct
from iso8583 import *
#格式：域：(域名，是否变长标志0-否 2-2位变长 3-3位变长 ，数据域长度：变长分别为99 999 ，
#数据类型：0-string 1-int 2-binary , 编码类型：BCD BIN ASC ，对BCD编码，长度均为右对齐，数据L为左对齐，R为右对齐)
#YL2_8583 = {
ISO8583 = {
0   :("消息类型"                    , 0 , 4     , 0 , 'BCDL')    ,
1   :("位图"                        , 0 , 8     , 2 , 'BIN')    ,
2   :("主账号"                      , 2 , 19    , 0 , 'BCDL')    ,
3   :("交易处理码"                  , 0 , 6     , 0 , 'BCDL')    ,
4   :("交易金额"                    , 0 , 12    , 1 , 'BCDL')    ,
5   :("NO USE"                      , 0 , 12    , 0 , '')   ,
6   :("NO USE"                      , 0 , 12    , 0 , '')   ,
7   :("交易日期和时间"              , 0 , 10    , 0 , '')   ,
8   :("NO USE"                      , 0 , 8     , 0 , '')   ,
9   :("NO USE"                      , 0 , 8     , 0 , '')   ,
10  :("NO USE"                      , 0 , 8     , 0 , '')   ,
11  :("受卡方系统跟踪号"            , 0 , 6     , 1 , 'BCDL')    ,
12  :("受卡方所在地时间"            , 0 , 6     , 0 , 'BCDL')    ,
13  :("受卡方所在地日期"            , 0 , 4     , 0 , 'BCDL')    ,
14  :("卡有效期"                    , 0 , 4     , 0 , 'BCDL')    ,
15  :("清算日期"                    , 0 , 4     , 0 , 'BCDL')    ,
16  :("NO USE"                      , 0 , 4     , 0 , '')   ,
17  :("获取日期"                    , 0 , 4     , 0 , '')   ,
18  :("商户类型"                    , 0 , 4     , 0 , '')   ,
19  :("NO USE"                      , 0 , 3     , 0 , '')   ,
20  :("NO USE"                      , 0 , 3     , 0 , '')   ,
21  :("NO USE"                      , 0 , 3     , 0 , '')   ,
22  :("服务点输入方式码"            , 0 , 3     , 0 , 'BCDL')    ,
23  :("卡序列号"                    , 0 , 3     , 0 , 'BCDR')    ,
24  :("NO USE"                      , 0 , 3     , 0 , '')   ,
25  :("服务点条件代码"              , 0 , 2     , 0 , 'BCDL')    ,
26  :("服务点PIN获取码"             , 0 , 2     , 0 , 'BCDL')    ,
27  :("NO USE"                      , 0 , 1     , 0 , '')   ,
28  :("field27"                     , 0 , 6     , 0 , '')   ,
29  :("NO USE"                      , 1 , 8     , 0 , '')   ,
30  :("NO USE"                      , 1 , 8     , 0 , '')   ,
31  :("NO USE"                      , 1 , 8     , 0 , '')   ,
32  :("受理方标识码"                , 2 , 11    , 0 , 'BCDL')    ,
33  :("授权机构标识码"              , 2 , 11    , 0 , '')   ,
34  :("NO USE"                      , 2 , 28    , 0 , '')   ,
35  :("2磁道数据"                   , 2 , 37    , 0 , 'BCDL')    ,
36  :("3磁道数据"                   , 3 , 104   , 0 , 'BCDL')    ,
37  :("检索参考号"                  , 0 , 12    , 0 , 'ASC')    ,
38  :("授权标识应答码"              , 0 , 6     , 0 , 'ASC')    ,
39  :("应答码"                      , 0 , 2     , 0 , 'ASC')    ,
40  :("NO USE"                      , 0 , 3     , 0 , '')   ,
41  :("受卡机终端标识码"            , 0 , 8     , 0 , 'ASC')    ,
42  :("受卡方标识码"                , 0 , 15    , 0 , 'ASC')    ,
43  :("收卡商户位置"                , 0 , 40    , 0 , '')   ,
44  :("附加响应数据"                , 2 , 25    , 0 , 'ASC')    ,
45  :("NO USE"                      , 2 , 76    , 0 , '')   ,
46  :("NO USE"                      , 3 , 999   , 0 , '')   ,
47  :("field47"                     , 3 , 999   , 0 , '')   ,
48  :("私有附加数据"                , 3 , 999   , 0 , 'BCDL')    ,
49  :("交易货币代码"                , 0 , 3     , 0 , 'ASC')    ,
50  :("结算货币代码"                , 0 , 3     , 0 , '')   ,
51  :("NO USE"                      , 0 , 3     , 0 , '')   ,
52  :("个人标识码PIN"               , 0 , 8     , 2 , 'BIN')    ,
53  :("安全控制信息"                , 0 , 16    , 0 , 'BCDL')    ,
54  :("附加金额"                    , 3 , 40    , 0 , 'BASC')   ,
55  :("IC卡数据域"                  , 3 , 999   , 0 , 'BIN')   ,
56  :("NO USE"                      , 3 , 999   , 0 , '')   ,
57  :("NO USE"                      , 3 , 999   , 0 , '')   ,
58  :("PBOC电子钱包标准交易信息"    , 3 , 999   , 0 , '')   ,
59  :("NO USE"                      , 3 , 999   , 0 , '')   ,
60  :("自定义域"                    , 3 , 13    , 0 , 'BCDL')    ,
61  :("原始信息域"                  , 3 , 999   , 0 , '')   ,
62  :("自定义域"                    , 3 , 512   , 0 , 'BCDL')    ,
63  :("自定义域"                    , 3 , 163   , 0 , 'ASC')    ,
64  :("信息确认码"                  , 0 , 8     , 2 , 'BIN')    ,
}

MAC_FIELDS = {  '0100,0110,0200,0210,0220,0230,0420,0430,0422,0432' : \
                    [0,2,3,4,7,11,18,25,28,32,33,38,39,41,42,90,102,103] , 
                '0520,0530,0522,0532' : \
                    [0,7,11,66,82,84,86,87,88,89,97] , 
                '0800,0810' : \
                    [0,7,11,39,53,70,100] , 
             }

MAK = None

def send( sock , fields , prefix , yljgdm ):
    """
    银联报文发送函数
    """
    # 组报文体
    buf = pack8583( fields )#, isomap = ISO8583  )
    # 补报文头
#    buf_header = '602100000000'.decode( 'hex' )
#    buf = buf_header + buf
    print 'yl2' , '[%s]要发送的报文'% buf 
    try:
        #sock.send( struct.pack( '>H' , len( buf ) ))
        sock.send(  '%04d'%len( buf ) )
        print '发送的报文【%s】'%buf
        sock.send( buf )
    except socket.timeout:
        raise RuntimeError( 2000 , '发送银联超时' )

def create_socket( timeout = 30 ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    if 'SO_REUSEPORT' in dir( socket ):
        s.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEPORT , 1 )
        
    s.setsockopt( socket.SOL_SOCKET , socket.SO_KEEPALIVE , 1 )
    s.settimeout( timeout ) # 设定超时时间为30秒
    return s


tgt_ip = '127.0.0.1'
tgt_port = 33062
#sock = create_socket()
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)      

#try:
#    print 'yl2' , '[%s]发送子进程创建连接....' 
#    print ( tgt_ip , tgt_port )
#    sock.connect( ( tgt_ip , tgt_port ) )
#    print '00000000000000000000000'
#    sock.send( '0000' ) # 连接成功就发送一个空闲心跳
#except Exception , e:
#    print 'yl2' , '[%s]发送子进程建立连接报错'  
fields = { 0: '0101' , 64:'', 11:'1111111', 18:'10', 54:'44444'  }
idx = 1
buf = pack8583( fields)# , isomap = ISO8583  )
res = unpack8583(  buf   )
for k,v in res[0].items():
    print k,v

yljgdm = '66666'
print yljgdm
sock.connect( ( tgt_ip , tgt_port ) )
send( sock , fields , idx , yljgdm )
buf = """
        60 00 00 04 50 60 22 00 - 00 00 00 02 10 70 3E 00
        81 0A D0 80 13 16 95 55 - 50 53 13 27 59 58 00 00
        00 00 00 00 01 00 00 00 - 01 91 17 14 14 12 15 49
        12 12 15 00 08 00 09 45 - 00 31 37 31 34 31 34 30
        38 31 30 33 36 30 30 37 - 30 30 30 30 30 30 35 33
        30 34 33 37 30 31 38 33 - 39 38 30 30 30 35 25 30
        33 30 38 34 35 31 30 20 - 20 20 30 33 30 34 34 35
        31 30 20 20 20 20 20 20 - 31 35 36 00 08 22 00 00
        01 00 63 43 55 50 20 20 - 20 20 20 20 20 20 20 20
        20 20 20 20 20 20 20 20 - 20 20 20 20 20 20 20 20
        20 20 20 20 20 20 20 20 - 20 20 20 20 20 20 20 20
        20 20 20 20 20 20 20 20 - 20 20 20 20 20 20 20 20
        20 20 42 39 38 42 38 31 - 39 31                  
      """
import binascii
sock.send('%04d%s'%(len(from_hex( buf )), from_hex( buf )) )