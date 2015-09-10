# coding: gbk
# 字典_数据周期
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

# 用户表
class GL_HYDY( settings.BaseModel ):
    __tablename__ = 'gl_hydy'
    hydm = Column( String(30) , primary_key = True )  # gl_hydy.hydm，所属人员
    gh   = Column( String(30) , nullable = False , unique = True ) # 工号.可登录,如果有多个可选择,则列出由用户选择后输入密码
    xm   = Column( String(40) , nullable = False ) # 姓名
    xb   = Column( String(1)  , nullable = False , default = '1' ) # 性别.2:女;1:男
    jgdm  = Column( Integer , ForeignKey( "gl_jgdy.jgdm" , enable = False ) , nullable = True ) # 机构代码
    sr   = Column( String(10) , nullable = True ) # 生日
    mm   = Column( String(10)  , nullable = False , default='1'*8 ) # 密码，强制8位，明文保存
    zt   = Column( String(1)  , nullable = False , default= '0' ) # 状态.0:启用;1:禁用;2:改密后才能登录
    dlcs = Column( Integer    , default = 0 )      # 登陆次数
    jsdm = Column( String(4) , ForeignKey( 'gl_jsdy.jsdm' , enable = False ) , nullable = True )  # 岗位代码
    kzjs = Column( String(100) , nullable = True ) # 扩展角色：jsdm,
    
    profile = Column( String(20) , default = '1' )  # 布局配置，默认1，共有1-8个模板
    
    kzpz    = Column( PickleType , nullable = True )      # 扩展配置，各模块配置信息，字典存放
                                                          # shortcut：快捷菜单，gndm的列表 []
                                                          # winexe:   windows应用快捷方式，列表[ ( 名称 , path ) ]
                                                          # urls:     个人网址 列表[ ( 名称, url , user , pass ) ]
    zxsj    = Column( String(20) , default = '0' )             # 在线总时间，秒单位
    ztgxsj  = Column( String(20) , default = now )             # 状态更新时间，IE每隔30秒刷新该字段
                                                          #      若：  该字段          当前时间            状态          在线时间统计
                                                          #                0              0-120          表示在线            +
                                                          #                0            121-300          表示暂离            +
                                                          #                0            301-?            表示离线            
    # 联系方式
    dwdh    = Column( String(20) , nullable = True ) # 单位电话
    dwcz    = Column( String(20) , nullable = True ) # 单位传真
    sj      = Column( String(20) , nullable = True ) # 手机
    xlt     = Column( String(20) , nullable = True ) # 小灵通
    
    glqx    = Column( String(1)  , default = '0' )   # 管理权限  0 本部门 1 全体 2 指定部门 3:个人
    sfcykp  = Column( String(1)  , default = '1' )   # 是否参与考评  1:参与  0：不参与（不被考评，也不能打分）
    zdglqx_id = Column( String(500) , nullable = True ) # 指定管理权限 ID
    zdglqx_mc = Column( String(500) , nullable = True ) # 指定管理权限 MC
    sskpjg_id = Column( String(1000) , nullable = True ) # 所属考评机构 ID
    sskpjg_mc = Column( String(1000) , nullable = True ) # 所属考评机构 MC
    jbdm  = Column( Integer , ForeignKey( "zd_hyjb.jbdm" , enable = False ) , nullable = True ) # 行员级别
    gwdm  = Column( Integer , ForeignKey( "zd_gwdy.gwdm" , enable = False ) , nullable = True ) # 行员岗位
    #zdm  = Column( Integer , ForeignKey( "zd_yhz.zdm" , enable = False ) , nullable = True ) # 行员组
    sfbhzbm = Column( String(1)  , default = '0' )   # 是否包含子部门  0 不包含 1 包含
    bz      = Column( String(200) , nullable = True )  # 备注
    fj   = Column( String(500) , nullable = True ) # 照片
    onlinestate = Column( String(1)  , nullable = False, default='0' ) # 状态.0:离线;1:在线;2:暂离 默认离线
    singlesignon = Column( String(1)  , nullable = False, default='1' ) # 单点登录模式
    cxgyh = Column(  String(12) , nullable = True )# 储蓄柜员号 
    dggyh = Column(  String(12) , nullable = True ) #对公柜员号 
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
        # 根据本人的管理权限，过滤hylist
        if self.glqx == '0':
            # 本部门
            jglist = [self.jgdm ] + [ x.jgdm for x in self.jgobj.get_all_children() ]
        elif self.glqx == '2':
            # 其他部门
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
    def get_jglxlist( self , se ):##根据本人的管理权限，得出本人可以管理的机构类型
        
        q = se.query( ZD_JGLX ).filter(ZD_JGLX.jglx>0)
        
        if self.glqx=='2':#指定部门
            zdjglist = filter(None,self.zdglqx_id.split(','))
            jglxlb=[]
            for obj in se.query( GL_JGDY ).filter( GL_JGDY.jgdm.in_(zdjglist)):
                jglxlb.append( obj.jglx )
            q  =q.filter( ZD_JGLX.jglx.in_(jglxlb))
        if self.glqx=='0':##本部门
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
# 机构定义
class GL_JGDY( settings.BaseModel ):
    __tablename__ = 'gl_jgdy'
    jgdm = Column( Integer , primary_key = True ) # 
    xh   = Column( Integer , default = 0 ) # 部门排序号
    ywjgdm = Column( String(20) , nullable = True ) # 业务机构代码
    jgmc = Column( String(40) , nullable = False ) # 机构名称
    zt   = Column( String(1)  , nullable = False ) # 状态，0启用，1禁用 默认0
    dh   = Column( String(20) , nullable = True  ) # 电话
    cz   = Column( String(20) , nullable = True  ) # 传真
    
    sjbm = Column( Integer , ForeignKey( 'gl_jgdy.jgdm' , enable = False ) , nullable = True )  # 上级部门
    bmzg = Column( String(100) , nullable = True )  # 部门主管
    sjzg = Column( String(100) , nullable = True )  # 上级主管
    sjfg = Column( String(100) , nullable = True )  # 上级分管
    jglx  = Column( Integer , ForeignKey( "zd_jglx.jglx" , enable = False ) , nullable = True ) # 机构类型：机关、营销部、支行三种类型 
    
    bmzn = Column( String(200) , nullable = True ) # 部门职能
    gggy = Column( String(40) , nullable = True ) #公共柜员
    
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
#            root 为根节点, 为空表示全部
#        """
        out = []
