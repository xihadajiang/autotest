#coding:utf-8
from utils import *
import datetime
from read_last_file import *
# -*- coding: utf-8 -*-
import sqlite3 as sqlite
# 建立与数据库的连接，如果不存在，则新建
cx = sqlite.connect("autotest.db")

def fun(req):
    xyxx = '9999999999'
    now = '2014066'
    return render_to_response( "index.html" , current_date=now,xyxx=xyxx)

def oatest(req):
    request = ''
    response = ''
    return render_to_response( "oatest.html" , request=request,response=response)

def oatest_sub(req):
    request = req.get('POST').get('req')
    #request = '9999999999'
    ywlx = req.get('POST').get('ywlx')
    response = '2014066'
    return render_to_response( "oatest.html" , request=request,response=response)
def zx_index(req):
    request = ""
    #request = '9999999999'
    #ywlx = req.get('POST').get('ywlx')
    response = '2014066'
    return render_to_response( "zx_index.html" , request=request,response=response)

def zx_index_submit(request):
    #name = request.GET.get( 'name' , '' )
    now = datetime.datetime.today().strftime('%Y%m%d')
    try:
        user = request.get('POST').get('username','')
        userpassword = request.get('POST').get('userpassword','')
    except:
        return zx_index(request)
    request['session'] = {}
    request.get('session')[ 'username'] = user
    #return HttpResponseRedirect( '/zx_main/' )
    return zx_main(request)

def zx_main(req):
    request = ""
    host = req.get('Host')
    port = req.get('Port')
    response = '2014066'
    return render_to_response( "zx_main.html" , host = host,port=port,request=request,response=response)
    #return render_to_cookie_response( "zx_main.html" ,set_cookie(req.get('session')), request=request,response=response)

def auto_refresh(req):
    request = ""
    #request = '9999999999'
    #ywlx = req.get('POST').get('ywlx')
    response = '2014066'
    today = datetime.datetime.today()
    now = today.strftime('%Y-%m-%d %H:%M:%S')
    #f = open("network-server")
    #result = f.read()
    #f.close()
    content = get_last_n_lines("network-server",30)
    result = '<br>'.join(content)#.replace('\n','<br>')
    return render_to_response( "auto_refresh.html" , result=result,now=now)

def cpdm_list(req):
    request = ""
    lpath =  'F:/Django/pyhttp/autotest/data'
    host = req.get('Host')
    port = req.get('Port')
    result=[]
    for path, dir, files in os.walk(lpath ):
        if path.split(os.sep)[-1] == 'mibdata':
            for pt in dir:
                line = []
                line.append( pt.decode('gbk') )
                line.append(path.strip(lpath).decode('gbk') )
                line.append('12/12')
                result.append(line)
    return render_to_response( "cpdm_list.html" , host = host,port=port,result=result)
def csal_list(req):
    request = ""
    lpath =  'F:/Django/pyhttp/autotest/data'
    response = '2014066'
    host = req.get('Host')
    port = req.get('Port')
    cpdm = req.get('GET').get('cpdm')
    result=[]
    for path, dir, files in os.walk(lpath ):
        if path.split(os.sep)[-1] == cpdm:
            for pt in dir:
                line = []
                line.append( pt.decode('gbk') )
                line.append(path.strip(lpath).decode('gbk') )
                line.append('12/12')
                result.append(line)
    #result = [['签约验证'.decode('gbk'),'6.1','12/12'],['网上支付'.decode('gbk'),'6.1','12/12']]
    #result = [['签约验证'.decode('gbk'),'6.1','12/12']]
    return render_to_response( "csal_list.html" ,  host = host,port=port,result=result)
def test_list(req):
    lpath =  'F:/Django/pyhttp/autotest/data'
    host = req.get('Host')
    port = req.get('Port')
    jymc = req.get('GET').get('jymc')
    result=[]
    for path, dir, files in os.walk(lpath ):
        if path.split(os.sep)[-1] == jymc:
            for file in files:
                line = []
                line.append( file.decode('gbk') )
                line.append(path.strip(lpath).decode('gbk') )
                line.append('12/12')
                result.append(line)
    #result = [['签约验证'.decode('gbk'),'6.1','12/12'],['网上支付'.decode('gbk'),'6.1','12/12']]
    #result = [['签约验证'.decode('gbk'),'6.1','12/12']]
    return render_to_response( "test_list.html" , host = host,port=port,result=result)
def ltcs(req):
    lpath =  'F:/Django/pyhttp/autotest/data'
    host = req.get('Host')
    port = req.get('Port')
    almc = req.get('GET').get('almc')
    alpath = req.get('GET').get('alpath')
    print '%s%s/%s'%(lpath,alpath,almc)
    f = open('%s%s/%s'%(lpath,alpath,almc),'r')
    request = f.read().decode('gbk')
    f.close()
    response = ""
    #result = [['签约验证'.decode('gbk'),'6.1','12/12'],['网上支付'.decode('gbk'),'6.1','12/12']]
    #result = [['签约验证'.decode('gbk'),'6.1','12/12']]
    return render_to_response( "ltcs.html" , host = host,port=port,request=request,response=response)

def gaps_index_log(req):
    current_date = "20150606"
    return render_to_response( "gaps_log_index.html" , current_date = current_date)

def cygj_jzzh(req):
    current_date = "20150606"
    return render_to_response( "cygj_jzzh.html" , current_date = current_date)
