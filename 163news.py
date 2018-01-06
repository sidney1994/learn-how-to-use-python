#!/usr/bin/env python
# encoding: utf-8
'''
@author: suidianbo
@file: 163news.py
@time: 2018/1/5 22:19
'''
from __future__ import division
import re
import urllib2
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from selenium import webdriver

#找到评论url
pattern1 = re.compile(r'http://.*com/')
pattern2 = re.compile(r'/\w*\.html')
def handle_url2_comment(url):
    global pattern1
    global pattern2
    b = re.findall(pattern1,url)[0]
    f = re.findall(pattern2,url)[0]
    m = re.sub(r'//', "", re.findall(r'//\w*\.',b)[0])[:-1]
    n = re.sub(r'//',r"//comment.",b)
    e='2_bbs'
    comment_url=n+m+e+f
    return comment_url
#爬取网易评论

def handel(content):
    raw_content = content.split('\n')
    raw_content = list(raw_content)
    #print "len", len(raw_content)
    if len(raw_content) < 3:
        #print "该数组为空"
        return "\n"
    else:
        for temp in raw_content:
            # 预处理只保留本层楼的评论，其他楼层的评论去除
            if temp == u"回复":
                index2 = raw_content.index(temp)
                raw_content.pop(index2)
                raw_content.pop(index2)
                raw_content.pop(index2)
                raw_content.pop(index2)
            #去除楼数
            if temp == "1" or temp == "2" or temp == "3" or temp == "4" or temp == "5" or temp == "6" or temp == "7" or temp == "8":
                index1 = raw_content.index(temp)
                raw_content.pop(index1-1)
                raw_content.pop(index1-1)
                raw_content.pop(index1-1)

        # 去除【此处隐藏..】这句话
        for temp in raw_content:
            #print "temp11", temp, type(temp)
            if re.match(ur"^[\u5df2\u7ecf\u9690\u85cf].*$", unicode(temp)):
                index3 = raw_content.index(temp)
                raw_content.pop(index3)

        # 从顶中提取数值
        for temp in raw_content:
            m = re.search(u"\u9876[^\d*?](\d*)\u005d", unicode(temp))
            if m:
                #print "temp11", temp
                index4 = raw_content.index(temp)
                raw_content[index4] = m.group(1)

        # 从踩中提取数值
        for temp in raw_content:
            m = re.search(u"\u8e29[^\d*?](\d*)\u005d", unicode(temp))
            if m:
                #print "temp11", temp
                index4 = raw_content.index(temp)
                raw_content[index4] = m.group(1)

    if len(raw_content) == 5:
        return raw_content   # 返回
    else:
        return "\n"


def Crawler(url):
    driver = webdriver.PhantomJS()
    driver.get(url)
    comment = ''

    total_comment = 0
    total_ding = 0
    total_cai = 0
    #抓取第一页的数据
    contents = driver.find_elements_by_class_name("reply")
    # 根据class抓取数据

    for content in contents:

        handel_data = handel(content.text)   # 调用处理函数返回一个list
        if handel_data == "\n":  # 如果为空
            continue
        else:
            comment = comment + "-----------------------------------------------------\n"
            # handel_data
            total_comment = total_comment+1
            total_ding = total_ding + int(handel_data[3])
            total_cai = total_cai + int(handel_data[4])
            for temp in handel_data:
                #print "temp22", temp, type(temp)
                comment = comment + temp + '\n'
    print "进入第 1 页"
    page = 1
    #抓取第二页到尾页的数据
    flag = True
    while True:
        try:
            if flag:
                driver.find_element_by_link_text("下一页").click()   # 找到下一页的连接进入
            else:
                flag = True
        except:
            try:
                driver.find_element_by_link_text("下一页").click()   # 再尝试一次
            except:
                break
            else:
                flag = False
                continue
        else:
            page += 1
            print "进入第 " + str(page) + " 页"
            if page > 20:
                break
            try:
                contents = driver.find_elements_by_class_name("reply")
                for content in contents:
                    handel_data = handel(content.text)  # 调用处理函数
                    if handel_data == "\n":  # 如果为空
                        continue
                    else:
                        comment = comment + "-----------------------------------------------------\n"
                        total_comment = total_comment + 1
                        total_ding = total_ding + int(handel_data[3])
                        total_cai = total_cai + int(handel_data[4])
                        for temp in handel_data:
                            # print "temp22", temp, type(temp)
                            comment = comment + temp + '\n'
            except:
                break


    driver.quit()
    return comment, total_comment, total_ding, total_cai


