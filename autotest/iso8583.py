# coding: gbk

"""
    8583报文的解包和打包
"""
import binascii
#from shangjie.utils.ftools import register
#from Crypto.Cipher import DES
#from shangjie.conf import settings
def from_hex( s ):
    import binascii
    datastr = s.replace( " " , "" ).replace( "\n" , "" ).replace( "-" , "" )
    d = binascii.a2b_hex( datastr )
    return d
bit = { 1: 0x80 , #1000 0000
        2: 0x40 , #0100 0000
        3: 0x20 , #0010 0000
        4: 0x10 , #0001 0000
        5: 0x08 , #0000 1000
        6: 0x04 , #0000 0100
        7: 0x02 , #0000 0010
        8: 0x01 , #0000 0001
      }
#格式：域：(域名，是否变长标志0-否 2-2位变长 3-3位变长 ，数据域长度：变长分别为99 999 ，
#数据类型：0-string 1-int 2-binary , 编码类型：BCD BIN ASC ，对BCD编码，长度均为右对齐，数据L为左对齐，R为右对齐)
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
54  :("附加金额"                    , 3 , 20    , 0 , 'BIN')   ,
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
65  :("NO USE"                      , 3 , 999   , 0 , '')   ,
66  :("NO USE"                      , 0 , 1     , 0 , '')   ,
67  :("NO USE"                      , 3 , 999   , 0 , '')   ,
68  :("NO USE"                      , 3 , 999   , 0 , '')   ,
69  :("NO USE"                      , 3 , 999   , 0 , '')   ,
70  :("管理信息码"                  , 0 , 3     , 0 , '')   ,
71  :("NO USE"                      , 3 , 999   , 0 , '')   ,
72  :("NO USE"                      , 3 , 999   , 0 , '')   ,
73  :("NO USE"                      , 0 , 6     , 0 , '')   ,
74  :("贷记交易笔数"                , 0 , 10    , 0 , '')   ,
75  :("贷记自动冲正交易笔数"        , 0 , 10    , 0 , '')   ,
76  :("借记交易笔数"                , 0 , 10    , 0 , '')   ,
77  :("借记自动冲正交易笔数"        , 0 , 10    , 0 , '')   ,
78  :("转帐交易笔数"                , 0 , 10    , 0 , '')   ,
79  :("转帐自动冲正交易笔数"        , 0 , 10    , 0 , '')   ,
80  :("查询交易笔数"                , 0 , 10    , 0 , '')   ,
81  :("授权交易笔数"                , 0 , 10    , 0 , '')   ,
82  :("NO USE"                      , 0 , 12    , 0 , '')   ,
83  :("贷记交易费金额"              , 0 , 12    , 0 , '')   ,
84  :("NO USE"                      , 0 , 12    , 0 , '')   ,
85  :("借记交易费金额"              , 0 , 12    , 0 , '')   ,
86  :("贷记交易金额"                , 0 , 16    , 0 , '')   ,
87  :("贷记自动冲正金额"            , 0 , 16    , 0 , '')   ,
88  :("借记交易金额"                , 0 , 16    , 0 , '')   ,
89  :("借记自动冲正交易金额"        , 0 , 16    , 0 , '')   ,
90  :("原交易的数据元素"            , 0 , 42    , 0 , '')   ,
91  :("文件修改编码"                , 0 , 1     , 0 , '')   ,
92  :("NO USE"                      , 3 , 999   , 0 , '')   ,
93  :("NO USE"                      , 3 , 999   , 0 , '')   ,
94  :("服务指示码"                  , 0 , 7     , 0 , '')   ,
95  :("代替金额"                    , 0 , 42    , 0 , '')   ,
96  :("NO USE"                      , 0 , 8     , 0 , '')   ,
97  :("净结算金额"                  , 0 , 16    , 0 , '')   ,
98  :("NO USE"                      , 3 , 999   , 0 , '')   ,
99  :("结算机构码"                  , 2 , 11    , 0 , '')   ,
100 :("接收机构码"                  , 2 , 11    , 0 , '')   ,
101 :("文件名"                      , 2 , 17    , 0 , '')   ,
102 :("帐号1"                       , 2 , 28    , 0 , '')   ,
103 :("帐号2"                       , 2 , 28    , 0 , '')   ,
104 :("NO USE"                      , 3 , 999   , 0 , '')   ,
105 :("NO USE"                      , 3 , 999   , 0 , '')   ,
106 :("NO USE"                      , 3 , 999   , 0 , '')   ,
107 :("NO USE"                      , 3 , 999   , 0 , '')   ,
108 :("NO USE"                      , 3 , 999   , 0 , '')   ,
109 :("NO USE"                      , 3 , 999   , 0 , '')   ,
110 :("NO USE"                      , 3 , 999   , 0 , '')   ,
111 :("NO USE"                      , 3 , 999   , 0 , '')   ,
112 :("NO USE"                      , 3 , 999   , 0 , '')   ,
113 :("NO USE"                      , 3 , 999   , 0 , '')   ,
114 :("NO USE"                      , 3 , 999   , 0 , '')   ,
115 :("NO USE"                      , 3 , 999   , 0 , '')   ,
116 :("NO USE"                      , 3 , 999   , 0 , '')   ,
117 :("NO USE"                      , 3 , 999   , 0 , '')   ,
118 :("NO USE"                      , 3 , 999   , 0 , '')   ,
119 :("NO USE"                      , 3 , 999   , 0 , '')   ,
120 :("NO USE"                      , 3 , 999   , 0 , '')   ,
121 :("NO USE"                      , 3 , 999   , 0 , '')   ,
122 :("NO USE"                      , 3 , 999   , 0 , '')   ,
123 :("新密码数据"                  , 3 , 8     , 2 , '')   ,
124 :("NO USE"                      , 3 , 999   , 0 , '')   ,
125 :("NO USE"                      , 3 , 999   , 0 , '')   ,
126 :("NO USE"                      , 3 , 999   , 0 , '')   ,
127 :("NO USE"                      , 3 , 999   , 0 , '')   ,
128 :("信息确认码"                  , 0 , 8     , 2 , '')   ,
}


