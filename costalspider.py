from bs4 import BeautifulSoup
import urllib.request
import pymysql
import os


class CostalSpider(object):

    # 解析页面获取HMTL文本数据
    def get_content(url):
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')

    # 获取JS动态页面URL
    def get_allurl(html_text):
        soup = BeautifulSoup(html_text, "lxml")
        url_dict = {}
        # 找到class=jcarousel-skin-tango下所有li标签
        li_arr = soup.select("[class=jcarousel-skin-tango]")[0].select("li")
        for i in li_arr:  # 遍历li标签拿到所有js动态页面路径
            url_dict[
                i.p.string] = "http://www.nmc.cn/f/rest/getContent?dataId=" + i.p.attrs['data-id']
        return url_dict

    # 分析HTML页面，根据标签选择器拿有效数据
    def get_data(html_text, publish_time):
        soup = BeautifulSoup(html_text, "lxml")
        tr = soup.select('tr[align=left]')  # 找到所有tr标签
        final = []
        for i in tr:
            weatherdata_arr = [publish_time]
            ocean_name = i.attrs['name']  # tr标签中属性name为海区名称
            weatherdata_arr.append(ocean_name)  # 保存海区名称到列表
            td = i.select('td')  # 找到tr标签下的td标签
            for j in range(len(td)):  # 遍历所有td
                if(len(td) == 6):  # 如果tr下包含6个td标签，第一个td标签是海区名称，之前保存了是无效数据
                    if(j != 5):
                        weatherdata_arr.append(td[j + 1].string)
                else:
                    weatherdata_arr.append(td[j].string)
            final.append(weatherdata_arr)  # 把页面所有数据保存到列表
        return final

    # 数据保存到数据库
    def save_db(data_arr):
        db = pymysql.connect("127.0.0.1", "marine_weather",
                             "qwe123", "marine_weather", charset="utf8")  # 连接数据库
        cursor = db.cursor()
        for i in data_arr:
            try:
                cursor.execute('INSERT INTO COASTAL(PUBLISH_TIME,OCEAN_NAME,FORECAST_TIME,PHENOMENON,WIND_DIRECTION,WIND_POWER,VISIBILITY) VALUES ("%s","%s","%s","%s","%s","%s","%s")' %
                               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))  # 插入数据
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
        db.close()

    # 记录日记
    def log(url_dict):
        file = open('./logs.txt', 'a+', encoding='utf-8')
        for key in url_dict:  # 迭代url字典把连接写入日志文件
            file.write(url_dict[key] + '\n')
        file.close()

    # 判断页面数据是否抓取过
    def flag_log(url_dict):
        log_folder_path = "./logs"
        isExists = os.path.exists(log_folder_path)
        if not isExists:
            os.makedirs(log_folder_path)
        # a+模式文件不存在则创建，追加位置从文本末尾开始
        file = open(log_folder_path+'/coastal_logs.txt', 'a+', encoding='utf-8')
        file.seek(0)  # 为了读取文件，把游标设置到文件头开始读
        for line in file:  # 逐行遍历文件内容
            for key in list(url_dict.keys()):  # 遍历页面抓取的JS链接URL，如果相同即抓过数据了，从URL字典里删除
                if(url_dict[key] + '\n' == line):
                    url_dict.pop(key)
        file.close()

    if __name__ == '__main__':
        url = 'http://www.nmc.cn/publish/marine/newcoastal.html'
        html_text = get_content(url)
        url_dict = get_allurl(html_text)
        flag_log(url_dict)
        for key in url_dict:
            tmp_text = get_content(url_dict[key])
            result = get_data(tmp_text, key)
            save_db(result)
        log(url_dict)
