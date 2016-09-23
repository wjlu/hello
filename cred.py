#-*- coding:utf-8 –*-
import sys
from bs4 import BeautifulSoup
from test2 import *
from test import *
import requests
import pymongo
import random, time, urllib, bs4, re, json, logging

#---------------不要删除------------
# # http://cn-proxy.com/
# proxy_list = [
#     'http://171.39.89.33:8123',
#     'http://1.162.55.154:8080',
#     'http://61.230.153.233:8080',
#     ]
daili=[]
file= open("/Users/abc/Documents/proxy_f_1","w+")
while 1:
    lines = file.readlines()
    if not lines:
        break
    for line in lines:
        print(line)
# # 随机获取代理ip
    #proxy_ip = random.choice(proxy_list)
    proxies = {'http': line}
    daili.append(proxies)
#---------------不要删除------------





client = pymongo.MongoClient('localhost',27017)
credit = client['credit']
sheet_1 = credit['sheet_1']
sheet_2 = credit['sheet_2']
sheet_3 = credit['sheet_3']
# print(proxies)

detail_url=[]
g_count=[]
b_count=[]
d_count=[]
def save(detail_url,g_count,b_count,d_count,proxies):
    time.sleep(0.2)
    #content = requests.get(url, values, headers=Headers)  # ,proxies=proxies
    #soup = BeautifulSoup(content.text, 'lxml')
    # values 后面不需要
    # for data in school_datas:
    #     time.sleep(1)
    #     encryStr=data['encryStr']
    #     detail_url = 'http://www.creditchina.gov.cn/credit_info_detail?objectType={}&encryStr='.format(objectType) +encryStr
    print('传入的数组参数')
    print(g_count)
    print(b_count)
    print(d_count)
    print(detail_url)
    print(proxies)
    wb_data = requests.get(detail_url, headers=Headers,proxies=proxies) #,
    soupa = BeautifulSoup(wb_data.text, 'lxml')
    jbxx_1=[]
    jbxx_2=[]
    jbxx_tt=[]
    tmp=[]

    data1 = {}
    patt = re.compile("^([^：]*)[：]{1}(.*)")  # 以非:的一个或者多个开头,然后以一个:结束,匹配之后的所有
    #判断有没有基础信息
    hh = soupa.select('div.creditsearch-tagsinfo')[0]
    # print('这里是hh信息')
    # print(hh)
    if hh.find('p','text-info'):
        print('个人没有基础信息')
    else:
        hh_len = soupa.select('ul.creditsearch-tagsinfo-ul ')[0]
        for i in soupa.find_all('li', class_='oneline'):
            jbxx_1.append(i.get_text().replace('\r', '').replace('\n', ''))
        print('企业分割线')
        print('基本信息共%s条' %(int((len(hh_len)-3)/2)))
        #print(jbxx_1)
        for i in range(0,int((len(hh_len)-3)/2)):
            if i == 5:
                pass
            else:
                tmp.append(jbxx_1[i].replace(' ',''))
        for i in range(0,len(tmp)):
            jbxx_2.append(patt.search(tmp[i]).groups()[1])
            jbxx_tt.append(patt.search(tmp[i]).groups()[0])
            data1[jbxx_tt[i]] = jbxx_2[i] if len(jbxx_2[i])>0 else None #类似 '企业名称：兴山县胡振全烟叶种植场'
        print('基本信息')
        print(data1)
        #sheet_2.insert_one({'基本信息': data1})


#---------以下为优良信息
    data3 = {}
    ylxx_1=[]
    ylxx_1_a=[]
    ylxx_2=[]
    ylxx_tt=[]
    #判断有没有优良信息
    yl = soupa.select('div.creditsearch-tagsinfo')[1]
    print('开始打印优良信息')
    #print(yl)
    if yl.find('p','text-info'):
        print('没有优良信息')
    else:
        print('优良信息共%s条:'%(g_count))
        for i in range(1,g_count+1):
            yl_len = soupa.select('ul.creditsearch-tagsinfo-ul ')[i]
            for i in yl_len:
                if '创建时间' in i:
                    ylxx_1.append(str(i).replace('\r', '').replace('\n', ''))
                else:
                    ylxx_1.append(str(i).replace('\r', '').replace('\n', '').replace(' ', ''))
            #以下代码为了去掉数组中的空
            #ylxx_1_a = []
            for i in ylxx_1:
                if i == '':
                    pass
                else:
                    ylxx_1_a.append(i)
            print('优良信息共%s行' %(int(len(ylxx_1_a))))
            #按照ly_patt,去掉数组中的多余标签,并按照健值对传给字典
            ly_patt = re.compile('^<liclass="oneline"><strong>([^：]*)[：]{1}</strong>(.*)</li>')
            for i in range(0,len(ylxx_1_a)):
                ylxx_2.append(ly_patt.search(ylxx_1_a[i]).groups()[1])
                ylxx_tt.append(ly_patt.search(ylxx_1_a[i]).groups()[0])
                data3[ylxx_tt[i]] = ylxx_2[i] if len(ylxx_2[i])>0 else None #类似 '企业名称：兴山县胡振全烟叶种植场'

            print(data3)

            #sheet_3.insert_one({'优良信息': data3})



    # ---------以下为负面信息



    # 判断有没有负面信息
    fm = soupa.select('div.creditsearch-tagsinfo')[2]
    print('开始打印负面信息')
    if fm.find('p', 'text-info'):
        print('没有负面信息')
    else:
        print('负面信息共%s条'%(b_count))
        for z in range(g_count+1,g_count+b_count+1):
            fmxx_2 = []
            fmxx_tt = []
            fmxx_1 = []
            fmxx_1_a = []
            data4 = {}
            fm_len = soupa.select('ul.creditsearch-tagsinfo-ul ')[z]

            for i in fm_len:
                if '入库时间' in i:
                    fmxx_1.append(str(i).replace('\r', '').replace('\n', ''))
                else:
                    fmxx_1.append(str(i).replace('\r', '').replace('\n', '').replace(' ', ''))
            # 以下代码为了去掉数组中的空
            for i in fmxx_1:
                if i == '':
                    pass
                else:
                    fmxx_1_a.append(i)
            print('1条负面信息共%s行' % (int(len(fmxx_1_a))))
            #print(fmxx_1_a)
            # 按照ly_patt,去掉数组中的多余标签,并按照健值对传给字典
            ly_patt = re.compile('^<liclass="oneline"><strong>([^：]*)[：]{1}</strong>(.*)</li>')

            for i in range(0, len(fmxx_1_a)):
                fmxx_2.append(ly_patt.search(fmxx_1_a[i]).groups()[1])
                #print(fmxx_2)
                fmxx_tt.append(ly_patt.search(fmxx_1_a[i]).groups()[0])
                data4[fmxx_tt[i]] = fmxx_2[i] if len(fmxx_2[i]) > 0 else None  # 类似 '企业名称：兴山县胡振全烟叶种植场'
                #print('mini循环')
                #print(data4)
            print('------一个公司的负面消息分隔线------------:')
            print(data4)
            # sheet_?.insert_one({'负面信息': data4})






