# coding: gbk
# �ֵ�_��������
import datetime
def now():
    return datetime.datetime.now().strftime( '%Y%m%d%H%M%S' )
#def Column():
from sqlalchemy import *
#from sqlalchemy.orm import *
#from sqlalchemy.ext.declarative import *

# �û���
class GL_HYDY():
    __tablename__ = 'gl_hydy'
    hydm = Column( String(30) , primary_key = True )  # gl_hydy.hydm��������Ա
    gh   = Column( String(30) , nullable = False , unique = True ) # ����.�ɵ�¼,����ж����ѡ��,���г����û�ѡ�����������
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