#        if root == '':
#            r = None
#            children = se.query( GL_JGDY ).filter( and_( GL_JGDY.sjbm == None , GL_JGDY.zt == '0' ) ).all()
#        else:
#            r = se.query( GL_JGDY ).get( root )
#            if r is None:
#                raise RuntimeError( '找不到指定的机构' )
#            out.append( ( r.jgdm , r.jgmc ) )
#            children = r.get_children()
        indexdic = GL_JGDY.filter(jglist)
        
        def build_tree( tobj , prefix , parent_next , self_next , first = True ):
            n_prefix = prefix + ( ( '　' if first == False else '' ) if parent_next == False else '│' )
            if indexdic[tobj.jgdm]['access']==True:
                jgdm = tobj.jgdm
                jgmc =tobj.jgmc

            else:
                jgdm=-1
                jgmc=''
            out.append( ( jgdm , n_prefix + ( '└' if self_next == False else '├' ) + jgmc ) )
            
            ch = indexdic[tobj.jgdm]['children']  #tobj['children'].get_children()  
            ma = len( ch )
            for i in range( ma ):
                build_tree( ch[ i ]['obj'] , n_prefix , self_next , i < ma-1 , first = False )
        
        children = indexdic['ROOT']['children']
        maxc = len( children )
        for i in range( maxc ):
            build_tree( children[ i ]['obj'], '' , False , i < maxc-1 )
            
        return out
    
    #获取支行部门树
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
#        ##针对可访问的叶子构造子树
#        def build_children( jgobj ):
#            tobj = indexdic[ jgobj.jgdm ]
#            tobj['access'] = True
#            for c in jgobj.children:
#                if c.jgdm in indexdic.keys():
#                    indexdic[ c.jgdm]['access'] = True # 重置为可访问
#                    continue 
#                cobj={'name':c.jgdm , 'children':[],'xssx':c.xh , 'obj':c,'access':False}
#                indexdic[c.jgdm] = cobj
#                tobj['children'].append( cobj )
#                build_children( c )
#
#        for x in jglist:
#            build_children(x)
        