#macfield = (2,3,4,11,12,13,32,38,39,41,49,95)

def unpack8583( buf , isomap = None ):
    """
    8583报文解包
    参数列表 
    buf 报文内容
    mackey mac校验码
    """
#    if isomap is None:
#        isomap = ISO8583
    isomap = ISO8583
    ret = {}
    # 先处理0,1域
    ori_val , value , pos = filed_decode( buf , isomap[0] , 0 , 0 )
    ori_ret = {}
    ret[0] = value  # 
    ori_ret[0] = ori_val
    #print 'MTI' , value
    bLen = ord(buf[pos]) & 0x80 or 64 # 测试是否128位bitmap
    #print buf[4] , ord(buf[4]) , bLen ,bLen/8+4
    bitmap = buf[pos:bLen/8+pos]
    ret[1] = [ bLen , bitmap ] # bitmap
    #print 'BITMAP' , `bitmap`
    pos = bLen/8 + pos
    if bLen == 128:
        macf = 128
    else:
        macf = 64
    for i in range( 2 , bLen + 1 ):
        byte = bitmap[(i-1)/8] # get byte
        bits = i % 8 or 8
        #print 'i',i,'byte',ord(byte),'bits',bits, ord( byte ) & bit[bits]
        if ord( byte ) & bit[bits] : # test bit
            ori_val , value , pos = filed_decode(buf,isomap[i],pos,i)
            if i in (35,36):
                value = value.replace('d','=')
            ret[i] = value
            ori_ret[i] = ori_val
    
    return ret , ori_ret


