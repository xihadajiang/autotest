# -*- coding: utf-8 -*-
import sqlite3 as sqlite
# 建立与数据库的连接，如果不存在，则新建
cx = sqlite.connect("test1.db")
# 游标
cu = cx.cursor()
def create(sql):
    """
    在数据库中添加一个table
    """
    cu.execute(sql)
    #cu.commit()
def insert(sql):
    """
    在数据库中添加一个table
    """
    cu.execute(sql)
    cu.commit()
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
sql_select="SELECT * FROM tbl_test;"
sql_create ="""create table tbl_test( id integer primary key)"""
#create(sql_create)
select(sql_select)