from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from typing import Optional
import pandas as pd
import requests
import json
from io import StringIO
import math
from concurrent.futures import ThreadPoolExecutor, as_completed
import re
import asyncio
import csv
import httpx

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "This API aims to create a seamless integration of weather station data from the Hong Kong Observatory (HKO) and the Common Spatial Data Infrastructure (CSDI). The goal is to georeference the weather station data and transform it into a GeoJSON format for real-time fetching, visualization and analysis."}

wind_json ={ "type": "FeatureCollection", "features": [ { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1558333,22.2888889 ] }, "properties": { "AutomaticWeatherStation_uc":"中環碼頭", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_0.csv", "AutomaticWeatherStation_en":"Central Pier" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9219444,22.3094444 ] }, "properties": { "AutomaticWeatherStation_uc":"赤鱲角", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_1.csv", "AutomaticWeatherStation_en":"Chek Lap Kok" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0266667,22.2011111 ] }, "properties": { "AutomaticWeatherStation_uc":"長 洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_2.csv", "AutomaticWeatherStation_en":"Cheung Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0291667,22.2108333 ] }, "properties": { "AutomaticWeatherStation_uc":"長洲泳灘", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_3.csv", "AutomaticWeatherStation_en":"Cheung Chau Beach" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1127778,22.285 ] }, "properties": { "AutomaticWeatherStation_uc":"青 洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_4.csv", "AutomaticWeatherStation_en":"Green Island" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.21429,22.2183 ] }, "properties": { "AutomaticWeatherStation_uc":"香港航海學校", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_5.csv", "AutomaticWeatherStation_en":"Hong Kong Sea School" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2133333,22.3097222 ] }, "properties": { "AutomaticWeatherStation_uc":"啟 德", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_6.csv", "AutomaticWeatherStation_en":"Kai Tak" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1727778,22.3119444 ] }, "properties": { "AutomaticWeatherStation_uc":"京士柏", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_7.csv", "AutomaticWeatherStation_en":"King's Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1086111,22.2261111 ] }, "properties": { "AutomaticWeatherStation_uc":"南丫島", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_8.csv", "AutomaticWeatherStation_en":"Lamma Island" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9836111,22.4688889 ] }, "properties": { "AutomaticWeatherStation_uc":"流浮山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_9.csv", "AutomaticWeatherStation_en":"Lau Fau Shan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9127778,22.2586111 ] }, "properties": { "AutomaticWeatherStation_uc":"昂 坪", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_10.csv", "AutomaticWeatherStation_en":"Ngong Ping" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.199722,22.294444 ] }, "properties": { "AutomaticWeatherStation_uc":"北 角", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_11.csv", "AutomaticWeatherStation_en":"North Point" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0433333,22.2911111 ] }, "properties": { "AutomaticWeatherStation_uc":"坪 洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_12.csv", "AutomaticWeatherStation_en":"Peng Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2744444,22.3755556 ] }, "properties": { "AutomaticWeatherStation_uc":"西 貢", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_13.csv", "AutomaticWeatherStation_en":"Sai Kung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.8911111,22.3458333 ] }, "properties": { "AutomaticWeatherStation_uc":"沙 洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_14.csv", "AutomaticWeatherStation_en":"Sha Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.21,22.4025 ] }, "properties": { "AutomaticWeatherStation_uc":"沙 田", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_15.csv", "AutomaticWeatherStation_en":"Sha Tin" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0847222,22.4361111 ] }, "properties": { "AutomaticWeatherStation_uc":"石 崗", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_16.csv", "AutomaticWeatherStation_en":"Shek Kong" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2186111,22.2141667 ] }, "properties": { "AutomaticWeatherStation_uc":"赤 柱", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_17.csv", "AutomaticWeatherStation_en":"Stanley" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.16842,22.293008 ] }, "properties": { "AutomaticWeatherStation_uc":"天星碼頭", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_18.csv", "AutomaticWeatherStation_en":"Star Ferry" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1566667,22.5286111 ] }, "properties": { "AutomaticWeatherStation_uc":"打鼓嶺", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_19.csv", "AutomaticWeatherStation_en":"Ta Kwu Ling" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2375,22.4752778 ] }, "properties": { "AutomaticWeatherStation_uc":"大美督", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_20.csv", "AutomaticWeatherStation_en":"Tai Mei Tuk" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1841667,22.4425 ] }, "properties": { "AutomaticWeatherStation_uc":"大埔滘", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_21.csv", "AutomaticWeatherStation_en":"Tai Po Kau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3605556,22.4713889 ] }, "properties": { "AutomaticWeatherStation_uc":"塔 門", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_22.csv", "AutomaticWeatherStation_en":"Tap Mun" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2177778,22.3577778 ] }, "properties": { "AutomaticWeatherStation_uc":"大老山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_23.csv", "AutomaticWeatherStation_en":"Tate's Cairn" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2555556,22.3158333 ] }, "properties": { "AutomaticWeatherStation_uc":"將軍澳", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_24.csv", "AutomaticWeatherStation_en":"Tseung Kwan O" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.11,22.3441667 ] }, "properties": { "AutomaticWeatherStation_uc":"青 衣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_25.csv", "AutomaticWeatherStation_en":"Tsing Yi" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9641667,22.3858333 ] }, "properties": { "AutomaticWeatherStation_uc":"屯 門", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_26.csv", "AutomaticWeatherStation_en":"Tuen Mun" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3033333,22.1822222 ] }, "properties": { "AutomaticWeatherStation_uc":"橫瀾島", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_27.csv", "AutomaticWeatherStation_en":"Waglan Island" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0088889,22.4666667 ] }, "properties": { "AutomaticWeatherStation_uc":"濕地公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_28.csv", "AutomaticWeatherStation_en":"Wetland Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1736111,22.2477778 ] }, "properties": { "AutomaticWeatherStation_uc":"黃竹坑", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_wind_csdi_29.csv", "AutomaticWeatherStation_en":"Wong Chuk Hang" } } ] }
temp_json = { "type": "FeatureCollection", "features": [ { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9219444,22.3094444 ] }, "properties": { "AutomaticWeatherStation_uc":"赤鱲角", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_0.csv", "AutomaticWeatherStation_en":"Chek Lap Kok" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0266667,22.2011111 ] }, "properties": { "AutomaticWeatherStation_uc":"長洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_1.csv", "AutomaticWeatherStation_en":"Cheung Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2997222,22.2633333 ] }, "properties": { "AutomaticWeatherStation_uc":"清水灣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_2.csv", "AutomaticWeatherStation_en":"Clear Water Bay" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1836111,22.2705556 ] }, "properties": { "AutomaticWeatherStation_uc":"跑馬地", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_3.csv", "AutomaticWeatherStation_en":"Happy Valley" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1741667,22.3019444 ] }, "properties": { "AutomaticWeatherStation_uc":"天文台", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_4.csv", "AutomaticWeatherStation_en":"HK Observatory" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1622222,22.2783333 ] }, "properties": { "AutomaticWeatherStation_uc":"香港公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_5.csv", "AutomaticWeatherStation_en":"HK Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2169444,22.3047222 ] }, "properties": { "AutomaticWeatherStation_uc":"啟德跑道公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_6.csv", "AutomaticWeatherStation_en":"Kai Tak Runway Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3125,22.3702778 ] }, "properties": { "AutomaticWeatherStation_uc":"滘西洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_7.csv", "AutomaticWeatherStation_en":"Kau Sai Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1727778,22.3119444 ] }, "properties": { "AutomaticWeatherStation_uc":"京士柏", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_8.csv", "AutomaticWeatherStation_en":"King's Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1847222,22.335 ] }, "properties": { "AutomaticWeatherStation_uc":"九龍城", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_9.csv", "AutomaticWeatherStation_en":"Kowloon City" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2247222,22.3186111 ] }, "properties": { "AutomaticWeatherStation_uc":"觀塘", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_10.csv", "AutomaticWeatherStation_en":"Kwun Tong" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9836111,22.4688889 ] }, "properties": { "AutomaticWeatherStation_uc":"流浮山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_11.csv", "AutomaticWeatherStation_en":"Lau Fau Shan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9127778,22.2586111 ] }, "properties": { "AutomaticWeatherStation_uc":"昂坪", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_12.csv", "AutomaticWeatherStation_en":"Ngong Ping" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3230556,22.4027778 ] }, "properties": { "AutomaticWeatherStation_uc":"北潭涌", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_13.csv", "AutomaticWeatherStation_en":"Pak Tam Chung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0433333,22.2911111 ] }, "properties": { "AutomaticWeatherStation_uc":"坪洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_14.csv", "AutomaticWeatherStation_en":"Peng Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2744444,22.3755556 ] }, "properties": { "AutomaticWeatherStation_uc":"西貢", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_15.csv", "AutomaticWeatherStation_en":"Sai Kung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.21,22.4025 ] }, "properties": { "AutomaticWeatherStation_uc":"沙田", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_16.csv", "AutomaticWeatherStation_en":"Sha Tin" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1369444,22.3358333 ] }, "properties": { "AutomaticWeatherStation_uc":"深水埗", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_17.csv", "AutomaticWeatherStation_en":"Sham Shui Po" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2361111,22.2816667 ] }, "properties": { "AutomaticWeatherStation_uc":"筲箕灣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_18.csv", "AutomaticWeatherStation_en":"Shau Kei Wan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0847222,22.4361111 ] }, "properties": { "AutomaticWeatherStation_uc":"石崗", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_19.csv", "AutomaticWeatherStation_en":"Shek Kong" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1111111,22.5019444 ] }, "properties": { "AutomaticWeatherStation_uc":"上水", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_20.csv", "AutomaticWeatherStation_en":"Sheung Shui" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2186111,22.2141667 ] }, "properties": { "AutomaticWeatherStation_uc":"赤柱", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_21.csv", "AutomaticWeatherStation_en":"Stanley" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1566667,22.5286111 ] }, "properties": { "AutomaticWeatherStation_uc":"打鼓嶺", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_22.csv", "AutomaticWeatherStation_en":"Ta Kwu Ling" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1175,22.4847222 ] }, "properties": { "AutomaticWeatherStation_uc":"大隴", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_23.csv", "AutomaticWeatherStation_en":"Tai Lung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2375,22.4752778 ] }, "properties": { "AutomaticWeatherStation_uc":"大美督", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_24.csv", "AutomaticWeatherStation_en":"Tai Mei Tuk" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1244444,22.4105556 ] }, "properties": { "AutomaticWeatherStation_uc":"大帽山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_25.csv", "AutomaticWeatherStation_en":"Tai Mo Shan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1788889,22.4461111 ] }, "properties": { "AutomaticWeatherStation_uc":"大埔", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_26.csv", "AutomaticWeatherStation_en":"Tai Po" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2177778,22.3577778 ] }, "properties": { "AutomaticWeatherStation_uc":"大老山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_27.csv", "AutomaticWeatherStation_en":"Tate's Cairn" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.155,22.2641667 ] }, "properties": { "AutomaticWeatherStation_uc":"山頂", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_28.csv", "AutomaticWeatherStation_en":"The Peak" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2555556,22.3158333 ] }, "properties": { "AutomaticWeatherStation_uc":"將軍澳", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_29.csv", "AutomaticWeatherStation_en":"Tseung Kwan O" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.11,22.3441667 ] }, "properties": { "AutomaticWeatherStation_uc":"青衣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_30.csv", "AutomaticWeatherStation_en":"Tsing Yi" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1077778,22.3836111 ] }, "properties": { "AutomaticWeatherStation_uc":"荃灣可觀", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_31.csv", "AutomaticWeatherStation_en":"Tsuen Wan Ho Koon" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1266667,22.3755556 ] }, "properties": { "AutomaticWeatherStation_uc":"荃灣城門谷", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_32.csv", "AutomaticWeatherStation_en":"Tsuen Wan Shing Mun Valley" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9641667,22.3858333 ] }, "properties": { "AutomaticWeatherStation_uc":"屯門", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_33.csv", "AutomaticWeatherStation_en":"Tuen Mun" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3033333,22.1822222 ] }, "properties": { "AutomaticWeatherStation_uc":"橫瀾島", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_34.csv", "AutomaticWeatherStation_en":"Waglan Island" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0088889,22.4666667 ] }, "properties": { "AutomaticWeatherStation_uc":"濕地公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_35.csv", "AutomaticWeatherStation_en":"Wetland Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1736111,22.2477778 ] }, "properties": { "AutomaticWeatherStation_uc":"黃竹坑", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_36.csv", "AutomaticWeatherStation_en":"Wong Chuk Hang" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2052778,22.3394444 ] }, "properties": { "AutomaticWeatherStation_uc":"黃大仙", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_37.csv", "AutomaticWeatherStation_en":"Wong Tai Sin" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0183333,22.4408333 ] }, "properties": { "AutomaticWeatherStation_uc":"元朗公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_temperature_csdi_38.csv", "AutomaticWeatherStation_en":"Yuen Long Park" } } ] }
otemp_json ={ "type": "FeatureCollection", "features": [ { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9219444,22.3094444 ] }, "properties": { "AutomaticWeatherStation_uc":"赤鱲角", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_0.csv", "AutomaticWeatherStation_en":"Chek Lap Kok" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0266667,22.2011111 ] }, "properties": { "AutomaticWeatherStation_uc":"長洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_1.csv", "AutomaticWeatherStation_en":"Cheung Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2997222,22.2633333 ] }, "properties": { "AutomaticWeatherStation_uc":"清水灣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_2.csv", "AutomaticWeatherStation_en":"Clear Water Bay" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1836111,22.2705556 ] }, "properties": { "AutomaticWeatherStation_uc":"跑馬地", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_3.csv", "AutomaticWeatherStation_en":"Happy Valley" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1741667,22.3019444 ] }, "properties": { "AutomaticWeatherStation_uc":"天文台", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_4.csv", "AutomaticWeatherStation_en":"HK Observatory" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1622222,22.2783333 ] }, "properties": { "AutomaticWeatherStation_uc":"香港公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_5.csv", "AutomaticWeatherStation_en":"HK Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2169444,22.3047222 ] }, "properties": { "AutomaticWeatherStation_uc":"啟德跑道公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_6.csv", "AutomaticWeatherStation_en":"Kai Tak Runway Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3125,22.3702778 ] }, "properties": { "AutomaticWeatherStation_uc":"滘西洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_7.csv", "AutomaticWeatherStation_en":"Kau Sai Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1727778,22.3119444 ] }, "properties": { "AutomaticWeatherStation_uc":"京士柏", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_8.csv", "AutomaticWeatherStation_en":"King's Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1847222,22.335 ] }, "properties": { "AutomaticWeatherStation_uc":"九龍城", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_9.csv", "AutomaticWeatherStation_en":"Kowloon City" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2247222,22.3186111 ] }, "properties": { "AutomaticWeatherStation_uc":"觀塘", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_10.csv", "AutomaticWeatherStation_en":"Kwun Tong" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9836111,22.4688889 ] }, "properties": { "AutomaticWeatherStation_uc":"流浮山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_11.csv", "AutomaticWeatherStation_en":"Lau Fau Shan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9127778,22.2586111 ] }, "properties": { "AutomaticWeatherStation_uc":"昂坪", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_12.csv", "AutomaticWeatherStation_en":"Ngong Ping" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3230556,22.4027778 ] }, "properties": { "AutomaticWeatherStation_uc":"北潭涌", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_13.csv", "AutomaticWeatherStation_en":"Pak Tam Chung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0433333,22.2911111 ] }, "properties": { "AutomaticWeatherStation_uc":"坪洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_14.csv", "AutomaticWeatherStation_en":"Peng Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2744444,22.3755556 ] }, "properties": { "AutomaticWeatherStation_uc":"西貢", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_15.csv", "AutomaticWeatherStation_en":"Sai Kung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.21,22.4025 ] }, "properties": { "AutomaticWeatherStation_uc":"沙田", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_16.csv", "AutomaticWeatherStation_en":"Sha Tin" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1369444,22.3358333 ] }, "properties": { "AutomaticWeatherStation_uc":"深水埗", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_17.csv", "AutomaticWeatherStation_en":"Sham Shui Po" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2361111,22.2816667 ] }, "properties": { "AutomaticWeatherStation_uc":"筲箕灣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_18.csv", "AutomaticWeatherStation_en":"Shau Kei Wan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0847222,22.4361111 ] }, "properties": { "AutomaticWeatherStation_uc":"石崗", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_19.csv", "AutomaticWeatherStation_en":"Shek Kong" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1111111,22.5019444 ] }, "properties": { "AutomaticWeatherStation_uc":"上水", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_20.csv", "AutomaticWeatherStation_en":"Sheung Shui" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2186111,22.2141667 ] }, "properties": { "AutomaticWeatherStation_uc":"赤柱", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_21.csv", "AutomaticWeatherStation_en":"Stanley" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1566667,22.5286111 ] }, "properties": { "AutomaticWeatherStation_uc":"打鼓嶺", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_22.csv", "AutomaticWeatherStation_en":"Ta Kwu Ling" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1175,22.4847222 ] }, "properties": { "AutomaticWeatherStation_uc":"大隴", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_23.csv", "AutomaticWeatherStation_en":"Tai Lung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2375,22.4752778 ] }, "properties": { "AutomaticWeatherStation_uc":"大美督", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_24.csv", "AutomaticWeatherStation_en":"Tai Mei Tuk" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1244444,22.4105556 ] }, "properties": { "AutomaticWeatherStation_uc":"大帽山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_25.csv", "AutomaticWeatherStation_en":"Tai Mo Shan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1788889,22.4461111 ] }, "properties": { "AutomaticWeatherStation_uc":"大埔", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_26.csv", "AutomaticWeatherStation_en":"Tai Po" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2177778,22.3577778 ] }, "properties": { "AutomaticWeatherStation_uc":"大老山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_27.csv", "AutomaticWeatherStation_en":"Tate's Cairn" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.155,22.2641667 ] }, "properties": { "AutomaticWeatherStation_uc":"山頂", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_28.csv", "AutomaticWeatherStation_en":"The Peak" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2555556,22.3158333 ] }, "properties": { "AutomaticWeatherStation_uc":"將軍澳", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_29.csv", "AutomaticWeatherStation_en":"Tseung Kwan O" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.11,22.3441667 ] }, "properties": { "AutomaticWeatherStation_uc":"青衣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_30.csv", "AutomaticWeatherStation_en":"Tsing Yi" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1077778,22.3836111 ] }, "properties": { "AutomaticWeatherStation_uc":"荃灣可觀", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_31.csv", "AutomaticWeatherStation_en":"Tsuen Wan Ho Koon" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1266667,22.3755556 ] }, "properties": { "AutomaticWeatherStation_uc":"荃灣城門谷", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_32.csv", "AutomaticWeatherStation_en":"Tsuen Wan Shing Mun Valley" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9641667,22.3858333 ] }, "properties": { "AutomaticWeatherStation_uc":"屯門", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_33.csv", "AutomaticWeatherStation_en":"Tuen Mun" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3033333,22.1822222 ] }, "properties": { "AutomaticWeatherStation_uc":"橫瀾島", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_34.csv", "AutomaticWeatherStation_en":"Waglan Island" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0088889,22.4666667 ] }, "properties": { "AutomaticWeatherStation_uc":"濕地公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_35.csv", "AutomaticWeatherStation_en":"Wetland Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1736111,22.2477778 ] }, "properties": { "AutomaticWeatherStation_uc":"黃竹坑", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_36.csv", "AutomaticWeatherStation_en":"Wong Chuk Hang" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.2052778,22.3394444 ] }, "properties": { "AutomaticWeatherStation_uc":"黃大仙", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_37.csv", "AutomaticWeatherStation_en":"Wong Tai Sin" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.0183333,22.4408333 ] }, "properties": { "AutomaticWeatherStation_uc":"元朗公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_past24_temperature_diff_csdi_38.csv", "AutomaticWeatherStation_en":"Yuen Long Park" } } ] }
humd_json = { "type": "FeatureCollection", "features": [ { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.92194444,22.3094444 ] }, "properties": { "AutomaticWeatherStation_uc":"赤鱲角", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_0.csv", "AutomaticWeatherStation_en":"Chek Lap Kok" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.02666667,22.2011111 ] }, "properties": { "AutomaticWeatherStation_uc":"長洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_1.csv", "AutomaticWeatherStation_en":"Cheung Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.29972222,22.2633333 ] }, "properties": { "AutomaticWeatherStation_uc":"清水灣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_2.csv", "AutomaticWeatherStation_en":"Clear Water Bay" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.17416667,22.3019444 ] }, "properties": { "AutomaticWeatherStation_uc":"天文台", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_3.csv", "AutomaticWeatherStation_en":"HK Observatory" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.16222222,22.2783333 ] }, "properties": { "AutomaticWeatherStation_uc":"香港公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_4.csv", "AutomaticWeatherStation_en":"Hong Kong Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.21694444,22.3047222 ] }, "properties": { "AutomaticWeatherStation_uc":"啟德跑道公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_5.csv", "AutomaticWeatherStation_en":"Kai Tak Runway Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3125,22.3702778 ] }, "properties": { "AutomaticWeatherStation_uc":"滘西洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_6.csv", "AutomaticWeatherStation_en":"Kau Sai Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.17277778,22.3119444 ] }, "properties": { "AutomaticWeatherStation_uc":"京士柏", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_7.csv", "AutomaticWeatherStation_en":"King's Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.18472222,22.335 ] }, "properties": { "AutomaticWeatherStation_uc":"九龍城", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_8.csv", "AutomaticWeatherStation_en":"Kowloon City" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.98361111,22.4688889 ] }, "properties": { "AutomaticWeatherStation_uc":"流浮山", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_9.csv", "AutomaticWeatherStation_en":"Lau Fau Shan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.32305556,22.4027778 ] }, "properties": { "AutomaticWeatherStation_uc":"北潭涌", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_10.csv", "AutomaticWeatherStation_en":"Pak Tam Chung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.04333333,22.2911111 ] }, "properties": { "AutomaticWeatherStation_uc":"坪洲", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_11.csv", "AutomaticWeatherStation_en":"Peng Chau" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.27444444,22.3755556 ] }, "properties": { "AutomaticWeatherStation_uc":"西貢", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_12.csv", "AutomaticWeatherStation_en":"Sai Kung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.21,22.4025 ] }, "properties": { "AutomaticWeatherStation_uc":"沙田", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_13.csv", "AutomaticWeatherStation_en":"Sha Tin" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.23611111,22.2816667 ] }, "properties": { "AutomaticWeatherStation_uc":"筲箕灣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_14.csv", "AutomaticWeatherStation_en":"Shau Kei Wan" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.08472222,22.4361111 ] }, "properties": { "AutomaticWeatherStation_uc":"石崗", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_15.csv", "AutomaticWeatherStation_en":"Shek Kong" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.11111111,22.5019444 ] }, "properties": { "AutomaticWeatherStation_uc":"上水", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_16.csv", "AutomaticWeatherStation_en":"Sheung Shui" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.15666667,22.5286111 ] }, "properties": { "AutomaticWeatherStation_uc":"打鼓嶺", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_17.csv", "AutomaticWeatherStation_en":"Ta Kwu Ling" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1175,22.4847222 ] }, "properties": { "AutomaticWeatherStation_uc":"大隴", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_18.csv", "AutomaticWeatherStation_en":"Tai Lung" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.17888889,22.4461111 ] }, "properties": { "AutomaticWeatherStation_uc":"大埔", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_19.csv", "AutomaticWeatherStation_en":"Tai Po" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.25555556,22.3158333 ] }, "properties": { "AutomaticWeatherStation_uc":"將軍澳", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_20.csv", "AutomaticWeatherStation_en":"Tseung Kwan O" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.11,22.3441667 ] }, "properties": { "AutomaticWeatherStation_uc":"青衣", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_21.csv", "AutomaticWeatherStation_en":"Tsing Yi" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.96416667,22.3858333 ] }, "properties": { "AutomaticWeatherStation_uc":"屯門", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_22.csv", "AutomaticWeatherStation_en":"Tuen Mun" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.30333333,22.1822222 ] }, "properties": { "AutomaticWeatherStation_uc":"橫瀾島", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_23.csv", "AutomaticWeatherStation_en":"Waglan Island" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.00888889,22.4666667 ] }, "properties": { "AutomaticWeatherStation_uc":"濕地公園", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_24.csv", "AutomaticWeatherStation_en":"Wetland Park" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.17361111,22.2477778 ] }, "properties": { "AutomaticWeatherStation_uc":"黃竹坑", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_1min_humidity_csdi_25.csv", "AutomaticWeatherStation_en":"Wong Chuk Hang" } } ] }
smls_json = { "type": "FeatureCollection", "features": [ { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.224991,22.315157 ] }, "properties": { "LP_NUMBER":"AB4818", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_AB4818_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.171015,22.31777 ] }, "properties": { "LP_NUMBER":"DF1020", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_DF1020_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.204519,22.333017 ] }, "properties": { "LP_NUMBER":"DF3633", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_DF3633_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.204583,22.332194 ] }, "properties": { "LP_NUMBER":"DF3637", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_DF3637_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.204639,22.331033 ] }, "properties": { "LP_NUMBER":"DF3644", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_DF3644_02.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.20464,22.330369 ] }, "properties": { "LP_NUMBER":"DF3647", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_DF3647_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.204611,22.329522 ] }, "properties": { "LP_NUMBER":"DF3651", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_DF3651_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.204576,22.328862 ] }, "properties": { "LP_NUMBER":"DF3654", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_DF3654_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.209811,22.321696 ] }, "properties": { "LP_NUMBER":"E7692", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_E7692_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.207796,22.321498 ] }, "properties": { "LP_NUMBER":"E7710", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_E7710_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.211365,22.32187 ] }, "properties": { "LP_NUMBER":"GF0710", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF0710_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.22374,22.314322 ] }, "properties": { "LP_NUMBER":"GF3637", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3637_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.223885,22.314722 ] }, "properties": { "LP_NUMBER":"GF3638", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3638_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.224662,22.31493 ] }, "properties": { "LP_NUMBER":"GF3640", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3640_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.225355,22.315073 ] }, "properties": { "LP_NUMBER":"GF3641", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3641_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.225609,22.314587 ] }, "properties": { "LP_NUMBER":"GF3643", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3643_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.225841,22.314045 ] }, "properties": { "LP_NUMBER":"GF3644", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3644_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.212971,22.309247 ] }, "properties": { "LP_NUMBER":"GF3831", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3831_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.212487,22.309188 ] }, "properties": { "LP_NUMBER":"GF3833", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3833_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.211431,22.308809 ] }, "properties": { "LP_NUMBER":"GF3837", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3837_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.211115,22.308653 ] }, "properties": { "LP_NUMBER":"GF3839", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3839_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.211083,22.308226 ] }, "properties": { "LP_NUMBER":"GF3842", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3842_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.211521,22.308128 ] }, "properties": { "LP_NUMBER":"GF3844", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3844_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.211648,22.308413 ] }, "properties": { "LP_NUMBER":"GF3846", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3846_04.csv" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.211864,22.308709 ] }, "properties": { "LP_NUMBER":"GF3851", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/smart-lamppost_GF3851_04.csv" } } ] }
visi_json = { "type": "FeatureCollection", "features": [ { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.1558333,22.2888889 ] }, "properties": { "AutomaticWeatherStation_uc":"中環", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_visibility_csdi_0.csv", "AutomaticWeatherStation_en":"Central" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 113.9219444,22.3094444 ] }, "properties": { "AutomaticWeatherStation_uc":"赤鱲角", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_visibility_csdi_1.csv", "AutomaticWeatherStation_en":"Chek Lap Kok" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.225833,22.285555 ] }, "properties": { "AutomaticWeatherStation_uc":"西灣河", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_visibility_csdi_2.csv", "AutomaticWeatherStation_en":"Sai Wan Ho" } }, { "type": "Feature", "geometry": { "type": "Point", "coordinates":  [ 114.3033333,22.1822222 ] }, "properties": { "AutomaticWeatherStation_uc":"橫瀾島", "Data_url":"https://data.weather.gov.hk/weatherAPI/hko_data/csdi/dataset/latest_10min_visibility_csdi_3.csv", "AutomaticWeatherStation_en":"Waglan Island" } } ] }

def process_row(row, coordinates, columns):
    properties = {
        row.index[col]: (
            None if isinstance(value := row[col], float) and math.isnan(value)
            else str(value) if isinstance(value, float) and math.isinf(value)
            else value
        )
        for col in columns
    }

    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": coordinates
        },
        "properties": properties
    }


