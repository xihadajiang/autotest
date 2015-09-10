# coding: gbk
# �ֵ�_��������
from shangjie.conf import settings
from sqlalchemy import *
from sqlalchemy.orm import *
from djangoext.sqlalchemy import ForeignKey
from sqlalchemy.ext.declarative import *
from shangjie.utils.ftools import register
from djangoext.mako import render_to_string

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
    
    @staticmethod
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
# ��������
class GL_JGDY( settings.BaseModel ):
    __tablename__ = 'gl_jgdy'
    jgdm = Column( Integer , primary_key = True ) # 
    xh   = Column( Integer , default = 0 ) # ���������
    ywjgdm = Column( String(20) , nullable = True ) # ҵ���������
    jgmc = Column( String(40) , nullable = False ) # ��������
    zt   = Column( String(1)  , nullable = False ) # ״̬��0���ã�1���� Ĭ��0
    dh   = Column( String(20) , nullable = True  ) # �绰
    cz   = Column( String(20) , nullable = True  ) # ����
    
    sjbm = Column( Integer , ForeignKey( 'gl_jgdy.jgdm' , enable = False ) , nullable = True )  # �ϼ�����
    bmzg = Column( String(100) , nullable = True )  # ��������
    sjzg = Column( String(100) , nullable = True )  # �ϼ�����
    sjfg = Column( String(100) , nullable = True )  # �ϼ��ֹ�
    jglx  = Column( Integer , ForeignKey( "zd_jglx.jglx" , enable = False ) , nullable = True ) # �������ͣ����ء�Ӫ������֧���������� 
    
    bmzn = Column( String(200) , nullable = True ) # ����ְ��
    gggy = Column( String(40) , nullable = True ) #������Ա
    
    children = relation( 'GL_JGDY' , order_by = [ xh ] , backref = backref( 'parent' , remote_side=[jgdm] ) )
    hylist = relation( 'GL_HYDY' , order_by = [ GL_HYDY.hydm ] , backref = backref( 'jgobj' , uselist = False ) )
    
    
    def get_children( self ):
        return self.children
    
    def get_all_children( self ):
        r = self.children[:]
        for x in self.children:
            r.extend( x.get_all_children() )
        return r
    
    @staticmethod
    def bm_tree( se, jglist ):
#        """
#            root Ϊ���ڵ�, Ϊ�ձ�ʾȫ��
#        """
        out = []
#        if root == '':
#            r = None
#            children = se.query( GL_JGDY ).filter( and_( GL_JGDY.sjbm == None , GL_JGDY.zt == '0' ) ).all()
#        else:
#            r = se.query( GL_JGDY ).get( root )
#            if r is None:
#                raise RuntimeError( '�Ҳ���ָ���Ļ���' )
#            out.append( ( r.jgdm , r.jgmc ) )
#            children = r.get_children()
        indexdic = GL_JGDY.filter(jglist)
        
        def build_tree( tobj , prefix , parent_next , self_next , first = True ):
            n_prefix = prefix + ( ( '��' if first == False else '' ) if parent_next == False else '��' )
            if indexdic[tobj.jgdm]['access']==True:
                jgdm = tobj.jgdm
                jgmc =tobj.jgmc

            else:
                jgdm=-1
                jgmc=''
            out.append( ( jgdm , n_prefix + ( '��' if self_next == False else '��' ) + jgmc ) )
            
            ch = indexdic[tobj.jgdm]['children']  #tobj['children'].get_children()  
            ma = len( ch )
            for i in range( ma ):
                build_tree( ch[ i ]['obj'] , n_prefix , self_next , i < ma-1 , first = False )
        
        children = indexdic['ROOT']['children']
        maxc = len( children )
        for i in range( maxc ):
            build_tree( children[ i ]['obj'], '' , False , i < maxc-1 )
            
        return out
    
    #��ȡ֧�в�����
    @staticmethod
    def get_zh_bm_tree(se  ,jglist ):
        jglist = filter(lambda x:x.jglxobj and x.jglxobj.xz=='zh' , jglist)
        bm_tree = GL_JGDY.bm_tree( se  , jglist )
        return bm_tree
    
    
    @staticmethod
    def filter(jglist):
        indexdic={'ROOT':{'name':'ROOT','children':[],'xssx':0}}
        def buildtree(jgobj):
            
            if jgobj.jgdm in indexdic.keys():
                return 
            tobj = {'name':jgobj.jgdm , 'children':[] , 'xssx':jgobj.xh , 'obj':jgobj , 'access':False}
            if jgobj in jglist:
                tobj['access'] = True
            indexdic[jgobj.jgdm] = tobj
            
            if jgobj.sjbm is None:
                sjbm='ROOT'
            else:
                buildtree(jgobj.parent)
                sjbm = jgobj.sjbm
            indexdic[sjbm]['children'].append(tobj)
            
        for x in jglist:
            buildtree(x)
