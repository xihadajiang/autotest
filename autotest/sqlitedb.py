# -*- coding: utf-8 -*-
import sqlite3 as sqlite
# 建立与数据库的连接，如果不存在，则新建
cx = sqlite.connect("autotest.db")
# 游标
cu = cx.cursor()
gl_hydy_create = """CREATE TABLE gl_hydy
(
  hydm character varying(20),
  gh character varying(20),
  xm character varying(40),
  xb character varying(1),
  jgdm integer,
  sr character varying(10),
  mm character varying(10),
  zt character varying(1),
  dlcs integer,
  jsdm character varying(4),
  kzjs character varying(100),
  profile character varying(20),
  kzpz character varying(20),
  zxsj character varying(20),
  ztgxsj character varying(20),
  dwdh character varying(20),
  dwcz character varying(20),
  sj character varying(20),
  xlt character varying(20),
  glqx character varying(1),
  zdglqx_id character varying(100),
  zdglqx_mc character varying(100),
  bz character varying(200),
  onlinestate character varying(1),
  sfcykp character varying(1),
  sskpjg_id character varying(1000),
  sskpjg_mc character varying(1000),
  jbdm integer,
  gwdm integer,
  sfbhzbm character varying(1),
  fj character varying(500),
  cxgyh character varying(12),
  dggyh character varying(12),
  CONSTRAINT gl_hydy_idx UNIQUE (hydm)
)"""
#cu.execute(gl_hydy_create)
#cu.commit()
ins = """INSERT INTO gl_hydy(hydm, gh, xm, xb, jgdm, sr, mm, zt, dlcs, jsdm, kzjs, profile, kzpz, zxsj, ztgxsj, dwdh, dwcz, sj, xlt, glqx, zdglqx_id, zdglqx_mc, bz, onlinestate, sfcykp, sskpjg_id, sskpjg_mc, jbdm, gwdm, sfbhzbm,fj, cxgyh, dggyh) VALUES ("admin","999999","admin","1",98,"2008-08-08","","0",547,"9999","","1","","766893","20141124010954","","","","","1","","","","1","0","","","","","0","","","");
"""
#cu.execute(ins)
#cx.commit()

def select(sql_select):
    """
    测试是否存在相同的记录
    """
    cu.execute(sql_select)
    res = cu.fetchall()
    print res
    for row in res:
        i=1;
        print "数据表第%s" %i,"条记录是：", row,
select("select * from gl_hydy")