# -*- coding: utf-8 -*-
import sqlite3 as sqlite
# ���������ݿ�����ӣ���������ڣ����½�
cx = sqlite.connect("test1.db")
# �α�
cu = cx.cursor()
def create(sql):
    """
    �����ݿ������һ��table
    """
    cu.execute(sql)
    #cu.commit()
def insert(sql):
    """
    �����ݿ������һ��table
    """
    cu.execute(sql)
    cu.commit()
def select(sql_select):
    """
    �����Ƿ������ͬ�ļ�¼
    """
    cu.execute(sql_select)
    res = cu.fetchall()
    print res
    for row in res:
        i=1;
        print "���ݱ��%s" %i,"����¼�ǣ�", row,
sql_select="SELECT * FROM tbl_test;"
sql_create ="""create table tbl_test( id integer primary key)"""
#create(sql_create)
select(sql_select)