def pack8583(t_dict , isomap = None , build_mac = None ):
    """
    8583报文打包
    参数列表
    t_dict 报文内容
    """
    if isomap is None:
        isomap = ISO8583
    buf = ''
    macstr= ''
    #提取有数据的域，key值是整数的
    field = list( filter( lambda x: type( x ) is int , t_dict.keys() ) )
    #print field
    #获取交易码
    ori_fields = {}
    jym = t_dict[0]
    #判断位图是64还是128位，使用65以后的域
    sf16 = max( field ) >= 65 

    #初始化位图
    byte = []
    if sf16:
        blen = 16
        byte = [0]*blen
        byte[0] = 0x80
    else:
        blen = 8
        byte = [0]*blen
    
    macf = 128 if sf16 else 64
    
    if macf not in field:
        field.append( macf ) # 先将mac域放入

    field.sort() 
    #遍历64或128个域
    for i in range(2 , blen*8 + 1 ):
        #数据域对应位图位置
        bytes = ( i - 1 ) / 8
        bits = i % 8 or 8
        #print i,bytes,bits
        #该域有值
        if i in field:
            #设置位图对应位
            byte[bytes] = byte[bytes] + bit[bits]
            if i != macf: #64 128域单独处理
                v = str(t_dict[i])
                if i in (35,36):
                    v = v.replace('=','d')
                v = field_encode(isomap[i],v)
                buf += v
                ori_fields[ i ] = v
    
    #报文组串
    jym_b = field_encode( isomap[0] , jym )  # 根据8583规范打包
    ori_fields[0] = jym_b
    if callable( build_mac ):
        macstr = build_mac( ori_fields )
    else:
        macstr = ''
    #print byte
    #生成位图
    if not macstr:
        byte[-1] = byte[-1] & 0b11111110 # 去掉最后的mac域
        
    map = ''
    for b in byte:
        map = map + chr(b)
    t_dict[1] = map
    # 
    ret = jym_b + map + buf + macstr
    
    return ret


def field_encode(ISO,v):
    #BCD压缩
    if ISO[4] in ('BCDL','BCDR','BASC'):
        v_len = len(v)  #BCD压缩后的长度
        #奇数位的根据对齐方式前后补零
        if (v_len % 2) == 1:
            if ISO[4] == 'BCDL':
                v = v + '0'
            elif ISO[4] == 'BCDR':
                v = '0' + v
        #变长字段写入实际长度，而不是压缩后的长度
        if ISO[1] == 2: # 二位变长域
            v_len = '%02d' % v_len 
        elif ISO[1] == 3: # 三位变长域，前补零
            v_len = '%04d' % v_len 
        else:#定长域
            v_len = ''
        v_len = v_len.decode( 'hex' )
        if 'BCD' in ISO[4]:
            v = v.decode( 'hex' )
        ret = v_len + v
    else:
        v_len = len(v)
        if ISO[1] == 2: # 二位变长域
            value = '%02d' %  v_len
            value += v
            #value = binascii.a2b_hex(value) + v
        elif ISO[1] == 3: # 三位变长域
            value = '%03d' %  v_len
            value += v
            #value = binascii.a2b_hex(value) + v
        else:#定长域
            value = v
        ret = value
    #print ret
    return ret


def filed_decode(buf,ISO,pos,i):
    #BCD解压缩
    if ISO[4] in ('BCDL','BCDR','BASC'):
        if ISO[1] == 2: # 2字节长度域
            #取长度
            tmp = buf[pos:pos+1]
            tmp = binascii.b2a_hex(tmp)
            length = int( tmp )
            #print i , '两位长度变长域:len[%s]' % length ,
            pos += 1
        elif ISO[1] == 3: # 3字节长度域
            tmp = buf[pos:pos+2]
            #print tmp
            tmp = binascii.b2a_hex(tmp)
            #print tmp
            length = int( tmp )
            #print length
            #print i , '三位长度变长域:len[%s]' % length ,
            pos += 2
        else:
            #print i , '定长域:len[%d]' % ISO[2] ,
            length = ISO[2]
            tmp = ''
        #ret[i] = [ length , buf[pos:pos+length] ]
        #计算压缩后的长度
        v_len = (length + 1) / 2
        value = buf[pos:pos+v_len]
        ori_val = tmp + value
        if 'BCD' in ISO[4]:
            value = binascii.b2a_hex(value)
            #奇数位的根据对齐方式前后补零的去掉
            if (length % 2) == 1:
                if ISO[4] == 'BCDL':
                    value = value[:-1]
                else:
                    value = value[1:]
    else:
        if ISO[1] == 2: # 2字节长度域
            tmp = buf[pos:pos+2]
            length = int( tmp )
            #print i , '两位长度变长域:len[%s]' % length ,
            pos += 2
            #print i , '两位长度变长域:len[%s]' % buf[pos:pos+2] ,
            #length = int( buf[pos:pos+2] )
            #pos += 2
        elif ISO[1] == 3: # 3字节长度域
            tmp = buf[pos:pos+3]
            #print tmp
            length = int( tmp )
            #print length
            #print i , '三位长度变长域:len[%s]' % length ,
            pos += 3

            #print i , '三位长度变长域:len[%s]' % buf[pos:pos+3] ,
            #length = int( buf[pos:pos+3] )
            #pos += 3
        else:
            #print i , '定长域:len[%d]' % ISO[2] ,
            length = ISO[2]
            tmp = ''
        value = buf[pos:pos+length]
        ori_val = tmp + value
        v_len = length
    #print pos,v_len
    pos += v_len
    #print pos
    #print value
    return ori_val,value,pos