#        ##构建树---------------------
#        def build_tree( tobj , prefix , parent_next , self_next , first = True ):
#            n_prefix = prefix + ( ( '　' if first == False else '' ) if parent_next == False else '│' )
#            out.append( ( tobj.jgdm , n_prefix + ( '└' if self_next == False else '├' ) + tobj.jgmc ) )
#            ch = tobj.get_children()
#            ma = len( ch )
#            for i in range( ma ):
#                build_tree( ch[ i ] , n_prefix , self_next , i < ma-1 , first = False )
        
        ##对构建的功能树进行排序
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
            获取主管
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
    gndm = Column( String(10)  , nullable = False , primary_key = True ) # 功能代码
    gnmc = Column( String(80)  , nullable = False ) # 功能名称
    url  = Column( String(255) , nullable = True ) # 功能对应url.web系统中相对地址
    gnjb = Column( Numeric( 2 , 0 , asdecimal = False ), nullable = False ) # 功能级别
    xssx = Column( Integer , nullable = False ) # 显示顺序
    sjdm = Column( String(10)  , ForeignKey('gl_gndy.gndm' , enable = False ), nullable = False ) # 上级代码.虚拟根对象为root
    sfmx = Column( String(1)   , nullable = False ) # 是否明细.0:否;1=是
    bz   = Column( String(255) , nullable = True )  # 备注.对于报表的功能链接,此字段的内容将被解释为报表的简介
    img  = Column( String(255) , nullable = True )  # 菜单图标
    sfwh = Column( String(1)   , nullable = True ) # 可否维护 0:否;1:是 空的话也是不可维护
    
    children = relation('GL_GNDY', backref = backref( 'parent' , remote_side=[gndm] ) )
    
    @staticmethod
    def buildmenu( gnlist , linefmt , sess , extra = None , caname = 'gn' ):
        """ 根据指定的功能列表，递归实现树。
            并返回树的索引
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
                    tobj = copy.deepcopy( ca.get( gndm ) )  # 首先从缓存中获取
                else:
                    tobj = ca[ gndm ]
            except KeyError:
                gnobj = sess.query( GL_GNDY ).get( gndm )
                if not gnobj:
                    raise RuntimeError( '功能[%s]无法找到' % gndm )
                    
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
        
        #对构建的功能树进行排序
        leaves = [] # 保存叶子，不再使用sfmx字段。
        for k , value in indexdic.items():
            if len( value['children'] ) == 0:
                leaves.append( k )
            else:
                value[ 'children' ].sort( key = lambda x:x['xssx'] )
                
        # 清理叶子节点，他们不需要在索引中体现（索引中的父节点已经有引用）
        for k in leaves:
            indexdic.pop( k )
        return indexdic

    @staticmethod
    def gn_tree( se , root = '' ):
        """
            root 为根节点, 为空表示全部
        """
        out = []
        if root == '':
            r = None
            children = se.query( GL_JSDY ).filter( GL_JSDY.sjdm == None ).all()
        else:
            r = se.query( GL_JSDY ).get( root )
            if r is None:
                raise RuntimeError( '找不到指定的功能' )
            out.append( ( r.jsdm , r.jsmc ) )
            children = r.get_children()
        
        def build_tree( tobj , prefix , parent_next , self_next , first = True ):
            n_prefix = prefix + ( ( '　' if first == False else '' ) if parent_next == False else '│' )
            out.append( ( tobj.jsdm , n_prefix + ( '└' if self_next == False else '├' ) + tobj.jsmc ) )
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

        ##对构建的功能树进行排序
        for k,v in indexdic.items():
            if len(v['children'])!=0:
                v['children'].sort(key = lambda x :x['xssx'])
        return indexdic

    @staticmethod
    def get_gn_tree( gnlst ):
#        """
#            返回功能树
#        """
        out = []

        indexdic = GL_GNDY.filter( gnlst )
        
        def build_tree( tobj , prefix , parent_next , self_next , first = True ):
            n_prefix = prefix + ( ( '　' if first == False else '' ) if parent_next == False else '│' )
            gndm = tobj.gndm
            gnmc =tobj.gnmc
            out.append( ( gndm , n_prefix + ( '└' if self_next == False else '├' ) + gnmc ) )
            
            ch = indexdic[tobj.gndm]['children']  #tobj['children'].get_children()  
            ma = len( ch )
            for i in range( ma ):
                build_tree( ch[ i ]['obj'] , n_prefix , self_next , i < ma-1 , first = False )
        
        children = indexdic['ROOT']['children']
        maxc = len( children )
        for i in range( maxc ):
            build_tree( children[ i ]['obj'], '' , False , i < maxc-1 )
            
        return out
    #返回功能路径
    def get_gn_path( self , sep = '/' ):
        if self.parent:
            return self.parent.gnpath + sep + self.gnmc
        else:
            return self.gnmc
            
    gnpath = property( get_gn_path )




