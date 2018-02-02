from bs4 import BeautifulSoup
import urllib.request
import pymysql


class CostalSpider(object):
    """docstring for Spider"""

    # def __init__(self, ocean_name, forecast_time, phenomenon, wind_direction, wind_power, visibility):
    #     super(Spider, self).__init__()
    #     self.ocean_name = ocean_name
    #     self.forecast_time = forecast_time
    #     self.phenomenon = phenomenon
    #     self.wind_direction = wind_direction
    #     self.wind_power = wind_power
    #     self.visibility = visibility

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

    if __name__ == '__main__':
        url = 'http://www.nmc.cn/publish/marine/newcoastal.html'
        html_text = get_content(url)
        url_dict = get_allurl(html_text)
        for key in url_dict:
            print(key, url_dict[key])
            tmp_text = get_content(url_dict[key])
            result = get_data(tmp_text, key)
            save_db(result)