#        ##��Կɷ��ʵ�Ҷ�ӹ�������
#        def build_children( jgobj ):
#            tobj = indexdic[ jgobj.jgdm ]
#            tobj['access'] = True
#            for c in jgobj.children:
#                if c.jgdm in indexdic.keys():
#                    indexdic[ c.jgdm]['access'] = True # ����Ϊ�ɷ���
#                    continue 
#                cobj={'name':c.jgdm , 'children':[],'xssx':c.xh , 'obj':c,'access':False}
#                indexdic[c.jgdm] = cobj
#                tobj['children'].append( cobj )
#                build_children( c )
#
#        for x in jglist:
#            build_children(x)
        
#        ##������---------------------
#        def build_tree( tobj , prefix , parent_next , self_next , first = True ):
#            n_prefix = prefix + ( ( '��' if first == False else '' ) if parent_next == False else '��' )
#            out.append( ( tobj.jgdm , n_prefix + ( '��' if self_next == False else '��' ) + tobj.jgmc ) )
#            ch = tobj.get_children()
#            ma = len( ch )
#            for i in range( ma ):
#                build_tree( ch[ i ] , n_prefix , self_next , i < ma-1 , first = False )
        
        ##�Թ����Ĺ�������������
        for k,v in indexdic.items():
            if len(v['children'])!=0:
                v['children'].sort(key = lambda x :x['xssx'])
            
#        for obj in indexdic['ROOT']['children']:
#            
#            if obj['access']:
#                out.append((obj['obj'].jgdm , obj['obj'].jgmc))
#            else:
#                out.append((-1 , ''))
#            children = obj['children']
#            maxc = len( children )
#            for i in range( maxc ):
#                build_tree( children[ i ]['obj'] , '' , False , i < maxc-1 )
        return indexdic
    
    def get_zg( self , se , kind ):
        """
            ��ȡ����
        """
        hylist = filter( None , ( getattr( self , kind , '' ) or '' ).split( ',' ) )
        if hylist:
            return se.query( GL_HYDY ).filter( GL_HYDY.hydm.in_( hylist ) ).order_by( GL_HYDY.hydm ).all()
        else:
            return []
    
    def get_jg_path( self , sep = '/' ):
        if self.parent:
            return self.parent.jgpath + sep + self.jgmc
        else:
            return self.jgmc
            
    jgpath = property( get_jg_path )
    
