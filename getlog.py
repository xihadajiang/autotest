#Tianhc 2014.11
#mode by lp_zxy 201409, ����LOGFILESIZE + LLOGTIMEZONE����
#��λ�ֶ���־�ļ�shell
#������� getlog.py DATE SYSNAME MODE LSH 
#MODE 1--ָ����ˮ��,����ȡ����һ����־�ļ�
import os
os.environ.get('HOME')
def getlog(DATE,SYSNAME,MODE,LSH ):
    f = open('$HOME/tmp/tmp_${SYSNAME}.file','w')