# coding: gbk
# 字典_数据周期
import datetime
def now():
    return datetime.datetime.now().strftime( '%Y%m%d%H%M%S' )
#def Column():
from sqlalchemy import *
#from sqlalchemy.orm import *
#from sqlalchemy.ext.declarative import *

# 用户表
class GL_HYDY():
    __tablename__ = 'gl_hydy'
    hydm = Column( String(30) , primary_key = True )  # gl_hydy.hydm，所属人员
    gh   = Column( String(30) , nullable = False , unique = True ) # 工号.可登录,如果有多个可选择,则列出由用户选择后输入密码
print GL_HYDY.hydm,GL_HYDY.__tablename__
GL_HYDY.hydm = '3333'
print GL_HYDY.hydm
print Column( String(30) , primary_key = True )
import os
for path, dir, files in os.walk( 'F:/Django/pyhttp/autotest/data' ):
    print path, dir, files
    for file in files:
        print file
        print path.strip('F:/Django/pyhttp/autotest/data')
