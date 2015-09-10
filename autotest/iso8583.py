# coding: gbk

"""
    8583���ĵĽ���ʹ��
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
#��ʽ����(�������Ƿ�䳤��־0-�� 2-2λ�䳤 3-3λ�䳤 �������򳤶ȣ��䳤�ֱ�Ϊ99 999 ��
#�������ͣ�0-string 1-int 2-binary , �������ͣ�BCD BIN ASC ����BCD���룬���Ⱦ�Ϊ�Ҷ��룬����LΪ����룬RΪ�Ҷ���)
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
54  :("���ӽ��"                    , 3 , 20    , 0 , 'BIN')   ,
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
65  :("NO USE"                      , 3 , 999   , 0 , '')   ,
66  :("NO USE"                      , 0 , 1     , 0 , '')   ,
67  :("NO USE"                      , 3 , 999   , 0 , '')   ,
68  :("NO USE"                      , 3 , 999   , 0 , '')   ,
69  :("NO USE"                      , 3 , 999   , 0 , '')   ,
70  :("������Ϣ��"                  , 0 , 3     , 0 , '')   ,
71  :("NO USE"                      , 3 , 999   , 0 , '')   ,
72  :("NO USE"                      , 3 , 999   , 0 , '')   ,
73  :("NO USE"                      , 0 , 6     , 0 , '')   ,
74  :("���ǽ��ױ���"                , 0 , 10    , 0 , '')   ,
75  :("�����Զ��������ױ���"        , 0 , 10    , 0 , '')   ,
76  :("��ǽ��ױ���"                , 0 , 10    , 0 , '')   ,
77  :("����Զ��������ױ���"        , 0 , 10    , 0 , '')   ,
78  :("ת�ʽ��ױ���"                , 0 , 10    , 0 , '')   ,
79  :("ת���Զ��������ױ���"        , 0 , 10    , 0 , '')   ,
80  :("��ѯ���ױ���"                , 0 , 10    , 0 , '')   ,
81  :("��Ȩ���ױ���"                , 0 , 10    , 0 , '')   ,
82  :("NO USE"                      , 0 , 12    , 0 , '')   ,
83  :("���ǽ��׷ѽ��"              , 0 , 12    , 0 , '')   ,
84  :("NO USE"                      , 0 , 12    , 0 , '')   ,
85  :("��ǽ��׷ѽ��"              , 0 , 12    , 0 , '')   ,
86  :("���ǽ��׽��"                , 0 , 16    , 0 , '')   ,
87  :("�����Զ��������"            , 0 , 16    , 0 , '')   ,
88  :("��ǽ��׽��"                , 0 , 16    , 0 , '')   ,
89  :("����Զ��������׽��"        , 0 , 16    , 0 , '')   ,
90  :("ԭ���׵�����Ԫ��"            , 0 , 42    , 0 , '')   ,
91  :("�ļ��޸ı���"                , 0 , 1     , 0 , '')   ,
92  :("NO USE"                      , 3 , 999   , 0 , '')   ,
93  :("NO USE"                      , 3 , 999   , 0 , '')   ,
94  :("����ָʾ��"                  , 0 , 7     , 0 , '')   ,
95  :("������"                    , 0 , 42    , 0 , '')   ,
96  :("NO USE"                      , 0 , 8     , 0 , '')   ,
97  :("��������"                  , 0 , 16    , 0 , '')   ,
98  :("NO USE"                      , 3 , 999   , 0 , '')   ,
99  :("���������"                  , 2 , 11    , 0 , '')   ,
100 :("���ջ�����"                  , 2 , 11    , 0 , '')   ,
101 :("�ļ���"                      , 2 , 17    , 0 , '')   ,
102 :("�ʺ�1"                       , 2 , 28    , 0 , '')   ,
103 :("�ʺ�2"                       , 2 , 28    , 0 , '')   ,
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
123 :("����������"                  , 3 , 8     , 2 , '')   ,
124 :("NO USE"                      , 3 , 999   , 0 , '')   ,
125 :("NO USE"                      , 3 , 999   , 0 , '')   ,
126 :("NO USE"                      , 3 , 999   , 0 , '')   ,
127 :("NO USE"                      , 3 , 999   , 0 , '')   ,
128 :("��Ϣȷ����"                  , 0 , 8     , 2 , '')   ,
}


#macfield = (2,3,4,11,12,13,32,38,39,41,49,95)

def unpack8583( buf , isomap = None ):
    """
    8583���Ľ��
    �����б� 
    buf ��������
    mackey macУ����
    """
#    if isomap is None:
#        isomap = ISO8583
    isomap = ISO8583
    ret = {}
    # �ȴ���0,1��
    ori_val , value , pos = filed_decode( buf , isomap[0] , 0 , 0 )
    ori_ret = {}
    ret[0] = value  # 
    ori_ret[0] = ori_val
    #print 'MTI' , value
    bLen = ord(buf[pos]) & 0x80 or 64 # �����Ƿ�128λbitmap
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
    8583���Ĵ��
    �����б�
    t_dict ��������
    """
    if isomap is None:
        isomap = ISO8583
    buf = ''
    macstr= ''
    #��ȡ�����ݵ���keyֵ��������
    field = list( filter( lambda x: type( x ) is int , t_dict.keys() ) )
    #print field
    #��ȡ������
    ori_fields = {}
    jym = t_dict[0]
    #�ж�λͼ��64����128λ��ʹ��65�Ժ����
    sf16 = max( field ) >= 65 

    #��ʼ��λͼ
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
        field.append( macf ) # �Ƚ�mac�����

    field.sort() 
    #����64��128����
    for i in range(2 , blen*8 + 1 ):
        #�������Ӧλͼλ��
        bytes = ( i - 1 ) / 8
        bits = i % 8 or 8
        #print i,bytes,bits
        #������ֵ
        if i in field:
            #����λͼ��Ӧλ
            byte[bytes] = byte[bytes] + bit[bits]
            if i != macf: #64 128�򵥶�����
                v = str(t_dict[i])
                if i in (35,36):
                    v = v.replace('=','d')
                v = field_encode(isomap[i],v)
                buf += v
                ori_fields[ i ] = v
    
    #�����鴮
    jym_b = field_encode( isomap[0] , jym )  # ����8583�淶���
    ori_fields[0] = jym_b
    if callable( build_mac ):
        macstr = build_mac( ori_fields )
    else:
        macstr = ''
    #print byte
    #����λͼ
    if not macstr:
        byte[-1] = byte[-1] & 0b11111110 # ȥ������mac��
        
    map = ''
    for b in byte:
        map = map + chr(b)
    t_dict[1] = map
    # 
    ret = jym_b + map + buf + macstr
    
    return ret


