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

    def get_content(url):
        response = urllib.request.urlopen(url)
        return response.read().decode('utf-8')

    def get_data(html_text):
        soup = BeautifulSoup(html_text, "lxml")
        marineArea = soup.select('td[rowspan=6]')
        tr = soup.select('tr[align=left]')
        final = []
        for i in tr:
            ocean_name = i.attrs['name']
            weatherdata_arr = [ocean_name]
            td = i.select('td')
            for j in range(len(td)):
                if(len(td) == 6):
                    if(j != 5):
                        weatherdata_arr.append(td[j + 1].string)
                else:
                    weatherdata_arr.append(td[j].string)
            final.append(weatherdata_arr)
            
        return final

    def save_db(data_arr):

        db = pymysql.connect("127.0.0.1", "marine_weather",
                             "qwe123", "marine_weather", charset="utf8")
        cursor = db.cursor()
        for i in data_arr:
            try:
                cursor.execute('INSERT INTO COASTAL(OCEAN_NAME,FORECAST_TIME,PHENOMENON,WIND_DIRECTION,WIND_POWER,VISIBILITY) VALUES ("%s","%s","%s","%s","%s","%s")' %
                               (i[0], i[1], i[2], i[3], i[4],i[5]))
                db.commit()
            except Exception as e:
                print(e)
                db.rollback()
        db.close()
    
    if __name__ == '__main__':
        url = 'http://www.nmc.cn/publish/marine/newcoastal.html'
        html_text = get_content(url)
        result = get_data(html_text)
        save_db(result)