class GL_JSDY( settings.BaseModel ):
    # 管理_角色定义
    __tablename__ = 'gl_jsdy'
    jsdm = Column( String(4) , primary_key = True ) # 角色代码
    xh   = Column( Integer , default = 0 )  # 序号
    
    jsmc = Column( String(40) , nullable = False ) # 角色名称
    
    def get_hylist( self ):
        se = settings.DB_SESSION()
        return se.query( GL_HYDY ).filter( and_( GL_HYDY.zt == '0' , or_( GL_HYDY.jsdm == self.jsdm , GL_HYDY.kzjs.like( '%%%s%%,' % self.jsdm ) ) ) ).all()
        
    hylist = property( get_hylist )
    

class GL_JSGNDY( settings.BaseModel ):
    # 管理_角色功能定义
    __tablename__ = 'gl_jsgndy'
    gndm = Column( String(10) , ForeignKey( "gl_gndy.gndm" , enable = False ) , primary_key = True ) # 功能代码
    jsdm = Column( String(4) , ForeignKey( "gl_jsdy.jsdm" , enable = False ) , primary_key = True ) # 角色代码
    qxxx = Column( PickleType , nullable = True ) # 权限信息

GL_JSDY.gnlist = relation( 'GL_GNDY' , secondary = GL_JSGNDY.__table__ , backref = 'jslist' )

# 行员级别定义表
class ZD_HYJB( settings.BaseModel ):
    __tablename__ = 'zd_hyjb'
    jbdm = Column( Integer , primary_key = True ) # 行员级别代码
    xh   = Column( Integer , default = 0 )  # 序号(1-12),     序号越小，级别越高
    mc = Column( String(40) , nullable = False ) # 级别名称
    
    hylist = relation( 'GL_HYDY' , order_by = [ GL_HYDY.hydm ] , backref = backref( 'jbobj' , uselist = False ) )#行员列表
    
    
    
#部门类型定义表
class ZD_JGLX( settings.BaseModel ):
    __tablename__ = 'zd_jglx'
    jglx = Column( Integer , primary_key = True )##机构类型代码
    mc = Column( String(40) , nullable = False ) # 机构类型,目前分：机关、营销部、支行三种类型
    xh = Column( Integer , default = 0 )  # 序号，显示顺序
    xz = Column( String(10) , nullable = True ) #区分机构是支行还是部门。。。'zh':支行，'bm'：部门
    jglist=relation( 'GL_JGDY' , order_by = [ GL_JGDY.jgdm ] , backref = backref( 'jglxobj' , uselist = False ) )#机构列表
    
