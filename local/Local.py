__author__ = '祥祥'

import os.path

def get_club_urls_at_local(city):
    if os.path.exists(city) and os.path.isdir(city):
        files = os.listdir(city)
        url_files = [city+'/'+x for x in files]
        detail_urls = []
        for file in url_files:
            openfile = open(file, 'r', 1, 'utf-8')
            urls = openfile.readlines()
            detail_urls += urls
        return detail_urls
    else:
        return []

#初始化结果文件
def init_result_in_city(city):
    folder_name = city + '_detail'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    detail_file = city + '_detail/clubdetail.txt'
    # if os.path.exists(detail_file):
    #     os.remove(detail_file)
    return detail_file

def get_error_file_in_city(city):
    folder_name = city + '_detail'
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    error_file = city + '_detail/errorurl.txt'
    # if os.path.exists(detail_file):
    #     os.remove(detail_file)
    return error_file