class GL_GNDY( settings.BaseModel ):
    ROOTDM = 'root'
    
    __tablename__ = 'gl_gndy'
    gndm = Column( String(10)  , nullable = False , primary_key = True ) # ���ܴ���
    gnmc = Column( String(80)  , nullable = False ) # ��������
    url  = Column( String(255) , nullable = True ) # ���ܶ�Ӧurl.webϵͳ����Ե�ַ
    gnjb = Column( Numeric( 2 , 0 , asdecimal = False ), nullable = False ) # ���ܼ���
    xssx = Column( Integer , nullable = False ) # ��ʾ˳��
    sjdm = Column( String(10)  , ForeignKey('gl_gndy.gndm' , enable = False ), nullable = False ) # �ϼ�����.���������Ϊroot
    sfmx = Column( String(1)   , nullable = False ) # �Ƿ���ϸ.0:��;1=��
    bz   = Column( String(255) , nullable = True )  # ��ע.���ڱ���Ĺ�������,���ֶε����ݽ�������Ϊ����ļ��
    img  = Column( String(255) , nullable = True )  # �˵�ͼ��
    sfwh = Column( String(1)   , nullable = True ) # �ɷ�ά�� 0:��;1:�� �յĻ�Ҳ�ǲ���ά��
    
    children = relation('GL_GNDY', backref = backref( 'parent' , remote_side=[gndm] ) )
    
    @staticmethod
    def buildmenu( gnlist , linefmt , sess , extra = None , caname = 'gn' ):
        """ ����ָ���Ĺ����б��ݹ�ʵ������
            ��������������
        """
        from shangjie.utils import cache
        import copy
        if caname:
            ca = cache.get_cache( caname , expiretime = 300 )
        else:
            ca = {}
        indexdic = { GL_GNDY.ROOTDM: { 'name':GL_GNDY.ROOTDM , 'children':[] , 'xssx':0 } }
        
        def buildtree( gndm ):
            if gndm in indexdic:
                return
            
            try:
                if caname:
                    tobj = copy.deepcopy( ca.get( gndm ) )  # ���ȴӻ����л�ȡ
                else:
                    tobj = ca[ gndm ]
            except KeyError:
                gnobj = sess.query( GL_GNDY ).get( gndm )
                if not gnobj:
                    raise RuntimeError( '����[%s]�޷��ҵ�' % gndm )
                    
                tobj = {'name':gndm,'children':[],'content':render_to_string( linefmt , gn = gnobj , extra = extra ),'xssx':gnobj.xssx , 'url':gnobj.url , 'gnjb': gnobj.gnjb , 'sjdm': gnobj.sjdm }
                if caname:
                    ca.put( gndm , copy.deepcopy( tobj ) )
                else:
                    ca[ gndm ] = tobj
                
            indexdic[ gndm ] = tobj
            sjdm = tobj['sjdm']
            if sjdm not in indexdic.keys():
                buildtree( sjdm )
                
            indexdic[ sjdm ]['children'].append( tobj )
            
        for g in gnlist:
            buildtree( g )
        
        #�Թ����Ĺ�������������
        leaves = [] # ����Ҷ�ӣ�����ʹ��sfmx�ֶΡ�
        for k , value in indexdic.items():
            if len( value['children'] ) == 0:
                leaves.append( k )
            else:
                value[ 'children' ].sort( key = lambda x:x['xssx'] )
                
        # ����Ҷ�ӽڵ㣬���ǲ���Ҫ�����������֣������еĸ��ڵ��Ѿ������ã�
        for k in leaves:
            indexdic.pop( k )
        return indexdic

    @staticmethod
    def gn_tree( se , root = '' ):
        """
            root Ϊ���ڵ�, Ϊ�ձ�ʾȫ��
        """
        out = []
        if root == '':
            r = None
            children = se.query( GL_JSDY ).filter( GL_JSDY.sjdm == None ).all()
        else:
            r = se.query( GL_JSDY ).get( root )
            if r is None:
                raise RuntimeError( '�Ҳ���ָ���Ĺ���' )
            out.append( ( r.jsdm , r.jsmc ) )
            children = r.get_children()
        
        def build_tree( tobj , prefix , parent_next , self_next , first = True ):
            n_prefix = prefix + ( ( '��' if first == False else '' ) if parent_next == False else '��' )
            out.append( ( tobj.jsdm , n_prefix + ( '��' if self_next == False else '��' ) + tobj.jsmc ) )
            ch = tobj.get_children()
            ma = len( ch )
            for i in range( ma ):
                build_tree( ch[ i ] , n_prefix , self_next , i < ma-1 , first = False )
        
        maxc = len( children )
        for i in range( maxc ):
            build_tree( children[ i ] , '' , False , i < maxc-1 )
        return out
    
    @staticmethod
    def filter( gnlst ):
        indexdic={'ROOT':{'name':'ROOT','children':[],'xssx':0}}
        def buildtree(gnobj):
            if gnobj.gndm in indexdic.keys():
                return 
            tobj = {'name':gnobj.gndm , 'children':[] , 'xssx':gnobj.xssx , 'obj':gnobj }
            indexdic[gnobj.gndm] = tobj
            if gnobj.sjdm =='root':
                sjdm='ROOT'
            else:
                buildtree(gnobj.parent)
                sjdm = gnobj.sjdm
            indexdic[sjdm]['children'].append(tobj)
            
        for x in gnlst:
            buildtree(x)

        ##�Թ����Ĺ�������������
        for k,v in indexdic.items():
            if len(v['children'])!=0:
                v['children'].sort(key = lambda x :x['xssx'])
        return indexdic

    @staticmethod
    def get_gn_tree( gnlst ):
