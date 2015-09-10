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

def _msg_recv( sock , length = 4 , body_len = None , timeout = None ):
    print '_msg_recv'
    sock.settimeout( timeout ) # 设置超时时间 等待的时候，不实用超时
    print length,type(length)
    if type( length ) is int:
        buflen = sock.recv( length )
        print 'buflen',buflen
        if not buflen:
            raise RuntimeError( -1 , '对方关闭连接' )
        buflen = int( buflen )
    elif type( length ) is str:
        l = struct.calcsize( length )
        buflen = sock.recv( l )
        if not buflen:
            raise RuntimeError( -1 , '对方关闭连接' )
        buflen = struct.unpack( length , buflen )[0] # 取长度
    print buflen,'lllllllllllllllll'
    print buflen,'lllllllllllllllll'
    
    if buflen == 0:
        # 报文长度为零，丢弃
        return buflen
        raise RuntimeError( 1002 , '报文长度为零，空闲报文' )
    
    if callable( body_len ):
        buflen = body_len( buflen )
    
    # 开始接收报文
    rcv_len = 0
    buf = ''
    sock.settimeout( 30 ) # 一组报文最长30秒超时
    while rcv_len < buflen:
        try:
            tbuf = sock.recv( buflen - rcv_len )  # 接收剩余字节
        except socket.timeout:
            raise RuntimeError( 1003 , '接受报文过程中超时' )
        if tbuf is '':
            raise RuntimeError( -1 , '对方关闭连接' )
        buf += tbuf
        rcv_len += len( tbuf )
    
    return buf

def recv( sock , prefix ):
    """
    银联报文接收函数。
    """
    try:
        buf = _msg_recv( sock , '>H' , timeout = 10 * 60 )
    except socket.timeout:
        raise RuntimeError( -2 , '超过10分钟未收到报文，该连接失效，需重启' )
    # 报文接收完毕，开始ISO8583解包
    print( 'yl2' , '[%s]接收到的报文' ,  buf )
    rsp = False
    # 解报文体
    # 解出来的报文，0域是交易码，1域是bitmap，之后是正常域
    fields , ori_fields = unpack8583( buf[46:] , isomap = YL2_ZD_8583 )
    fields['HEADER'] = buf[:6] # 报文头需要送回，因为当返回请求时，报文头中的关键域要送回
    # TODO 应该增加头的处理
    output_msg_body( fields , prefix )
    # 进行MAC校验
    if not check_mac( ori_fields , prefix ):
        if fields[0][2] in ( '1' , '3' ): #响应报文
            fields['ORI39'] = fields[39]
            fields[39] = 'A0'       # TODO 需要考虑自动申请密钥
        else: # 银联发起的新交易
            raise RuntimeError( 1004 , '报文校验错' , fields ) # 会导致系统重新密钥申请
    
    if fields[0][2] in ( '1' , '3' ):
        # 响应报文
        rsp = True
            
    return pickle_dumps( fields ) , rsp

def create_socket( timeout = 30 ):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEADDR , 1 )
    if 'SO_REUSEPORT' in dir( socket ):
        s.setsockopt( socket.SOL_SOCKET , socket.SO_REUSEPORT , 1 )
        
    s.setsockopt( socket.SOL_SOCKET , socket.SO_KEEPALIVE , 1 )
    s.settimeout( timeout ) # 设定超时时间为30秒
    return s

def server_rsp( q_rsp , lock , socks ):
    # 子线程
    print( 'yl2' , '[S1]响应处理子线程启动' )
    while True:
        print( 'yl2' , '[S1]等待响应队列....' )
        try:
            buf = q_rsp.get() 
            print( 'yl2' , '[S1]接收到响应报文: ' , buf  )
            # 提取关键信息，用于构建唯一索引，7和11域作为唯一索引
            i8583 = pickle_loads( buf ) 
            key = '%s_%s' % ( i8583[7] , i8583[11] )
            with lock:
                conn = socks.pop( key , None )
            
            if conn is None:
                print( 'yl2' , '[S1]提取发起端sock失败，该交易有可能是内部自动发起' )
                continue
            try:
                # 组织报文
                buf2 = '%04d' % ( 20 + len( buf ) ) + conn[1] + buf
                conn[0].send( buf2 )
            except:
                print( 'yl2' , '[S1]响应报文返回失败' )
            finally:
                conn[0].close()
        except ( IOError , SystemExit ):
            print( 'yl2' , '[S1]收到终止信号，响应处理线程退出' )
            break
        except:
            print( 'yl2' , '[S1]处理响应报文时出错' )
            

def server( svr_ip ,svr_port  ):
    # 主线程监听tongser使用socket短连接发送过来的报文，并保留短连接和报文对应关系，然后转发q_snd
    # 子线程监听q_rsp（银联响应的报文），查表并通过保留的短连接将报文发回。
    pid = os.getpid()
    print 'yl2' , '[S1]监听子进程启动，%d，pid: %s' %( svr_port , pid )
    
    # 初始化子线程
#    LOCK = threading.Lock()
#    socks = {}
#    t = threading.Thread( target = server_rsp , args = ( q_rsp , LOCK , socks ) )
#    t.start()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   
    sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)      
    #sock = create_socket( None ) # 不限超时
    print 'yl2' , '[S1]监听socket创建成功' 
    sock.bind( (svr_ip , svr_port ) )
    #sock.bind( ('127.0.0.1' , 3306 ) )
    sock.listen( 5 )
#    try:
    while True:
        print 'yl2' , '[S1]交易发起子进程开始监听...' 
        conn, addr = sock.accept()
        print addr 
        conn.settimeout( 30 ) # 设置超时时间
        #buflen = conn.recv( 4 )
        #print '=====',buflen
        try:
            #buflen = conn.recv( length )
            #print '=====',buflen
            buf = _msg_recv( conn , 4  ) # 20字节头+pickle，长度域包含自己
            # 如果报文是：RESTART，则表示系统要求重启
            print buf,'-------------------'
            if buf == 'RESTART':
                print 'yl2' , '[S1]监听子进程收到主动重启信号' 
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
#            # 提取关键信息，用于构建唯一索引，7和11域作为唯一索引
#            i8583 = pickle_loads( fields ) 
#            key = '%s_%s' % ( i8583[7] , i8583[11] )
#            with LOCK:
#                socks[ key ] = ( conn , buf[:16] ) # 用于响应
        except :
            print 'yl2' , '[S1]接收报文失败，错误码: %d，错误描述: %s'
            conn.close() # 应关闭连接
#    except:
#        print 'yl2' , '[S1]监听子进程异常, pid: %s' % pid 
#    finally:
#        sock.close()
#        print 'yl2' , '[S1]监听子进程终止，pid: %s' % pid 
#        #RESTART.set()
    


svr_ip = '127.0.0.1'
svr_port = 33062
server( svr_ip ,svr_port  )