def fetch_data(session, url):
    try:
        with session.get(url, verify=False) as response:
            response.raise_for_status()
            return response.content.decode('utf-8')  # Use UTF-8 decoding
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None


def fetch_and_process_data(wind_json, columns):
    features = []

    with requests.Session() as session:
        session.verify = False

        def fetch_and_process(feature):
            coordinates = feature['geometry']['coordinates']
            data_text = fetch_data(session, feature['properties']['Data_url'])
            if data_text:
                data = pd.read_csv(StringIO(data_text), encoding='utf-8')
                return [process_row(row, coordinates, columns) for _, row in data.iterrows()]
            return []

        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_feature = {executor.submit(fetch_and_process, feature): feature for feature in
                                 wind_json['features']}
            for future in as_completed(future_to_feature):
                features.extend(future.result())

    if not features:
        print("No data was successfully fetched.")
        return None

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return json.dumps(geojson, ensure_ascii=False)


@app.get("/weather/{data_type}")
async def get_weather_data(data_type: str):
    data_mappings = {
        "wind": (wind_json, [7, 8, 9, 10]),
        "temp": (temp_json, [7, 8]),
        "24vt": (otemp_json, [7, 8]),
        "rhum": (humd_json, [7, 8]),
        "smls": (smls_json, [9, 10]),
        "visi": (visi_json, [7, 8])
    }

    if data_type not in data_mappings:
        raise HTTPException(status_code=404, detail="Data type not found")

    json_data, indices = data_mappings[data_type]
    result = fetch_and_process_data(json_data, indices)

    if result:
        return JSONResponse(content=json.loads(result))
    else:
        raise HTTPException(status_code=500, detail="Failed to fetch and process data")