#        """
#            ���ع�����
#        """
        out = []

        indexdic = GL_GNDY.filter( gnlst )
        
        def build_tree( tobj , prefix , parent_next , self_next , first = True ):
            n_prefix = prefix + ( ( '��' if first == False else '' ) if parent_next == False else '��' )
            gndm = tobj.gndm
            gnmc =tobj.gnmc
            out.append( ( gndm , n_prefix + ( '��' if self_next == False else '��' ) + gnmc ) )
            
            ch = indexdic[tobj.gndm]['children']  #tobj['children'].get_children()  
            ma = len( ch )
            for i in range( ma ):
                build_tree( ch[ i ]['obj'] , n_prefix , self_next , i < ma-1 , first = False )
        
        children = indexdic['ROOT']['children']
        maxc = len( children )
        for i in range( maxc ):
            build_tree( children[ i ]['obj'], '' , False , i < maxc-1 )
            
        return out
    #���ع���·��
    def get_gn_path( self , sep = '/' ):
        if self.parent:
            return self.parent.gnpath + sep + self.gnmc
        else:
            return self.gnmc
            
    gnpath = property( get_gn_path )




class GL_JSDY( settings.BaseModel ):
    # ����_��ɫ����
    __tablename__ = 'gl_jsdy'
    jsdm = Column( String(4) , primary_key = True ) # ��ɫ����
    xh   = Column( Integer , default = 0 )  # ���
    
    jsmc = Column( String(40) , nullable = False ) # ��ɫ����
    
    def get_hylist( self ):
        se = settings.DB_SESSION()
        return se.query( GL_HYDY ).filter( and_( GL_HYDY.zt == '0' , or_( GL_HYDY.jsdm == self.jsdm , GL_HYDY.kzjs.like( '%%%s%%,' % self.jsdm ) ) ) ).all()
        
    hylist = property( get_hylist )
    

class GL_JSGNDY( settings.BaseModel ):
    # ����_��ɫ���ܶ���
    __tablename__ = 'gl_jsgndy'
    gndm = Column( String(10) , ForeignKey( "gl_gndy.gndm" , enable = False ) , primary_key = True ) # ���ܴ���
    jsdm = Column( String(4) , ForeignKey( "gl_jsdy.jsdm" , enable = False ) , primary_key = True ) # ��ɫ����
    qxxx = Column( PickleType , nullable = True ) # Ȩ����Ϣ

GL_JSDY.gnlist = relation( 'GL_GNDY' , secondary = GL_JSGNDY.__table__ , backref = 'jslist' )

# ��Ա�������
class ZD_HYJB( settings.BaseModel ):
    __tablename__ = 'zd_hyjb'
    jbdm = Column( Integer , primary_key = True ) # ��Ա�������
    xh   = Column( Integer , default = 0 )  # ���(1-12),     ���ԽС������Խ��
    mc = Column( String(40) , nullable = False ) # ��������
    
    hylist = relation( 'GL_HYDY' , order_by = [ GL_HYDY.hydm ] , backref = backref( 'jbobj' , uselist = False ) )#��Ա�б�
    
    
    
#�������Ͷ����
class ZD_JGLX( settings.BaseModel ):
    __tablename__ = 'zd_jglx'
    jglx = Column( Integer , primary_key = True )##�������ʹ���
    mc = Column( String(40) , nullable = False ) # ��������,Ŀǰ�֣����ء�Ӫ������֧����������
    xh = Column( Integer , default = 0 )  # ��ţ���ʾ˳��
    xz = Column( String(10) , nullable = True ) #���ֻ�����֧�л��ǲ��š�����'zh':֧�У�'bm'������
    jglist=relation( 'GL_JGDY' , order_by = [ GL_JGDY.jgdm ] , backref = backref( 'jglxobj' , uselist = False ) )#�����б�
    
##��λ�����
class ZD_GWDY( settings.BaseModel ):
    __tablename__ = 'zd_gwdy'
    gwdm = Column( Integer , primary_key = True )##��λ����
    mc = Column( String(40) , nullable = False ) # ��λ����
    xh = Column( Integer , default = 0 )  # ��ţ����ԽС������Խ��
    jglx  = Column( Integer , ForeignKey( "zd_jglx.jglx" , enable = False ) , nullable = True ) # �������ͣ����ء�Ӫ������֧����������
    
    jglxobj = relation( 'ZD_JGLX' , order_by = [ ZD_JGLX.xh ] , backref = backref( 'gwlist' , order_by=[ ('ZD_GWDY.xh' ) ] ) )#��λ�б�
    hylist = relation( 'GL_HYDY' , order_by = [ GL_HYDY.hydm ] , backref = backref( 'gwobj' , uselist = False ) )#��Ա�б�
    

