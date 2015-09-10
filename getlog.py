#Tianhc 2014.11
#mode by lp_zxy 201409, 运行LOGFILESIZE + LLOGTIMEZONE功能
#定位分段日志文件shell
#输入参数 getlog.py DATE SYSNAME MODE LSH 
#MODE 1--指定流水号,其它取最新一个日志文件
import os
os.environ.get('HOME')
def getlog(DATE,SYSNAME,MODE,LSH ):
    f = open('$HOME/tmp/tmp_${SYSNAME}.file','w')