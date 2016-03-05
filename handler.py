__author__ = '祥祥'

import os.path
from selenium import webdriver
import time
from model.ClubDetail import Club
from selenium.common.exceptions import NoSuchElementException


#分析list page 并把结果存入detail pages文件中           'beijing'
def handle_list_data(browser, index):
    folder_name = 'beijing'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    file_name = 'beijing/detail_pages_'+ str(index) +'.txt'

    #删除已存在的文件
    if os.path.exists(file_name):
        os.remove(file_name)
        print('已删除存在的文件', file_name)
    #追加写入文件内容
    file = open(file_name, 'w+', 1, 'utf-8', newline='\n')

    detail_list = analyse_list_page_for_detail(browser)

    #构造返回的字典数据

    #把列表写入文件中
    for item in detail_list:
        file.write(item + '\n')

    file.close()
    print('成功写入文件', file_name)
    #返回详情页的列表
    return detail_list

#分析列表page的内容，得到所有详情页的链接并返回
def analyse_list_page_for_detail(browser):
    detail_list = []
     #通过class 获取title和url
    # deal-tile__cover
    element_h3s = browser.find_elements_by_class_name('deal-tile__cover')
    for item in element_h3s:
        href = item.get_attribute('href')
        detail_list.append(href)
    return detail_list

#分析列表page的内容，得到所有其他列表页的链接并返回
def analyse_list_page_for_list(browser):
    list_list = []
    return list_list

#分析详情页内容
def handle_detail_data(browser = None, data = None, index = 0, error_file = None):
    club = Club()

    if data is not None:
        #TODO write to file
        USE_DATA = False
        if USE_DATA:
            folder_name = 'beijing_detail'
            if not os.path.exists(folder_name):
                os.mkdir(folder_name)
            file_name = 'beijing_detail/detail_pages_'+ str(index) +'.txt'
            print('开始写入文件... ', file_name)
            #删除已存在的文件
            if os.path.exists(file_name):
                os.remove(file_name)
                print('已删除存在的文件', file_name)
            #追加写入文件内容
            file = open(file_name, 'w+', 1, 'utf-8', newline='\n')
            file.write(data)
            file.close()
            print('写入文件成功... ', file_name)
        else:
            element_class = 'search-path'
            map_location_name = 'tocoord'
            class_name = 'deal-component-title'
            class_area = 'deal-component-title-prefix'
            class_location = 'div[class=\"biz-item field-group\"]'
            class_cover = 'focus-view'
            class_phone = 'biz-item'    #这个class被多个引用 需使用最后一个
            class_meituan_category = 'bread-nav'    #在美团中的分类 位置》地域》。。。
            class_intro = 'standard-content'   #酒吧介绍
            current_class = ''
            try:
                current_class = element_class
                element_search = browser.find_element_by_class_name(element_class)
                element_search.click()
                time.sleep(0.7)
                #经纬度
                current_class = map_location_name
                element_map_location = browser.find_element_by_name(map_location_name)
                lati_longi = element_map_location.get_attribute('value')
                club.setLatiLongi(lati_longi)
                #酒吧名
                current_class = class_name
                element_clubname = browser.find_element_by_class_name(class_name)
                club.name = element_clubname.text
                #区域名
                current_class = class_area
                element_area = browser.find_element_by_class_name(class_area)
                club.area = element_area.text.strip('【').strip('】')
                #位置
                current_class = class_location
                element_location = browser.find_element_by_css_selector(class_location)
                club.location = element_location.get_attribute('title')
                #cover图
                current_class = class_cover
                element_cover = browser.find_element_by_class_name(class_cover)
                club.cover = element_cover.get_attribute('src')
                #在美团中的分类  包括地域  位置  分类
                current_class = class_meituan_category
                element_category = browser.find_element_by_class_name(class_meituan_category)
                club.meituan_category = element_category.text
                #phone
                current_class = class_phone
                element_phones = browser.find_elements_by_class_name(class_phone)

                if len(element_phones) > 0:
                    element_phone = element_phones[-1]
                    text = element_phone.text
                    club.phone = text.split('：')[1]
                else:
                    print('club has no phone at ', browser.current_url)
                    error_file.write(browser.current_url)

                #酒吧简介
                current_class = class_intro
                element_intro = browser.find_elements_by_class_name(class_intro)[-1]
                club.club_intro = element_intro.find_element_by_tag_name('p').text

            except NoSuchElementException:
                print('未找到 class ', current_class, browser.current_url)
                error_file.write(browser.current_url)

            except IndexError:
                print('未找到酒吧 phone， at', browser.current_url)
                error_file.write(browser.current_url)

            # folder_name = 'beijing_detail'
            # if not os.path.exists(folder_name):
            #     os.mkdir(folder_name)
            # file_name = 'beijing_detail/detail_pages_'+ str(index) +'.txt'
            # print('开始写入文件... ', file_name)
            # #删除已存在的文件
            # if os.path.exists(file_name):
            #     os.remove(file_name)
            #     print('已删除存在的文件', file_name)
            # #追加写入文件内容
            # file = open(file_name, 'w+', 1, 'utf-8', newline='\n')
            # file.write(browser.page_source)
            # file.close()
            # print('写入文件成功... ', file_name)
    else:
        print('data is none at index ', index)
    return club