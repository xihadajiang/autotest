# coding: gbk

"""
    8583报文的解包和打包
"""
bit = { 1: 0x80 , #1000 0000
        2: 0x40 , #0100 0000
        3: 0x20 , #0010 0000
        4: 0x10 , #0001 0000
        5: 0x08 , #0000 1000
        6: 0x04 , #0000 0100
        7: 0x02 , #0000 0010
        8: 0x01 , #0000 0001
      }

#格式:域:(域名，是否变长标志0-否 2-2位变长 3-3位变长 ，数据域长度:变长分别为99 999 ，
#数据类型:0-string 1-int 2-binary , 编码类型:BCD BIN ASC ，对BCD编码，长度均为右对齐，数据L为左对齐，R为右对齐)
ISO8583 = {
0   :("消息类型"                    , 0 , 4     , 0 , '')    ,
1   :("位图"                        , 0 , 8     , 0 , '')    ,
2   :("主账号"                      , 2 , 19    , 0 , '')    ,
3   :("交易处理码"                  , 0 , 6     , 0 , '')    ,
4   :("交易金额"                    , 0 , 12    , 1 , '')    ,
5   :("NO USE"                      , 0 , 12    , 0 , '')   ,
6   :("NO USE"                      , 0 , 12    , 0 , '')   ,
7   :("交易日期和时间"              , 0 , 10    , 0 , '')   ,
8   :("NO USE"                      , 0 , 8     , 0 , '')   ,
9   :("NO USE"                      , 0 , 8     , 0 , '')   ,
10  :("NO USE"                      , 0 , 8     , 0 , '')   ,
11  :("受卡方系统跟踪号"            , 0 , 6     , 1 , '')    ,
12  :("受卡方所在地时间"            , 0 , 6     , 0 , '')    ,
13  :("受卡方所在地日期"            , 0 , 4     , 0 , '')    ,
14  :("卡有效期"                    , 0 , 4     , 0 , '')    ,
15  :("清算日期"                    , 0 , 4     , 0 , '')    ,
16  :("NO USE"                      , 0 , 4     , 0 , '')   ,
17  :("获取日期"                    , 0 , 4     , 0 , '')   ,
18  :("商户类型"                    , 0 , 4     , 0 , '')   ,
19  :("NO USE"                      , 0 , 3     , 0 , '')   ,
20  :("NO USE"                      , 0 , 3     , 0 , '')   ,
21  :("NO USE"                      , 0 , 3     , 0 , '')   ,
22  :("服务点输入方式码"            , 0 , 3     , 0 , '')    ,
23  :("卡序列号"                    , 0 , 3     , 0 , '')    ,
24  :("NO USE"                      , 0 , 3     , 0 , '')   ,
25  :("服务点条件代码"              , 0 , 2     , 0 , '')    ,
26  :("服务点PIN获取码"             , 0 , 2     , 0 , '')    ,
27  :("NO USE"                      , 0 , 1     , 0 , '')   ,
28  :("field27"                     , 0 , 6     , 0 , '')   ,
29  :("NO USE"                      , 1 , 8     , 0 , '')   ,
30  :("NO USE"                      , 1 , 8     , 0 , '')   ,
31  :("NO USE"                      , 1 , 8     , 0 , '')   ,
32  :("受理方标识码"                , 2 , 11    , 0 , '')    ,
33  :("授权机构标识码"              , 2 , 11    , 0 , '')   ,
34  :("NO USE"                      , 2 , 28    , 0 , '')   ,
35  :("2磁道数据"                   , 2 , 37    , 0 , '')    ,
36  :("3磁道数据"                   , 3 , 104   , 0 , '')    ,
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
48  :("私有附加数据"                , 3 , 999   , 0 , '')    ,
49  :("交易货币代码"                , 0 , 3     , 0 , 'ASC')    ,
50  :("结算货币代码"                , 0 , 3     , 0 , '')   ,
51  :("NO USE"                      , 0 , 3     , 0 , '')   ,
52  :("个人标识码PIN"               , 0 , 8     , 2 , 'BIN')    ,
53  :("安全控制信息"                , 0 , 16    , 0 , '')    ,
54  :("附加金额"                    , 3 , 20    , 0 , 'BIN')   ,
55  :("IC卡数据域"                  , 3 , 999   , 0 , 'BIN')   ,
56  :("NO USE"                      , 3 , 999   , 0 , '')   ,
57  :("NO USE"                      , 3 , 999   , 0 , '')   ,
58  :("PBOC电子钱包标准交易信息"    , 3 , 999   , 0 , '')   ,
59  :("NO USE"                      , 3 , 999   , 0 , '')   ,
60  :("自定义域"                    , 3 , 13    , 0 , '')    ,
61  :("原始信息域"                  , 3 , 999   , 0 , '')   ,
62  :("自定义域"                    , 3 , 512   , 0 , '')    ,
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

#import cStringIO
#def to_hex( s ):
#    st = cStringIO.StringIO()
#    
#    def fmt( x ):
#        if ord( ' ' ) <= ord( x ) <= ord( '\x7E' ):
#            return x
#        return '.'
#    i = 0
#    end = 0
#    line = ''
#    if type( s ) != str:
#        s = str( s )
#    for c in s:
#        i += 1
#        if i % 16 == 1:
#            line += '%04X: ' % ( i - 1 , )
#        line += '%02X ' % ord(c)
#        if i % 8 == 0 and ( i / 8 ) % 2 == 1 :
#            line += '- '
#        if i % 16 == 0:
#            line += ' ' + ''.join( map( fmt , s[i-16:i] ) )
#            st.write( line + '\n' )
#            line = ''
#            end = i
#    if line :
#        line += ' ' * ( 56 - len( line ) )
#        st.write( line )
#        st.write( ' ' + ''.join( map( fmt , s[end:] ) ) + '\n' )
#    return st.getvalue()

di = { '0000':'0' , 
       '0001':'1' , 
       '0010':'2' , 
       '0011':'3' , 
       '0100':'4' , 
       '0101':'5' , 
       '0110':'6' , 
       '0111':'7' , 
       '1000':'8' , 
       '1001':'9' , 
       '1010':'A' , 
       '1011':'B' , 
       '1100':'C' , 
       '1101':'D' , 
       '1110':'E' , 
       '1111':'F' 
     }
id = { '0':'0000' , 
       '1':'0001' , 
       '2':'0010' , 
       '3':'0011' , 
       '4':'0100' , 
       '5':'0101' , 
       '6':'0110' , 
       '7':'0111' , 
       '8':'1000' , 
       '9':'1001' , 
       'A':'1010' , 
       'B':'1011' , 
       'C':'1100' , 
       'D':'1101' , 
       'E':'1110' , 
       'F':'1111' 
     }
     
def bin2hex( x ):
    i = 0
    s = ''
    while i < len(x):
        s = s + di.get(x[i:i+4])
        i = i + 4
    return s
def hex2bin( x ):
    i = 0
    s = ''
    while i < len(x):
        s = s + id.get(x[i])
        i = i + 1
    return s

def pack8583(t_dict , isomap = None , build_mac = None ):
    """
    8583报文打包
    参数列表
    t_dict 报文内容
    """
    for k,v in t_dict.items():
        t_dict.pop(k)
        t_dict[int(k)] = v
    
    if isomap is None:
        isomap = ISO8583
    buf = ''
    macstr= ''
    #提取有数据的域，key值是整数的
    field = list( filter( lambda x: type( x ) is int , t_dict.keys() ) )
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
    
    if sf16:
        macf = 128 
    else:
        macf = 64
    #macf = 128 if sf16 else 64
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
        macstr = t_dict.get(128)
    #生成位图
    #if not macstr:
    #    byte[-1] = byte[-1] & 0b11111110 # 去掉最后的mac域
        
    map = ''
    for b in byte:
        map = map + chr(b)
    t_dict[1] = map
    s1 = ''
    for i in range(0,macf + 1):
        if i in field:
            s1 = s1 + '1'
        else:
            s1 = s1 + '0'    
    map = '1'+s1[2:]
    print map
    #map = s1[1:]
    map = bin2hex(map)
    import binascii
    map = binascii.a2b_hex(map)
    ret = jym_b + map + buf + macstr
    
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
    elif ISO[4] == 'ASC':
        #print ISO[1],pos,i
        #print ISO[4],len(buf)
        length = ISO[2]
        tmp = ''
        value = buf[pos:pos+length]
        ori_val = tmp + value
        v_len = length
    else:
        #print ISO[1],pos,i
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
    elif ISO[4] == 'ASC':
        ret = v.ljust(ISO[2],' ')
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

def unpack8583( buf , isomap = None ):
    """
    8583报文解包
    参数列表 
    buf 报文内容
    mackey mac校验码
    """
    if isomap is None:
        isomap = ISO8583
    ret = {}
    # 先处理0,1域
    ori_val , value , pos = filed_decode( buf , isomap[0] , 0 , 0 )
    ori_ret = {}
    ret[0] = value  # 
    ori_ret[0] = ori_val
    if id.get(buf[4])[0] == '1':
        bLen = 128
        macf = 128
    else:
        bLen = 64
        macf = 64
    bitmap = '00' + hex2bin(buf[pos:bLen/4+pos])[1:]
#    print 'MTI' , value,pos,buf[pos],ord(buf[pos]),ord(buf[pos]) & 0x80
#    bLen = ord(buf[pos]) & 0x80 or 64 # 测试是否128位bitmap
#    print buf[4] , ord(buf[4]) , bLen ,bLen/8+4
#    bitmap = buf[pos:bLen/8+pos]
#    ret[1] = [ bLen , bitmap ] # bitmap
#    print 'BITMAP' , `bitmap`
#    pos = bLen/8 + pos
#    if bLen == 128:
#        macf = 128
#    else:
#        macf = 64
    # n1 = binascii.a2b_hex(n1)
    pos = bLen/4 + pos
    for i in range( 2 , bLen + 1 ):
        byte = bitmap[i]
        if byte == '1':
            ori_val , value , pos = filed_decode(buf,isomap[i],pos,i)
            ret[i] = value
            ori_ret[i] = ori_val
        
#        byte = bitmap[(i-1)/8] # get byte
#        bits = i % 8 or 8
#        print 'i',i,'byte',ord(byte),'bits',bits, ord( byte ) & bit[bits]
#        if ord( byte ) & bit[bits] : # test bit
#            ori_val , value , pos = filed_decode(buf,isomap[i],pos,i)
#            print ori_val , value , pos
#            if i in (35,36):
#                value = value.replace('d','=')
#            ret[i] = value
#            ori_ret[i] = ori_val
    for k,v in ret.items():
        ret.pop(k)
        ret[str(k)] = v
    return ret , ori_ret

if __name__ == '__main__':
    #E22244C128C098000000000010000001
    #E22244C128C098000000000010000001
    #0000000010000001
    #B22044D00AC088000000000016000041
    #'0200E22244C128C09800000000001000000119622359100000416783630000010161004532210191016676002100060803090000406223591000004167836d49121201410000000883221019      101     02101          15667BE7E2436719B8D20000000000000000881800101'
    buf = '0200E22244C128C09800000000001000000119622359100000416783630000010161004532210191016676002100060803090000406223591000004167836=49121201410000000883221019      101     02101          15667BE7E2436719B8D20000000000000000881800101E5C03534'
    #t = { 0: '0101' ,3:'400000',18:'6760', 64:'',102:'06223591000004163561',103:'16223591000004163561'  }
    #t = {0:'0200',3:'400000',4:'000012345600',7:'1204140341',11:'968510',18:'6760',22:'022',25:'00',26:'06',28:'D00000100',37:'968510',38:'      ',39:'00',41:'101',42:'812123456789022',49:'156',53:'200000000000000',100:'81800101',102:'06223591000004163561',103:'16223591000004163561',122:'999010999',128:'BCACEFE8'}
    t = {0:'0200',2:'6223591000004167836',3:'300000',7:'1016100453',11:'221019',15:'1016',18:'6760',22:'021',25:'00',26:'06',32:'03090000',35:'6223591000004167836=49121201410000000883',37:'221019',41:'101',42:'02101',49:'156',52:'67BE7E2436719B8D',53:'2000000000000000',100:'81800101',128:'E5C03534'}
#    print repr( pack8583( t )  )
    print unpack8583( buf , isomap = None )

