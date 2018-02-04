from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
import urllib.request
import pymysql
import os


class CostalSpider(object):

    # 解析页面获取HMTL文本数据
    def get_content(url):
        response = urllib.request.urlopen(url)
        return response.read()

    # 获取JS动态页面URL
    def get_allurl(html_text):
        soup = BeautifulSoup(html_text, "lxml")
        url_arr = []
        # 找到class=jcarousel-skin-tango下所有li标签
        li_arr = soup.select("[class=jcarousel-skin-tango]")[0].select("li")
        for i in li_arr:  # 遍历li标签拿到所有js动态页面路径
            url_arr.append(
                i.p.img.attrs['data-original'].replace('small', 'medium'))
        return url_arr

    # 保存图片文件到本地文件夹
    def save_img(img_url):

        # 定义图片存储文件夹路径，不存在则创建
        img_folder_path = "./wxyt"
        isExists = os.path.exists(img_folder_path)
        if not isExists:
            os.makedirs(img_folder_path)
        # 根据图片URL获取日期信息
        url_data = img_url[img_url.rfind('_') + 1:img_url.rfind('_') + 13]
        # 图片按日期创建子文件夹,不存在则创建
        date_folder_path = img_folder_path + '/' + url_data[0:8]
        isExists = os.path.exists(date_folder_path)
        if not isExists:
            os.makedirs(date_folder_path)
        # 图片按yyyyMMddHHmm命名，URL日期信息加8小时正确对应图片信息与文件名
        url_time = datetime.strptime(url_data, '%Y%m%d%H%M')
        img_time = url_time + timedelta(hours=8)
        urllib.request.urlretrieve(
            img_url, filename=date_folder_path + '/' + img_time.strftime('%Y%m%d%H%M') + '.jpg')

    # 记录日记
    def log(url_arr):
        file = open('./logs/wxytlogs.txt', 'a+', encoding='utf-8')
        for each in url_arr:  # 迭代url列表把连接写入日志文件
            file.write(each + '\n')
        file.close()

    # 判断图片是否下载过
    def flag_log(url_arr):
        log_folder_path = "./logs"
        isExists = os.path.exists(log_folder_path)
        if not isExists:
            os.makedirs(log_folder_path)
        # a+模式文件不存在则创建，追加位置从文本末尾开始
        file = open('./logs/wxytlogs.txt', 'a+', encoding='utf-8')
        file.seek(0)  # 为了读取文件，把游标设置到文件头开始读
        for line in file:  # 逐行遍历文件内容
            for i in range(len(url_arr) - 1, -1, -1):  # 遍历图片链接，如果相同即下载过，从URL列表里删除
                if(url_arr[i] + '\n' == line):
                    url_arr.pop(i)
        file.close()

    if __name__ == '__main__':
        url = 'http://www.nmc.cn/publish/satellite/fy2.htm'
        html_text = get_content(url)
        url_arr = get_allurl(html_text)
        flag_log(url_arr)
        for each in url_arr:
            save_img(each)
        log(url_arr)
