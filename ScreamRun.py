__author__ = '祥祥'

from tornado import httpclient
import urllib.request
import urllib
from collections import deque
from util.urls import UrlsInMeituan
from selenium import webdriver
from handler import handle_list_data
from handler import handle_detail_data
from selenium.common.exceptions import NoSuchElementException
from local.Local import get_club_urls_at_local
from local.Local import init_result_in_city
from local.Local import get_error_file_in_city
from read_club import read_club_from_file
from selenium.webdriver.common.keys import Keys
import time
import os.path

#超时时间
__REQUEST_TIME_OUT__ = 10
#构造浏览器引擎
browser = webdriver.Chrome(executable_path='./chromedriver.exe')     #use chrome
#构造http_cleint用于获取详情页
http_client = httpclient.HTTPClient()

#滚动页面
def scroll_to_end(browser):
    #滚动到底部
    #将页面滚动条拖到底部
    #for chrome 使用 body +str(10**x)
    x = 2
    while x < 6:
        x += 1
        js="document.body.scrollTop=document.body.clientHeight"
        browser.execute_script(js)
        time.sleep(0.8)

#获取详情页面的数据
def get_detail_page(detail_urls, city):
    print('详情页个数：', len(detail_urls))
    detail_name = init_result_in_city(city)
    error_name = get_error_file_in_city(city)
    #打开错误文件
    error_file = open(error_name, 'w', 1, 'utf-8')
    # 获取已经存在的个数
    open_file = open(detail_name, 'r', 1, 'utf-8')
    lines = len(open_file.readlines())
    open_file.close()
    # 打开写入的文件
    detail_file = open(detail_name, 'a', 1, 'utf-8')
    if lines < 2:
        detail_file.write('酒吧名     区域       位置     cover图      phone    纬度      经度    在美团中的分类（地域，类型等）   酒吧介绍\n')
    print('已经存在的个数：', lines - 1)
    for index in range(lines - 1 ,len(detail_urls)):
    # for index in range(50):
        print('-----------------------------------\n开始获取详情页   index :', index)
        request = httpclient.HTTPRequest(url=detail_urls[index].strip('\n'), request_timeout=__REQUEST_TIME_OUT__)
        try:
            response = http_client.fetch(request)
        except Exception:
            print('error at ', detail_urls[index].strip('\n'))
            error_file.write(detail_urls[index])
        else:
            if(response.code == 200):
                data = response.body.decode('utf-8')
                browser.get(detail_urls[index].strip('\n'))
                time.sleep(1.8)
                #处理详情页面
                club = handle_detail_data(browser, data=data, index=index, error_file=error_file)
                detail_file.write(str(club.to_string())+'\n')
    detail_file.close()
    error_file.close()
    pass

#获取某个城市的酒吧
def get_clubs_in_city(city='beijing'):


    #获取酒吧第一页列表
    url = UrlsInMeituan.listpage_url

    #列表和详情的数量
    cnt_list = 0

    #详情页的url列表
    detail_urls = []

    end = False
    city = 'beijing'

    if os.path.exists(city):
        detail_urls = get_club_urls_at_local(city)
        print('------------------------------\n从本地读取酒吧详情页面url列表')
    else:
        print('已经获取到的列表页面 : '+str(cnt_list)+'  正在解析' + url)
        #模拟浏览器请求页面
        browser.get(url)
        time.sleep(1)
        while not end:
            cnt_list += 1
            #获取列表队首元素
            print('已经获取到的列表页面 : '+str(cnt_list)+'  正在解析' + browser.current_url)
            #滑到最底端
            scroll_to_end(browser)
            #获取网页内容
            # data = browser.page_source
            # 写入文件
            # file_name = 'list_'+str(cnt_list)+'.txt'
            # file = open(file_name, 'w', 1, 'utf-8')
            # try:
            #     file.write(data)
            #     file.close()
            # except Exception:
            #     # write to error file
            #     print('error at page ', url, ' exception:',Exception.args)
            #     file.close()
            #     continue

            #正则表达式提取页面中的所有list界面和detail界面  判断是否已经访问过，加入待爬界面
            detail_list = handle_list_data(browser, cnt_list)
            detail_urls += detail_list

            #find next and click
            try:
                element_next = browser.find_element_by_class_name('next')
                element_next.click()
            except NoSuchElementException:
                end = True
                print('已经到了尽头，开始获取详情页数据......')
            pass
    #开始获取详情页
    get_detail_page(detail_urls, city)

if __name__ == '__main__':
    get_clubs_in_city('beijing')
    # read_club_from_file()

browser.close()
http_client.close()
