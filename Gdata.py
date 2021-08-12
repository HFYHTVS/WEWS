'''GET DATA'''
import requests
import re
import json
import Gip


def Gweather(province_,city_):
    # token
    requests.packages.urllib3.disable_warnings()
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJBY2NvdW50SWQiOiJhYWRhZTVkNTVhMDVjOTM2OTU2YzJjYWMyNGUzNjliNiJ9.YBM7f506K6v9scq1dlLfi3EhXOW22DcvA0rD6_6T98w'
    rep = requests.get(f'https://www.douyacun.com/api/openapi/weather?province={province_}&city={city_}&weather_type=forecast_hour|forecast_day|alarm|limit|rise|observe|life_index|air&token={token}',verify=False)
    rep.encoding = 'utf-8'
    data = json.loads(rep.text)
    return data


def Glocal():
    ip,addres = Gip.get_all()
    if '省' in addres:
        province = addres.split('省')[0]
        city = addres.split('省')[1].split('市')[0]
    else:
        province = addres.split('市')[0]
        city = addres.split('市')[1].split('市')[0]
    l = [province,city]
    return  Gweather(province,city),l
    