def field_encode(ISO,v):
    #BCDѹ��
    if ISO[4] in ('BCDL','BCDR','BASC'):
        v_len = len(v)  #BCDѹ����ĳ���
        #����λ�ĸ��ݶ��뷽ʽǰ����
        if (v_len % 2) == 1:
            if ISO[4] == 'BCDL':
                v = v + '0'
            elif ISO[4] == 'BCDR':
                v = '0' + v
        #�䳤�ֶ�д��ʵ�ʳ��ȣ�������ѹ����ĳ���
        if ISO[1] == 2: # ��λ�䳤��
            v_len = '%02d' % v_len 
        elif ISO[1] == 3: # ��λ�䳤��ǰ����
            v_len = '%04d' % v_len 
        else:#������
            v_len = ''
        v_len = v_len.decode( 'hex' )
        if 'BCD' in ISO[4]:
            v = v.decode( 'hex' )
        ret = v_len + v
    else:
        v_len = len(v)
        if ISO[1] == 2: # ��λ�䳤��
            value = '%02d' %  v_len
            value += v
            #value = binascii.a2b_hex(value) + v
        elif ISO[1] == 3: # ��λ�䳤��
            value = '%03d' %  v_len
            value += v
            #value = binascii.a2b_hex(value) + v
        else:#������
            value = v
        ret = value
    #print ret
    return ret