def getNewsdetial(url, newsTitle, newstime,i,newscomment,total_comment,total_ding,total_cai):


    req = urllib2.urlopen(url)
    res = req.read()
    soup = BeautifulSoup(res, 'lxml')
    tag = soup.find('div', class_='post_text').find_all('p')

    body = ''
    for p in tag:
        body += p.text + '\n'
    if '//' in body:
        body = body[:body.index('//')]
    body = body.replace(" ", "")

    doc = ET.Element("doc")
    ET.SubElement(doc, "id").text = "%d" % (i)
    ET.SubElement(doc, "url").text = url
    ET.SubElement(doc, "title").text = newsTitle
    ET.SubElement(doc, "datetime").text = newstime
    ET.SubElement(doc, "body").text = body
    if total_comment > 0:
        ET.SubElement(doc, "comment").text = newscomment
    else:
        ET.SubElement(doc, "comment").text = r"Oops,there is no comment!"
    ET.SubElement(doc, "total_comment").text = str(total_comment)
    ET.SubElement(doc, "total_ding").text = str(total_ding)
    ET.SubElement(doc, "total_cai").text = str(total_cai)
    tree = ET.ElementTree(doc)
    tree.write('../data/news2/' + "%d.xml" % (i), encoding='utf-8',  xml_declaration=True)
#生活
urls = ['http://temp.163.com/special/00804KVA/cm_shehui.js?callback=data_callback',
        'http://temp.163.com/special/00804KVA/cm_shehui_02.js?callback=data_callback',
        'http://temp.163.com/special/00804KVA/cm_shehui_03.js?callback=data_callback']
#国际
urls_guoji = ['http://temp.163.com/special/00804KVA/cm_guoji.js?callback=data_callback',
              'http://temp.163.com/special/00804KVA/cm_guoji_02.js?callback=data_callback',
              ]
#国内
urls_guonei = ['http://temp.163.com/special/00804KVA/cm_guonei_02.js?callback=data_callback',
               'http://temp.163.com/special/00804KVA/cm_guonei_03.js?callback=data_callback',
               'http://temp.163.com/special/00804KVA/cm_guonei.js?callback=data_callback']
def write_xml(url,k1):
    req = urllib2.urlopen(url)
    res = req.read().decode('gbk')
    pat1 = r'"title":"(.*?)",'
    pat2 = r'"tlink":"(.*?)",'
    pat3 = r'"time":"(.*?)",'
    pat4 = r'"commenturl":"(.*?)",'
    m1 = re.findall(pat1, res)
    news_title = []
    for i in m1:
        news_title.append(i)
    m2 = re.findall(pat2, res)
    news_url = []
    for j in m2:
        news_url.append(j)
    m3 = re.findall(pat3, res)
    news_time = []
    for k in m3:
        news_time.append(k)
    m4 = re.findall(pat4,res)
    comment_url =[]
    for ele in m4:
        comment_url.append(ele)
    for i in range(k1, len(news_url) + k1):
        print news_title[i - k1]
        print news_url[i - k1]
        print news_time[i - k1]
        print '正在爬取第' + str(i) + '个新闻', news_title[i - k1]

        try:
            newscomment, total_comment, total_ding, total_cai= Crawler(comment_url[i-k1])
            getNewsdetial(news_url[i - k1], news_title[i - k1], news_time[i - k1], i, newscomment, total_comment, total_ding, total_cai)
        except:

            getNewsdetial(news_url[i - k1], news_title[i - k1], news_time[i - k1], i,str(1),0,0,0)

# k1=1
# write_xml(urls[0],k1)
# req = urllib2.urlopen(urls[0])
# res = req.read().decode('gbk')
# pat2 = r'"tlink":"(.*?)",'
# m2 = re.findall(pat2, res)
# news_url = []
# for j in m2:
#     news_url.append(j)
# a=len(news_url)
#
# write_xml(urls[1], a+1)
# req = urllib2.urlopen(urls[1])
# res = req.read().decode('gbk')
# pat2 = r'"tlink":"(.*?)",'
# m2 = re.findall(pat2, res)
# news_url = []
# for j in m2:
#     news_url.append(j)
# b=len(news_url)
# write_xml(urls[2], a+b+1)
write_xml(urls_guoji[0], 211)
req = urllib2.urlopen(urls_guoji[0])
res = req.read().decode('gbk')
pat2 = r'"tlink":"(.*?)",'
m2 = re.findall(pat2, res)
news_url = []
for j in m2:
    news_url.append(j)
b=len(news_url)

write_xml(urls_guoji[1],211+b+1)
req = urllib2.urlopen(urls_guoji[1])
res = req.read().decode('gbk')
pat2 = r'"tlink":"(.*?)",'
m2 = re.findall(pat2, res)
news_url = []
for j in m2:
    news_url.append(j)
c=len(news_url)

write_xml(urls_guonei[0],211+b+c+1)
req = urllib2.urlopen(urls_guonei[0])
res = req.read().decode('gbk')
pat2 = r'"tlink":"(.*?)",'
m2 = re.findall(pat2, res)
news_url = []
for j in m2:
    news_url.append(j)
d=len(news_url)

write_xml(urls_guonei[1],211+b+c+d+1)
req = urllib2.urlopen(urls_guonei[1])
res = req.read().decode('gbk')
pat2 = r'"tlink":"(.*?)",'
m2 = re.findall(pat2, res)
news_url = []
for j in m2:
    news_url.append(j)
e=len(news_url)
write_xml(urls_guonei[2],211+b+c+d+e+1)