def ins( conn, gndm=None, gnmc=None, url=None, gnjb=None, xssx=None, sjdm=None, sfmx=None, img=None ):
    if conn.query( GL_GNDY ).get( gndm ) is None:
        gn = GL_GNDY( gndm=gndm, gnmc=gnmc, url=url, gnjb=gnjb, xssx=xssx, sjdm=sjdm, sfmx=sfmx,img = img )
        conn.add( gn )

##�û��鶨���
class ZD_YHZ( settings.BaseModel ):
    __tablename__ = 'zd_yhz'
    zdm = Column( Integer , primary_key = True )##�����
    mc = Column( String(40) , nullable = False ) # ������
    zlx = Column( String(1) , nullable = False ) #�û����������� 0������������ 1�������û���
    xh = Column( Integer , default = 0 )  # ��ţ����ԽС������Խ��
    hylst = Column( PickleType , nullable = True ) # ��Ա�����б�
    cjr = Column( String(20) , nullable = False ) #������ 
    #hylist = relation( 'GL_HYDY' , order_by = [ GL_HYDY.hydm ] , backref = backref( 'zobj' , uselist = False ) )#��Ա�б�
    #������Ա�����б�
    def get_hylst( self ):
        se = settings.DB_SESSION()
        return se.query( GL_HYDY ).filter( GL_HYDY.hydm.in_( self.hylst ) ).all()
    hyobjlst = property( get_hylst )
    
# ��Ա ���� Ȩ��
class GL_HYGNQX( settings.BaseModel ):
    __tablename__ = 'gl_hygnqx'
    
    hydm = Column( String(30) , ForeignKey( "gl_hydy.hydm" , enable = False ) , primary_key = True )  # ������Ա
    gndm = Column( String(10) , ForeignKey( "gl_gndy.gndm" , enable = False ) , primary_key = True )  # ���ܴ���
    glqx = Column( String(1)  , nullable = True, default = '0' )   # ����Ȩ��  0 ������ 1 ȫ�� 2 ָ������ 3 ����
    zdglqx_id = Column( String(500) , nullable = True ) # ָ������Ȩ�� ID
    zdglqx_mc = Column( String(500) , nullable = True ) # ָ������Ȩ�� MC
    sfbhzbm = Column( String(1)  , default = '0' )   # �Ƿ�����Ӳ���  0 ������ 1 ����

##��Ȩ�˵ǼǱ�
class GL_SQ( settings.BaseModel ):
    __tablename__ = 'gl_sq'
    
    sqdm = Column( String(10) , primary_key = True )  #��Ȩ����
    sqmc = Column( String(100),nullable = False )     #��Ȩ����
    
    glqx_id = Column( String() , nullable=True  ) #����Ȩ��-��Ա�����б�
    glqx_mc = Column( String() , nullable=True  ) #����Ȩ��-��Ա�����б�

##��Ȩ��ˮ
class LS_SQMX( settings.BaseModel ):
    __tablename__ = 'ls_sqmx'
    
    id = Column( Integer , primary_key = True ) 
    sqdm = Column( String(10) , ForeignKey( 'gl_sq.sqdm' , enable = False ), nullable=False  ) # ��Ȩ����
    sqr   = Column( String(40) , ForeignKey( 'gl_hydy.hydm' , enable = False ), nullable=False  ) # ��Ȩ��
    lx = Column( String(100) , nullable=False  ) # ��Ȩ���ͣ������޸�MCC�����MCC��ɾ��MCC�ȵ�
    sqnr = Column( String(1000) , nullable=True  ) # ��Ȩ����
    glid = Column( String(10) , nullable=True  ) # ����id
    sqsj = Column( String(20) , nullable=False ,server_default=now() ) # ��Ȩʱ��
    czry = Column( String(40) , ForeignKey( 'gl_hydy.hydm' , enable = False ), nullable=False  ) # ������Ա
    