coordinates = {"Southern": [114.16014, 22.247461], "North": [114.128244, 22.496697],
               "Kwun Tong": [114.231174, 22.309625], "Tseung Kwan O": [114.259561, 22.317642],
               "Tuen Mun": [113.976728, 22.391143], "Tung Chung": [113.943659, 22.288889],
               "Eastern Air": [114.219372, 22.282886], "Tap Mun": [114.360719, 22.471317],
               "Kwai Chung": [114.129601, 22.357104], "Yuen Long": [114.022649, 22.445155],
               "Sha Tin": [114.184532, 22.376281], "Sham Shui Po": [114.159109, 22.330226],
               "Tai Po": [114.16457, 22.45096], "Mong Kok": [114.168272, 22.322611],
               "Central/Western": [114.144421, 22.284891], "Central": [114.158127, 22.281815],
               "Causeway Bay": [114.18509, 22.280133], "Tsuen Wan": [114.114535, 22.371742]}


@app.get("/aqhi/data/")
def get_pollutant_data(last=False):
    url = "https://www.aqhi.gov.hk/js/data/past_24_pollutant.js"
    data = fetch_and_extract_json(url, "station_24_data")

    if data:
        features = []
        for station_data in data:
            for entry in station_data:
                station_name = entry["StationNameEN"]
                if station_name in coordinates:
                    longitude, latitude = coordinates[station_name]

                    feature = {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [longitude, latitude]
                        },
                        "properties": {
                            "name": station_name,
                            "feature": []
                        }
                    }

                    measurement = {
                        "DateTime": entry["DateTime"],
                        "aqhi": entry["aqhi"],
                        "NO2": entry["NO2"],
                        "O3": entry["O3"],
                        "SO2": entry["SO2"],
                        "CO": entry["CO"],
                        "PM10": entry["PM10"],
                        "PM25": entry["PM25"]
                    }

                    existing_feature = next((f for f in features if f["properties"]["name"] == station_name), None)
                    if existing_feature:
                        existing_feature["properties"]["feature"].append(measurement)
                    else:
                        feature["properties"]["feature"].append(measurement)
                        features.append(feature)

        if last:
            for feature in features:
                if feature["properties"]["feature"]:
                    feature["properties"]["feature"] = [feature["properties"]["feature"][0]]

        geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        return geojson
    else:
        return {"error": "No match found"}


