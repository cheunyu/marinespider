from bs4 import BeautifulSoup
import urllib.request


class Spider(object):
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
for i in tr:
    ocean_name = i.attrs['name']
    data_arr = []
    td = i.select('td')
    for j in range(len(td)):
        if(len(td) == 6):
            if(j != 5):
                print(td[j + 1])
                data_arr.append(td[j + 1])
        else:
            data_arr.append(td[j])
            # print(td[j])
    print(len(data_arr))