def pin_encode(t_dict,pinkey = None):
    #PIN码加密
    try:
        #PIN码明文
        PIN = t_dict[52]
        #加密方式
        jmfs = t_dict[53]
    except:
        raise RuntimeError( '未提供PIN码或加密方式' )
    PAN = ''
    if jmfs[0] == '2':
        try:
            zh = t_dict[2]
            PAN = zh[-13:-1]
        except:
            try:
                zh = t_dict[35]
            except:
                try:
                    zh = t_dict[36]
                except:
                    raise RuntimeError( '未提供35或36域' )
            fgf = zh.find('=')
            PAN = zh[fgf - 13:fgf - 1]
        #PAN = '678901234567'
        #print PIN,PAN
        pin_len = len(PIN)
        pin_hex = binascii.a2b_hex('%02d'%pin_len) +  binascii.a2b_hex(PIN) + '\xff'*(7-pin_len/2)
        #print to_hex(pin_hex)
        pan_hex = '\x00\x00' + binascii.a2b_hex(PAN)
        #print to_hex(pan_hex)
        #print `pin_hex`,`pan_hex`
        xorstr = ''
        for i in range(0,8):
            a = ord(pin_hex[i]) ^ ord(pan_hex[i])
            b = hex(a)
            c = chr(a)
            xorstr += c
            #print pin_hex[i],pan_hex[i],a,b,c
        PIN = xorstr
        #print to_hex(PIN)

    PIN = mac_encode(PIN,pinkey)
    return PIN


def mac_encode_xh(buf,mackey):
    """mac加密
    参数列表
    buf  报文内容
    mackey
    """
    des = DES.new(mackey,DES.MODE_ECB)
    #字节补齐8的倍数
    buf = buf + '\x00' * ( 8 - ( len(buf) % 8 ) )
    #print buf

    tmp = buf[:8]
    tmp1 = ''
    #每8个字节一组，依次取做异或，第一组与第二组异或，结果与第三组异或，依次类推
    for i in range(0,len(buf)/8 - 1):
        for l in range(0,8):
            #print i,l,tmp[l],buf[(i+1)*8+l],tmp1
            tmp1 += chr(ord(tmp[l]) ^ ord(buf[(i+1)*8+l]))
        tmp = tmp1
        tmp1 = ''
    #print `tmp`

    #将异或的最后结果转换为16个hex
    for i in range(0,8):
        #print '%02X'%(ord(tmp[i]))
        tmp1 += '%02X'%(ord(tmp[i]))
    #print tmp1

    #前8位des加密再与后8位异或
    tmp2 =  des.encrypt(tmp1[:8])
    #print `tmp2`
    tmp = ''
    for i in range(0,8):
        #print tmp2[i],tmp1[i+8]
        tmp += chr(ord(tmp2[i]) ^ ord(tmp1[i+8]))
    #print `tmp`

    #再次进行des加密，将加密结果转换为16个hex
    tmp =  des.encrypt(tmp)
    tmp1 = ''
    for i in range(0,8):
        #print '%02X'%(ord(tmp[i]))
        tmp1 += '%02X'%(ord(tmp[i]))
    #print tmp1

    #取前8位返回
    return tmp1[:8]