def fetch_and_extract_json(url, variable_name):
    response = requests.get(url)
    js_content = response.text

    pattern = rf"var {variable_name} = (.+);"
    match = re.search(pattern, js_content)
    if match:
        json_data = match.group(1)
        data = json.loads(json_data)
        return data
    else:
        return None


@app.get("/aqhi/repo/")
def get_aqhi_report_and_forecast():
    url = "https://www.aqhi.gov.hk/js/data/forecast_aqhi.js"
    aqhi_report = fetch_and_extract_json(url, "aqhi_report")
    aqhi_forecast = fetch_and_extract_json(url, "aqhi_forecast")

    response_data = {}
    if aqhi_report:
        response_data["aqhi_report"] = aqhi_report
    else:
        response_data["aqhi_report"] = {"error": "No match found for aqhi_report."}

    if aqhi_forecast:
        response_data["aqhi_forecast"] = aqhi_forecast
    else:
        response_data["aqhi_forecast"] = {"error": "No match found for aqhi_forecast."}

    return response_data


async def fetch_csv_data(url: str) -> pd.DataFrame:
    response = await asyncio.to_thread(requests.get, url)
    response.raise_for_status()
    csv_data = StringIO(response.text)
    return pd.read_csv(csv_data)


async def process_occupancy_data(bbox: Optional[str], limit: Optional[int]) -> pd.DataFrame:
    occupancy_url = "https://resource.data.one.gov.hk/td/psiparkingspaces/occupancystatus/occupancystatus.csv"
    parkingspaces_url = "parkingspaces.csv"

    occupancy_df = await fetch_csv_data(occupancy_url)
    occupancy_df.rename(columns={'ï»¿ParkingSpaceId': 'ParkingSpaceId'}, inplace=True)

    parkingspaces_df = pd.read_csv('parkingspaces.csv', skiprows=2)
    parkingspaces_df.rename(columns={'ParkingSpa': 'ParkingSpaceId'}, inplace=True)

    merged_df = pd.merge(occupancy_df, parkingspaces_df, on='ParkingSpaceId')
    merged_df = merged_df[
        ['ParkingSpaceId', 'SectionOfStreet', 'ParkingMeterStatus', 'OccupancyStatus', 'OccupancyDateChanged',
         'Latitude', 'Longitude', 'VehicleType', 'LPP', 'OperatingPeriod', 'TimeUnit', 'PaymentUnit']]

    if bbox:
        min_lon, min_lat, max_lon, max_lat = map(float, bbox.split(','))
        merged_df = merged_df.query('@min_lon <= Longitude <= @max_lon and @min_lat <= Latitude <= @max_lat')

    if limit:
        merged_df = merged_df.head(limit)

    return merged_df


