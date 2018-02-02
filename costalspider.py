from bs4 import BeautifulSoup
import urllib.request
import pymysql


class CostalSpider(object):
    """docstring for Spider"""

    def __init__(self, ocean_name, forecast_time, phenomenon, wind_direction, wind_power, visibility):
        super(Spider, self).__init__()
        self.ocean_name = ocean_name
        self.forecast_time = forecast_time
        self.phenomenon = phenomenon
        self.wind_direction = wind_direction
        self.wind_power = wind_power
        self.visibility = visibility


response = urllib.request.urlopen(
    'http://www.nmc.cn/publish/marine/newcoastal.html')
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, "lxml")
marineArea = soup.select('td[rowspan=6]')
# for i in marineArea:
#     print(i.string)
tr = soup.select('tr[align=left]')
db = pymysql.connect("127.0.0.1", "marine_weather",
                     "qwe123", "marine_weather", charset="utf8")
cursor = db.cursor()
cursor.execute("SELECT VERSION()")
print(cursor.fetchone())
for i in tr:
    ocean_name = i.attrs['name']
    data_arr = []
    td = i.select('td')
    for j in range(len(td)):
        if(len(td) == 6):
            if(j != 5):
                # print(td[j + 1])
                data_arr.append(td[j + 1])
        else:
            data_arr.append(td[j])
    try:
        cursor.execute('INSERT INTO COASTAL(OCEAN_NAME,FORECAST_TIME,PHENOMENON,WIND_DIRECTION,WIND_POWER,VISIBILITY) VALUES ("%s","%s","%s","%s","%s","%s")' %
                       (ocean_name, data_arr[0].string, data_arr[1].string, data_arr[2].string, data_arr[3].string, data_arr[4].string))
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
db.close()