def filed_decode(buf,ISO,pos,i):
    #BCD��ѹ��
    if ISO[4] in ('BCDL','BCDR','BASC'):
        if ISO[1] == 2: # 2�ֽڳ�����
            #ȡ����
            tmp = buf[pos:pos+1]
            tmp = binascii.b2a_hex(tmp)
            length = int( tmp )
            #print i , '��λ���ȱ䳤��:len[%s]' % length ,
            pos += 1
        elif ISO[1] == 3: # 3�ֽڳ�����
            tmp = buf[pos:pos+2]
            #print tmp
            tmp = binascii.b2a_hex(tmp)
            #print tmp
            length = int( tmp )
            #print length
            #print i , '��λ���ȱ䳤��:len[%s]' % length ,
            pos += 2
        else:
            #print i , '������:len[%d]' % ISO[2] ,
            length = ISO[2]
            tmp = ''
        #ret[i] = [ length , buf[pos:pos+length] ]
        #����ѹ����ĳ���
        v_len = (length + 1) / 2
        value = buf[pos:pos+v_len]
        ori_val = tmp + value
        if 'BCD' in ISO[4]:
            value = binascii.b2a_hex(value)
            #����λ�ĸ��ݶ��뷽ʽǰ�����ȥ��
            if (length % 2) == 1:
                if ISO[4] == 'BCDL':
                    value = value[:-1]
                else:
                    value = value[1:]
    else:
        if ISO[1] == 2: # 2�ֽڳ�����
            tmp = buf[pos:pos+2]
            length = int( tmp )
            #print i , '��λ���ȱ䳤��:len[%s]' % length ,
            pos += 2
            #print i , '��λ���ȱ䳤��:len[%s]' % buf[pos:pos+2] ,
            #length = int( buf[pos:pos+2] )
            #pos += 2
        elif ISO[1] == 3: # 3�ֽڳ�����
            tmp = buf[pos:pos+3]
            #print tmp
            length = int( tmp )
            #print length
            #print i , '��λ���ȱ䳤��:len[%s]' % length ,
            pos += 3

            #print i , '��λ���ȱ䳤��:len[%s]' % buf[pos:pos+3] ,
            #length = int( buf[pos:pos+3] )
            #pos += 3
        else:
            #print i , '������:len[%d]' % ISO[2] ,
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
    #PIN�����
    try:
        #PIN������
        PIN = t_dict[52]
        #���ܷ�ʽ
        jmfs = t_dict[53]
    except:
        raise RuntimeError( 'δ�ṩPIN�����ܷ�ʽ' )
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
                    raise RuntimeError( 'δ�ṩ35��36��' )
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
    """mac����
    �����б�
    buf  ��������
    mackey
    """
    des = DES.new(mackey,DES.MODE_ECB)
    #�ֽڲ���8�ı���
    buf = buf + '\x00' * ( 8 - ( len(buf) % 8 ) )
    #print buf

    tmp = buf[:8]
    tmp1 = ''
    #ÿ8���ֽ�һ�飬����ȡ����򣬵�һ����ڶ�����򣬽��������������������
    for i in range(0,len(buf)/8 - 1):
        for l in range(0,8):
            #print i,l,tmp[l],buf[(i+1)*8+l],tmp1
            tmp1 += chr(ord(tmp[l]) ^ ord(buf[(i+1)*8+l]))
        tmp = tmp1
        tmp1 = ''
    #print `tmp`

    #�����������ת��Ϊ16��hex
    for i in range(0,8):
        #print '%02X'%(ord(tmp[i]))
        tmp1 += '%02X'%(ord(tmp[i]))
    #print tmp1

    #ǰ8λdes���������8λ���
    tmp2 =  des.encrypt(tmp1[:8])
    #print `tmp2`
    tmp = ''
    for i in range(0,8):
        #print tmp2[i],tmp1[i+8]
        tmp += chr(ord(tmp2[i]) ^ ord(tmp1[i+8]))
    #print `tmp`

    #�ٴν���des���ܣ������ܽ��ת��Ϊ16��hex
    tmp =  des.encrypt(tmp)
    tmp1 = ''
    for i in range(0,8):
        #print '%02X'%(ord(tmp[i]))
        tmp1 += '%02X'%(ord(tmp[i]))
    #print tmp1

    #ȡǰ8λ����
    return tmp1[:8]


def mac_encode(buf,mackey):
    """mac���� des����
    �����б�
    buf  ��������
    mackey macУ����
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
    """mac���� ��des��������
       �����б�
       buf ��������
       mackey macУ����
    """
    des = DES.new(mackey,DES.MODE_CBC)

    #buf = buf + '\x00' * ( 8 - ( len(buf) % 8 ) )
    ret = des.decrypt(buf)
    return ret

import re

p = re.compile( '\d{6}' )


def kmm_decode(sbbh,kmm_en):
    """��������ܣ������豸��mackey ��des���ܵĽ��ܷ���
        �����б� 
        sbbh �豸���
        kmm_en  ���ܵĿ�����
    """
    #print '���ܵĿ����룺%s'%kmm_en
    sbobj = GL_SBDY.get_by(bh = sbbh)
    if sbobj:
        mackey = sbobj.mackey
    else:
        raise RuntimeError("�豸��ŷǷ�")
    #print "mackey:",mackey
    mackey = binascii.a2b_hex(mackey)
    kmm_en = binascii.a2b_hex(kmm_en)
    #�����豸��ˮ�����ɹ�����Կ
    des = DES.new(mackey,DES.MODE_CBC)
    kmm_de = des.decrypt(kmm_en)
    #print '���ܵĿ����룺%s'%kmm_de[:6]
    if p.match( kmm_de[:6] ):
        return kmm_de[:6]
    else:
        raise RuntimeError( '��������ʽ����[%s]' % `kmm_de[:6]` )


def make_mackey(sbbh,sblsh):
    """�豸������Կ���ɣ�DES����
       �����б�
       sbbh �豸���
       sblsh �豸��ˮ��
    """
    with connection() as con:
        cur = con.cursor()
        rs = sql_execute( cur , "select mainkey from gl_sbdy where bh = %s for update" , [ sbbh ] )
        if rs.next():
            mainkey = rs.getString( 'mainkey' )
            mainkey = binascii.a2b_hex(mainkey)
            #�����豸��ˮ�����ɹ�����Կ
            des = DES.new(mainkey,DES.MODE_CBC)
            sblsh = '%08d'%sblsh
            mackey_en = des.encrypt(sblsh)
            mackey = binascii.b2a_hex(mackey_en)
            #print "�����µĹ�����Կ��%s"%mackey
            cur.execute( "update gl_sbdy set mackey = %s where bh = %s" , [ mackey , sbbh ] )
        else:
            raise RuntimeError("�豸��ŷǷ�")
    
    #�Թ�����Կ�ٴν��м��ܣ����͵��豸
    des = DES.new(mainkey,DES.MODE_CBC)
    mackey1 = des.encrypt(mackey_en)
    mackey1 = binascii.b2a_hex(mackey1)
    #print "������Կ�ٴν��м��ܣ�%s"%mackey1
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