def mac_encode(buf,mackey):
    """mac加密 des加密
    参数列表
    buf  报文内容
    mackey mac校验码
    """
    #print buf
    des = DES.new(mackey,DES.MODE_CBC)
    a = len(buf) % 8
    if a == 0:
        a = 8
    buf = buf + '\x00' * ( 8 - a )

    ret = des.encrypt(buf)
    return ret


def mac_decode(buf,mackey):
    """mac解密 解des方法加密
       参数列表
       buf 报文内容
       mackey mac校验码
    """
    des = DES.new(mackey,DES.MODE_CBC)

    #buf = buf + '\x00' * ( 8 - ( len(buf) % 8 ) )
    ret = des.decrypt(buf)
    return ret

import re

p = re.compile( '\d{6}' )


def kmm_decode(sbbh,kmm_en):
    """卡密码解密，根据设备的mackey 用des加密的解密方法
        参数列表 
        sbbh 设备编号
        kmm_en  加密的卡密码
    """
    #print '加密的卡密码：%s'%kmm_en
    sbobj = GL_SBDY.get_by(bh = sbbh)
    if sbobj:
        mackey = sbobj.mackey
    else:
        raise RuntimeError("设备编号非法")
    #print "mackey:",mackey
    mackey = binascii.a2b_hex(mackey)
    kmm_en = binascii.a2b_hex(kmm_en)
    #根据设备流水号生成工作密钥
    des = DES.new(mackey,DES.MODE_CBC)
    kmm_de = des.decrypt(kmm_en)
    #print '解密的卡密码：%s'%kmm_de[:6]
    if p.match( kmm_de[:6] ):
        return kmm_de[:6]
    else:
        raise RuntimeError( '解出密码格式不对[%s]' % `kmm_de[:6]` )


def make_mackey(sbbh,sblsh):
    """设备工作密钥生成，DES加密
       参数列表
       sbbh 设备编号
       sblsh 设备流水号
    """
    with connection() as con:
        cur = con.cursor()
        rs = sql_execute( cur , "select mainkey from gl_sbdy where bh = %s for update" , [ sbbh ] )
        if rs.next():
            mainkey = rs.getString( 'mainkey' )
            mainkey = binascii.a2b_hex(mainkey)
            #根据设备流水号生成工作密钥
            des = DES.new(mainkey,DES.MODE_CBC)
            sblsh = '%08d'%sblsh
            mackey_en = des.encrypt(sblsh)
            mackey = binascii.b2a_hex(mackey_en)
            #print "生成新的工作密钥：%s"%mackey
            cur.execute( "update gl_sbdy set mackey = %s where bh = %s" , [ mackey , sbbh ] )
        else:
            raise RuntimeError("设备编号非法")
    
    #对工作密钥再次进行加密，传送到设备
    des = DES.new(mainkey,DES.MODE_CBC)
    mackey1 = des.encrypt(mackey_en)
    mackey1 = binascii.b2a_hex(mackey1)
    #print "工作密钥再次进行加密：%s"%mackey1
    return mackey1

if __name__ == '__main__':
    t = { 0: '0101' , 64:'', 11:'1111111', 18:'10', 54:'44444'  }
    buf1 = pack8583( t ) 
    print repr( pack8583( t )  )
    #raw_input()
    kmm_en = 'F2DC9D5A1510CB4'
    mackey = 'ec4662686bced3d9'
    class Dummy:
        pass
    from shangjie.utils.ftools import AttrDict
    t = Dummy()
    t.fmt = AttrDict()
    
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
    print from_hex( buf )
    res = unpack8583( from_hex( buf )  )
    for k,v in res[0].items():
        print k,v
#    buf1 = "0101002040000000040011111110313000053434343434"
#    res = unpack8583( buf1  )
#    for k,v in res[0].items():
#        print k,v
