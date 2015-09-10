#coding:utf-8
from views import *
url = {
'/test':'fun',
'/':'fun',
'/oatest':'oatest',
'/oatest_sub':'oatest_sub',
'/zx_index':'zx_index',
'/zx_index_submit':'zx_index_submit',
'/zx_main':'zx_main',
'/test_list':'test_list',
'/csal_list':'csal_list',
'/cpdm_list':'cpdm_list',
'/cygj_jzzh':'cygj_jzzh',
'/test_coolie':'test_cookie',
'/ltcs':'ltcs',
'/gaps_index_log':'gaps_index_log',
'/auto_refresh':'auto_refresh',
'/favicon.ico':'fun'

}
str2 = '3*6 + 4*8'
req = '0000000000'
str2 = url.get('/test')
c2 = compile(str2,'','eval')        # 编译为表达式 
result = eval(c2)                    # 执行
