#coding:utf-8
def getformfile(filename):
    txt_content_head = """HTTP/1.0 200 OK
Content-Type:text/html
Set-Cookie: JSESSIONID=1442A671BEEDA147A2756B7E083D3B7E; Path=/zx_index 

"""
    try:
        f = open(filename,'r')
        txt_content = txt_content_head + f.read()
        f.close()
        return  txt_content
    except:
        print '%s不存在'%filename
        return ''

def getimage(filename):
    pic_content_head = """HTTP/1.0 200 OK
Content-Type:image/jpg
Set-Cookie: JSESSIONID=1442A671BEEDA147A2756B7E083D3B7E; Path=/zx_index 

"""
    try:
        f = open(filename,'rb')
        pic_content = pic_content_head + f.read()
        f.close()
        return pic_content
    except:
        print '%s不存在'%filename
        return ''

def datatoreq(datas):
    jyzd = {}
    import urllib
    datas = urllib.unquote(datas)
    req = datas.split('\r\n')
    for line in req:
        if 'Host:' in line:
            add_list = line.split(":")
            #print add_list,'add_list'
            if len(add_list) >= 2:
                host = add_list[1]
                port = add_list[2]
            else:
                host = add_list[1]
                port = '80'
            jyzd['Host'] = host.strip()
            jyzd['Port'] = port.strip()
        elif 'GET' in line or 'POST' in line:
            method , url , vsion = line.split()
            jyzd['method'] = method.strip()
            jyzd['url'] = url.strip()
            jyzd['vsion'] = vsion.strip()
        elif ': ' in line:
            k,v = line.split(': ')
            jyzd[k] = v.strip()
    url_dict = {}
    if jyzd.get('method') == 'GET':
        url_a = jyzd.get('url')
        if '?'in url_a and '&' in url_a:
            jyzd['url'] ,url_tmp = url_a.split('?')
            url = url_tmp.split('&')
            for i in url:
                req_list = i.split('=')
                url_dict[req_list[0]] ='='.join(req_list[1:]).strip()
    else:
    #if len(req[-1])>2:
        url = req[-1].split('&')
        for i in url:
            req_list = i.split('=')
            url_dict[req_list[0]] ='='.join(req_list[1:]).strip()
    jyzd[jyzd['method']] = url_dict
    #url = data.split(' ')[-1]
    print datas
    return jyzd
def set_cookie(dic):
    s = """Date: Mon, 24 Oct 2015 06:54:41 GMT
Server: IBM_HTTP_Server
Cache-Control: no-cache
Content-Length: 19885
Connection: close"""
    for k,v in dic.items():
        s = s + "Set-Cookie: %s=%s; Path=/zx_index; Domain=127.0.0.1:8080; HttpOnly\n"%(k,v)
    return s
def url2jyzd(url,jyzd):
    req = url.split('&')
    for line in req:
        if 'PORT:' in line:
            add_list = line.split("=")
            #print add_list,'add_list'
            if len(add_list) >= 2:
                host = add_list[1]
                port = add_list[2]
            else:
                host = add_list[1]
                port = '80'
            jyzd['Host'] = host.strip()
            jyzd['Port'] = port.strip()
        elif '=' in line:
            k,v = line.split('=')
            jyzd[k] = v.strip()
    return jyzd
def render_to_response( context,  **kwargs):
    txt_content_head = """HTTP/1.0 200 OK
Content-Type:text/html
Set-Cookie: JSESSIONID=1442A671BEEDA147A2756B7E083D3B7E; Path=/zx_index 

"""
    from mako.template import Template
    f = open('templates/%s'%context,'r')
    content = f.read()
    f.close()
    mytemplate = Template(content)
    res =  mytemplate.render( **kwargs)
    return txt_content_head + res

def render_to_cookie_response( context,cookie ,**kwargs):
    txt_content_head = """HTTP/1.0 200 OK
Server: Apache-Coyote/1.1  
Set-Cookie: JSESSIONID=1442A671BEEDA147A2756B7E083D3B7E; Path=/zx_index 
Content-Type:text/html
"""
    from mako.template import Template
    f = open('templates/%s'%context,'r')
    content = f.read()
    f.close()
    mytemplate = Template(content)
    res =  mytemplate.render( **kwargs)
    content = txt_content_head + res
    return content

def HttpResponseRedirect( context,  **kwargs):
    from mako.template import Template
    f = open('templates/%s'%context,'r')
    content = f.read()
    f.close()
    mytemplate = Template(content)
    res =  mytemplate.render( **kwargs)
    return res