def create_geojson(merged_df: pd.DataFrame) -> dict:
    features = [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['Longitude'], row['Latitude']]
            },
            "properties": row.drop(['Longitude', 'Latitude']).to_dict()
        }
        for _, row in merged_df.iterrows()
    ]

    return {
        "type": "FeatureCollection",
        "features": features
    }

@app.get("/td/meter")
async def process_data(bbox: Optional[str] = None, limit: Optional[int] = None):
    try:
        merged_df = await process_occupancy_data(bbox, limit)
        geojson_data = await asyncio.to_thread(create_geojson, merged_df)
        return JSONResponse(content=geojson_data, media_type="application/geo+json")

    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


async def fetch_csv_content(url):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            return response.content.decode('big5hkscs')
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Error fetching CSV data: {e}")

def process_csv_content(csv_content):
    file = StringIO(csv_content)
    reader = csv.reader(file, delimiter='|')
    header = next(reader)
    grouped_data = {}
    for row in reader:
        filtered_row = {col: val for col, val in zip(header, row)}
        district = filtered_row.get('DISTRICT_ENG', 'Unknown')

        if district not in grouped_data:
            grouped_data[district] = []
        grouped_data[district].append(filtered_row)
    return grouped_data


@app.get("/wsd/note")
async def get_wsd_note():
    csv_url = "https://www.esd.wsd.gov.hk/wsms_open_data/WSMS_OPEN_DATA(all).csv"

    csv_content = await fetch_csv_content(csv_url)
    grouped_data = process_csv_content(csv_content)
    json_data = json.dumps(grouped_data, ensure_ascii=False, indent=4)

    return json.loads(json_data)
