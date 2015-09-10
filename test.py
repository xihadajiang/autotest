#coding:gbk
def getcontent(filename,rq,lsh):
    BUF_SIZE = 1024
    bigfile = open(filename,'r') 
    tmp_lines = bigfile.readlines(BUF_SIZE) 
    content = []
    flag = 0
    tmp_content = []
    tmp_flag = 0
    while tmp_lines: 
        i = 0
        for line in tmp_lines:
            #print line
            if flag == 0:
                if "--------------开始分级日志" in line:
                    tmp_flag = 1
                    tmp_content = []
                elif '当前流水号=[5511' in line:
                    flag = 1
                    content = tmp_content
                tmp_content.append(line)
            else:
                if "--------------提交缓冲日志" in line:
                    content.append(line)
                    return content
                else:
                    content.append(line)
            i = i + 1
        tmp_lines = bigfile.readlines(BUF_SIZE)
    bigfile.close()
    return content
lines = getcontent(r'D:\Django\data\log\20140401\sys_smqt_20140401.log','20140401','79722')
for i in lines:
    print i