#ϵͳ����
"""
 * @brief ϵͳ������
 * ÿ���ֶξ��嶨���ɾ�������Զ���
"""
class GL_XTCS( settings.BaseModel ):
    __tablename__ = 'gl_xtcs'
    csdm  = Column( String(10) , nullable = False, primary_key = True ) #/**< ��������, Ҫ��ȫ��Сд */
    csmc  = Column( String(40) , nullable = False ) #/**< �������� */
    csqz1 = Column( String(50) , nullable = False ) #/**< ����ȡֵ1, Ĭ�ϲ���ֵ */
    csqz2 = Column( String(50) , nullable = True ) #/**< ����ȡֵ2 */
    csqz3 = Column( String(50) , nullable = True ) #/**< ����ȡֵ3 */
    csqz4 = Column( String(50) , nullable = True ) #/**< ����ȡֵ4 */
    csqz5 = Column( String(50) , nullable = True ) #/**< ����ȡֵ5 �ڻ�����Ŀ�����ڼ�¼���ݿ⴦���� */
    csqz6 = Column( String(50) , nullable = True ) #/**< ����ȡֵ6 */
    csqz7 = Column( String(50) , nullable = True ) #/**< ����ȡֵ7 */
    csqz8 = Column( String(500), nullable = True ) #/**< ����ȡֵ8 */
    csqz9 = Column( String(500), nullable = True ) #/**< ����ȡֵ9 */
    bz    = Column( String(500), nullable = True ) #/**< ��ע */
    kfwh  = Column( String(2) , nullable = False ) #/**< �ɷ�ά����1=�ɣ�0=�� */
# ʱ�������ֵ� 
class ZD_SJZQ ( settings.BaseModel ):
    __tablename__ = 'zd_sjzq'
    zqdm    = Column( String(8)    , nullable = False  , primary_key = True ) # ʱ�����ڴ���
                                            #�� �� M200401��2004��1�£�
                                            #�� �� Q200401��2004��һ���ȣ�
                                            #���� �� B200401��2004�ϰ��꣩
                                            #�� �� Y2004��2004��ȣ�
                                       
    zqmc    = Column( String(30)   , nullable = False ) # �������� 
    zqts    = Column( Numeric(3 , 0 , asdecimal= True )   , nullable = False ) # �������� 
    zqjljts = Column( Numeric(3 , 0 , asdecimal= True )   , nullable = True ) # ���ڼ��ۼ����� 
    zqnljts = Column( Numeric(3 , 0 , asdecimal= True )   , nullable = False ) # �������ۼ����� 
    zqksrq  = Column( String( 10 ) ,  nullable = False ) # ���ڿ�ʼ���� 
    zqjsrq  = Column( String( 10 )  ,  nullable = False ) # ���ڽ������� 
    zqssnf  = Column( Numeric(4 , 0 , asdecimal= True )   , nullable = False ) # ����������� 
    zqssjd  = Column( Numeric(1 , 0 , asdecimal= True )    , nullable = True ) # �����������ȣ����������ڸ��ֶ�Ϊ�� 
    zqssyf  = Column( Numeric(2 , 0 , asdecimal= True )    , nullable = True ) # ���������·ݣ���Ӧ�꣬���꣬�����ڣ����ֶ�Ϊ�� 
    
# ��Ա�����¶ȶ�Ӧ�����ڻ�Ҫ��չ
class GL_HYJG( settings.BaseModel ):
    __tablename__ = 'gl_hyjg'
    zqdm  = Column( String(8),   nullable = False, primary_key = True )  #/**< ʱ�����ڴ��� */
    hydm  = Column( String(30), ForeignKey( "gl_hydy.hydm" , enable = False ), nullable = False, primary_key = True )  #/**< ��Ա���룬4λ��������ԱΪ��99���������� */
    jgdm  = Column( Integer, ForeignKey( "gl_jgdy.jgdm" , enable = False ) ,  nullable = False )  #/**< ��Ա���������Ļ������� */
    cxgyh  = Column( String(12), nullable = True ) #/**< ��Ӧ�����Ա�� */
    dggyh  = Column( String(12), nullable = True ) #/**< ��Ӧ�Թ���Ա�� */
    xm  = Column( String(40),   nullable = False )  #/**< ���� */
    
    hyobj = relation( 'GL_HYDY' , uselist = False ) #��Ա����
    jgobj = relation( 'GL_JGDY' , uselist = False ) #��������
