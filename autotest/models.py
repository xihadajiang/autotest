# coding: gbk
# 字典_数据周期
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