##岗位定义表
class ZD_GWDY( settings.BaseModel ):
    __tablename__ = 'zd_gwdy'
    gwdm = Column( Integer , primary_key = True )##岗位代码
    mc = Column( String(40) , nullable = False ) # 岗位名称
    xh = Column( Integer , default = 0 )  # 序号，序号越小，级别越高
    jglx  = Column( Integer , ForeignKey( "zd_jglx.jglx" , enable = False ) , nullable = True ) # 机构类型：机关、营销部、支行三种类型
    
    jglxobj = relation( 'ZD_JGLX' , order_by = [ ZD_JGLX.xh ] , backref = backref( 'gwlist' , order_by=[ ('ZD_GWDY.xh' ) ] ) )#岗位列表
    hylist = relation( 'GL_HYDY' , order_by = [ GL_HYDY.hydm ] , backref = backref( 'gwobj' , uselist = False ) )#行员列表
    

def ins( conn, gndm=None, gnmc=None, url=None, gnjb=None, xssx=None, sjdm=None, sfmx=None, img=None ):
    if conn.query( GL_GNDY ).get( gndm ) is None:
        gn = GL_GNDY( gndm=gndm, gnmc=gnmc, url=url, gnjb=gnjb, xssx=xssx, sjdm=sjdm, sfmx=sfmx,img = img )
        conn.add( gn )

##用户组定义表
class ZD_YHZ( settings.BaseModel ):
    __tablename__ = 'zd_yhz'
    zdm = Column( Integer , primary_key = True )##组代码
    mc = Column( String(40) , nullable = False ) # 组名称
    zlx = Column( String(1) , nullable = False ) #用户定义组类型 0：公共工作组 1：个人用户组
    xh = Column( Integer , default = 0 )  # 序号，序号越小，级别越高
    hylst = Column( PickleType , nullable = True ) # 行员代码列表
    cjr = Column( String(20) , nullable = False ) #创建人 
    #hylist = relation( 'GL_HYDY' , order_by = [ GL_HYDY.hydm ] , backref = backref( 'zobj' , uselist = False ) )#行员列表
    #返回行员对象列表
    def get_hylst( self ):
        se = settings.DB_SESSION()
        return se.query( GL_HYDY ).filter( GL_HYDY.hydm.in_( self.hylst ) ).all()
    hyobjlst = property( get_hylst )
    
# 行员 功能 权限
class GL_HYGNQX( settings.BaseModel ):
    __tablename__ = 'gl_hygnqx'
    
    hydm = Column( String(30) , ForeignKey( "gl_hydy.hydm" , enable = False ) , primary_key = True )  # 所属人员
    gndm = Column( String(10) , ForeignKey( "gl_gndy.gndm" , enable = False ) , primary_key = True )  # 功能代码
    glqx = Column( String(1)  , nullable = True, default = '0' )   # 管理权限  0 本部门 1 全体 2 指定部门 3 个人
    zdglqx_id = Column( String(500) , nullable = True ) # 指定管理权限 ID
    zdglqx_mc = Column( String(500) , nullable = True ) # 指定管理权限 MC
    sfbhzbm = Column( String(1)  , default = '0' )   # 是否包含子部门  0 不包含 1 包含

##授权人登记表
class GL_SQ( settings.BaseModel ):
    __tablename__ = 'gl_sq'
    
    sqdm = Column( String(10) , primary_key = True )  #授权代码
    sqmc = Column( String(100),nullable = False )     #授权名称
    
    glqx_id = Column( String() , nullable=True  ) #管理权限-行员代码列表
    glqx_mc = Column( String() , nullable=True  ) #管理权限-行员姓名列表

##授权流水
class LS_SQMX( settings.BaseModel ):
    __tablename__ = 'ls_sqmx'
    
    id = Column( Integer , primary_key = True ) 
    sqdm = Column( String(10) , ForeignKey( 'gl_sq.sqdm' , enable = False ), nullable=False  ) # 授权代码
    sqr   = Column( String(40) , ForeignKey( 'gl_hydy.hydm' , enable = False ), nullable=False  ) # 授权人
    lx = Column( String(100) , nullable=False  ) # 授权类型，例如修改MCC、添加MCC、删除MCC等等
    sqnr = Column( String(1000) , nullable=True  ) # 授权内容
    glid = Column( String(10) , nullable=True  ) # 关联id
    sqsj = Column( String(20) , nullable=False ,server_default=now() ) # 授权时间
    czry = Column( String(40) , ForeignKey( 'gl_hydy.hydm' , enable = False ), nullable=False  ) # 操作人员
    
