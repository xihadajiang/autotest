# coding: gbk
# �ֵ�_��������
import datetime
def now():
    return datetime.datetime.now().strftime( '%Y%m%d%H%M%S' )

# �û���
class GL_HYDY( settings.BaseModel ):
    __tablename__ = 'gl_hydy'
    hydm = Column( String(30) , primary_key = True )  # gl_hydy.hydm��������Ա
    gh   = Column( String(30) , nullable = False , unique = True ) # ����.�ɵ�¼,����ж����ѡ��,���г����û�ѡ�����������
    xm   = Column( String(40) , nullable = False ) # ����
    xb   = Column( String(1)  , nullable = False , default = '1' ) # �Ա�.2:Ů;1:��
    jgdm  = Column( Integer , ForeignKey( "gl_jgdy.jgdm" , enable = False ) , nullable = True ) # ��������
    sr   = Column( String(10) , nullable = True ) # ����
    mm   = Column( String(10)  , nullable = False , default='1'*8 ) # ���룬ǿ��8λ�����ı���
    zt   = Column( String(1)  , nullable = False , default= '0' ) # ״̬.0:����;1:����;2:���ܺ���ܵ�¼
    dlcs = Column( Integer    , default = 0 )      # ��½����
    jsdm = Column( String(4) , ForeignKey( 'gl_jsdy.jsdm' , enable = False ) , nullable = True )  # ��λ����
    kzjs = Column( String(100) , nullable = True ) # ��չ��ɫ��jsdm,
    
    profile = Column( String(20) , default = '1' )  # �������ã�Ĭ��1������1-8��ģ��
    
    kzpz    = Column( PickleType , nullable = True )      # ��չ���ã���ģ��������Ϣ���ֵ���
                                                          # shortcut����ݲ˵���gndm���б� []
                                                          # winexe:   windowsӦ�ÿ�ݷ�ʽ���б�[ ( ���� , path ) ]
                                                          # urls:     ������ַ �б�[ ( ����, url , user , pass ) ]
    zxsj    = Column( String(20) , default = '0' )             # ������ʱ�䣬�뵥λ
    ztgxsj  = Column( String(20) , default = now )             # ״̬����ʱ�䣬IEÿ��30��ˢ�¸��ֶ�
                                                          #      ����  ���ֶ�          ��ǰʱ��            ״̬          ����ʱ��ͳ��
                                                          #                0              0-120          ��ʾ����            +
                                                          #                0            121-300          ��ʾ����            +
                                                          #                0            301-?            ��ʾ����            
    # ��ϵ��ʽ
    dwdh    = Column( String(20) , nullable = True ) # ��λ�绰
    dwcz    = Column( String(20) , nullable = True ) # ��λ����
    sj      = Column( String(20) , nullable = True ) # �ֻ�
    xlt     = Column( String(20) , nullable = True ) # С��ͨ
    
    glqx    = Column( String(1)  , default = '0' )   # ����Ȩ��  0 ������ 1 ȫ�� 2 ָ������ 3:����
    sfcykp  = Column( String(1)  , default = '1' )   # �Ƿ���뿼��  1:����  0�������루����������Ҳ���ܴ�֣�
    zdglqx_id = Column( String(500) , nullable = True ) # ָ������Ȩ�� ID
    zdglqx_mc = Column( String(500) , nullable = True ) # ָ������Ȩ�� MC
    sskpjg_id = Column( String(1000) , nullable = True ) # ������������ ID
    sskpjg_mc = Column( String(1000) , nullable = True ) # ������������ MC
    jbdm  = Column( Integer , ForeignKey( "zd_hyjb.jbdm" , enable = False ) , nullable = True ) # ��Ա����
    gwdm  = Column( Integer , ForeignKey( "zd_gwdy.gwdm" , enable = False ) , nullable = True ) # ��Ա��λ
    #zdm  = Column( Integer , ForeignKey( "zd_yhz.zdm" , enable = False ) , nullable = True ) # ��Ա��
    sfbhzbm = Column( String(1)  , default = '0' )   # �Ƿ�����Ӳ���  0 ������ 1 ����
    bz      = Column( String(200) , nullable = True )  # ��ע
    fj   = Column( String(500) , nullable = True ) # ��Ƭ
    onlinestate = Column( String(1)  , nullable = False, default='0' ) # ״̬.0:����;1:����;2:���� Ĭ������
    singlesignon = Column( String(1)  , nullable = False, default='1' ) # �����¼ģʽ
    cxgyh = Column(  String(12) , nullable = True )# �����Ա�� 
    dggyh = Column(  String(12) , nullable = True ) #�Թ���Ա�� 
    jsobj = relation( 'GL_JSDY' , uselist = False )
    
    def get_jslist( self ):
        se = settings.DB_SESSION()
        jslist = filter( None , self.kzjs.split( ',' ) ) if self.kzjs else []
        jslist = se.query( GL_JSDY ).filter( GL_JSDY.jsdm.in_( jslist ) ).order_by( GL_JSDY.xh ).all()
        jslist.insert( 0 , se.query( GL_JSDY ).get( self.jsdm ) )
        return jslist
    
    jslist = property( get_jslist )
    
    def get_gnlist( self ):
        gnlist = {}
        for js in self.jslist:
            gnlist.update( dict( ( ( gn.gndm , gn ) for gn in js.gnlist ) ) )
        return gnlist
    
    def get_hylist( se , hylist ):
        ret = []
        if hylist:
            hylist = filter( None , hylist.split( ',' ) )
            ret = map( se.query( GL_HYDY ).get , hylist )
        return ret
    
    def filter( self , hylist , sess ):
        # ���ݱ��˵Ĺ���Ȩ�ޣ�����hylist
        if self.glqx == '0':
            # ������
            jglist = [self.jgdm ] + [ x.jgdm for x in self.jgobj.get_all_children() ]
        elif self.glqx == '2':
            # ��������
            qtbm = filter( None , self.zdglqx_id.split( ',' ) )
            jglist = [ x.jgdm for x in self.jgobj.get_all_children() ]
            for y in sess.query( GL_JGDY ).filter( GL_JGDY.jgdm.in_( qtbm ) ):
                jglist.extend( [y.jgdm])
                jglist.extend( [ x.jgdm for x in y.get_all_children() ] )
        else:
            hylist = filter(None , hylist)
            try:
                hylist.sort( key=lambda x:[x.jgobj.jglxobj.xh , x.jgobj.xh])
            except:
                hylist.sort( key=lambda x:[ x.jgobj.xh if x.jgobj else ''])
            return hylist
        hylist = filter( lambda x: x.jgdm in jglist , hylist )
        try:
            
            hylist.sort( key=lambda x:[x.jgobj.jglxobj.xh , x.jgobj.xh])
        except:
            hylist.sort( key=lambda x:[ x.jgobj.xh])
        return hylist
    def get_jglxlist( self , se ):##���ݱ��˵Ĺ���Ȩ�ޣ��ó����˿��Թ���Ļ�������
        
        q = se.query( ZD_JGLX ).filter(ZD_JGLX.jglx>0)
        
        if self.glqx=='2':#ָ������
            zdjglist = filter(None,self.zdglqx_id.split(','))
            jglxlb=[]
            for obj in se.query( GL_JGDY ).filter( GL_JGDY.jgdm.in_(zdjglist)):
                jglxlb.append( obj.jglx )
            q  =q.filter( ZD_JGLX.jglx.in_(jglxlb))
        if self.glqx=='0':##������
            q = q.filter( ZD_JGLX.jglx == self.jgobj.jglx)
        q = q.order_by( ZD_JGLX.xh )
        jglxlist = q.all()
        return jglxlist
    
    def get_hyjblist( self , se ):
        q = se.query( ZD_HYJB ).filter(ZD_HYJB.jbdm>0)
        if self.glqx=='2':
            
            jglist = filter(None,self.zdglqx_id.split(','))
            hylist = se.query(GL_HYDY).filter( GL_HYDY.jgdm.in_(jglist)).all()
            hyjb_lb = filter(None , map( lambda x:x.jbdm , hylist))
            q  =q.filter( ZD_HYJB.jbdm.in_(hyjb_lb))
        elif self.glqx=='0':
            jglist = [self.jgobj.jgdm]
            hylist = se.query(GL_HYDY).filter( GL_HYDY.jgdm.in_(jglist)).all()
            hyjb_lb = filter(None , map( lambda x:x.jbdm , hylist))
            q  =q.filter( ZD_HYJB.jbdm.in_(hyjb_lb))
        q = q.order_by( ZD_HYJB.xh )
        hyjblist = q.all()
        return hyjblist