#------------


    #dishonestyCount = data['dishonestyCount']
    #print('不诚实记录:%s' % (dishonestyCount))
    co=soupa.select('#dishonestyImg > ul')
    print('受惩黑名单有%s条' %(len(co)))
    for i in range(1,len(co)+1):
        sjly= soupa.select('#dishonestyImg > ul:nth-of-type({}) > li'.format(i))
        tmp = []
        for i in sjly:
            tmp.append(i.get_text().replace('\r','').replace('\n','').replace(' ',''))
        tmp_hmd=[]
        scxx_tt = []
        data2 ={}
        for i in range(0,len(tmp)):
            tmp_hmd.append(patt.search(tmp[i]).groups()[1])
            scxx_tt.append(patt.search(tmp[i]).groups()[0])
            data2[scxx_tt[i]]=tmp_hmd[i]

        print(data2)
        #sheet_2.insert_one({'受惩黑名单': data2})
#要改 这里写死了
#!!注意 注意 这里要考虑网速慢,页面没加载的情况   raise JSONDecodeError("Expecting value", s, err.value) from None

url = 'http://www.creditchina.gov.cn/credit_info_search?'
Headers={
    'User-Agent':'Mozilla/5.0 (Windowhttp://www.creditchina.gov.cn/search_all#keyword=330106198612054015&searchtype=0&departmentId=&creditType=&areas=&objectType=2&page=1s NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
    'Cookie':'Hm_lvt_0076fef7e919d8d7b24383dc8f1c852a=1472028511; Hm_lpvt_0076fef7e919d8d7b24383dc8f1c852a=1472042783'
}




def get_detail_link():
    #detail_url=[]
    page = 1
    values = {'keyword': '胡振',
              'searchtype': '0',
              'objectType': 2,  # 法人这里是2,自然人这里是1
              'dataType': '1',
              'page': page
              }
    data = requests.get(url, values).json()
    #data = requests.get(url, values_change)
    print("number records in one page :is", len(data['result']['results']))
    print ("total page counts:is",data["result"]["totalPageCount"])
    print("all message count is:", data["result"]["totalCount"])
    title_info = data['result']['results']

    # wb_data = requests.get(detail_url, headers=Headers)
    # soup = BeautifulSoup(wb_data.text, 'lxml')
    # records=soup.select('dd.credit-type')
    # print(records)

    for i in range(1, data["result"]["totalPageCount"]+1):
        time.sleep(0.1)
        page = i
        print("No Page:%s"%str(i))
        # values = {'keyword': '胡振',
        #           'searchtype': '0',
        #           'objectType': 2,  # 法人这里是2,自然人这里是1
        #           'dataType': '1',
        #           'page': page
        #           }
    #values 放在这里是因为是需要循环page
        for data in title_info:
            time.sleep(0.1)
            encryStr=data['encryStr']
            goodCount=data['goodCount']
            badCount=data['badCount']   # 不良记录
            dishonestyCount=data['dishonestyCount'] #受惩黑名单
            en_patt = re.compile("(.*)[\n]$")
            encryStr=en_patt.search(encryStr).groups()[0]
            detail_link='http://www.creditchina.gov.cn/credit_info_detail?objectType={}&encryStr='.format(values['objectType']) + encryStr
            detail_url.append('http://www.creditchina.gov.cn/credit_info_detail?objectType={}&encryStr='.format(values['objectType']) +encryStr)
            # print(goodCount)
            # print(badCount)
            # print(dishonestyCount)
            g_count.append(goodCount)
            b_count.append(badCount)
            d_count.append(dishonestyCount)
            # print(g_count)
            # print(b_count)
            # print(d_count)
            #sheet_1.insert_one({'url': detail_link})
            #sheet_1.insert_one({'credit_count': credit_count})
            #save(detail_url,g_count,b_count,d_count)

#save(detail_url,g_count,b_count,d_count)