#系统参数
"""
 * @brief 系统参数表
 * 每个字段具体定义由具体参数自定义
"""
class GL_XTCS( settings.BaseModel ):
    __tablename__ = 'gl_xtcs'
    csdm  = Column( String(10) , nullable = False, primary_key = True ) #/**< 参数代码, 要求全部小写 */
    csmc  = Column( String(40) , nullable = False ) #/**< 参数名称 */
    csqz1 = Column( String(50) , nullable = False ) #/**< 参数取值1, 默认参数值 */
    csqz2 = Column( String(50) , nullable = True ) #/**< 参数取值2 */
    csqz3 = Column( String(50) , nullable = True ) #/**< 参数取值3 */
    csqz4 = Column( String(50) , nullable = True ) #/**< 参数取值4 */
    csqz5 = Column( String(50) , nullable = True ) #/**< 参数取值5 在汇总项目中用于记录数据库处理步数 */
    csqz6 = Column( String(50) , nullable = True ) #/**< 参数取值6 */
    csqz7 = Column( String(50) , nullable = True ) #/**< 参数取值7 */
    csqz8 = Column( String(500), nullable = True ) #/**< 参数取值8 */
    csqz9 = Column( String(500), nullable = True ) #/**< 参数取值9 */
    bz    = Column( String(500), nullable = True ) #/**< 备注 */
    kfwh  = Column( String(2) , nullable = False ) #/**< 可否维护，1=可，0=否 */
# 时间周期字典 
class ZD_SJZQ ( settings.BaseModel ):
    __tablename__ = 'zd_sjzq'
    zqdm    = Column( String(8)    , nullable = False  , primary_key = True ) # 时间周期代码
                                            #月 － M200401（2004年1月）
                                            #季 － Q200401（2004年一季度）
                                            #半年 － B200401（2004上半年）
                                            #年 － Y2004（2004年度）
                                       
    zqmc    = Column( String(30)   , nullable = False ) # 周期名称 
    zqts    = Column( Numeric(3 , 0 , asdecimal= True )   , nullable = False ) # 周期天数 
    zqjljts = Column( Numeric(3 , 0 , asdecimal= True )   , nullable = True ) # 周期季累计天数 
    zqnljts = Column( Numeric(3 , 0 , asdecimal= True )   , nullable = False ) # 周期年累计天数 
    zqksrq  = Column( String( 10 ) ,  nullable = False ) # 周期开始日期 
    zqjsrq  = Column( String( 10 )  ,  nullable = False ) # 周期结束日期 
    zqssnf  = Column( Numeric(4 , 0 , asdecimal= True )   , nullable = False ) # 周期所属年份 
    zqssjd  = Column( Numeric(1 , 0 , asdecimal= True )    , nullable = True ) # 周期所属季度，对于年周期该字段为空 
    zqssyf  = Column( Numeric(2 , 0 , asdecimal= True )    , nullable = True ) # 周期所属月份，对应年，半年，季周期，该字段为空 
    
# 行员机构月度对应表，后期还要扩展
class GL_HYJG( settings.BaseModel ):
    __tablename__ = 'gl_hyjg'
    zqdm  = Column( String(8),   nullable = False, primary_key = True )  #/**< 时间周期代码 */
    hydm  = Column( String(30), ForeignKey( "gl_hydy.hydm" , enable = False ), nullable = False, primary_key = True )  #/**< 行员代码，4位，公共行员为‘99’＋机构码 */
    jgdm  = Column( Integer, ForeignKey( "gl_jgdy.jgdm" , enable = False ) ,  nullable = False )  #/**< 行员所属机构的机构代码 */
    cxgyh  = Column( String(12), nullable = True ) #/**< 对应储蓄柜员号 */
    dggyh  = Column( String(12), nullable = True ) #/**< 对应对公柜员号 */
    xm  = Column( String(40),   nullable = False )  #/**< 姓名 */
    
    hyobj = relation( 'GL_HYDY' , uselist = False ) #行员对象
    jgobj = relation( 'GL_JGDY' , uselist = False ) #机构对象
