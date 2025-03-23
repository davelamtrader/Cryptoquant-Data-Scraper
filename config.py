import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import time
from datetime import date, datetime, timedelta
import pandas as pd
import random
import os
import sys
import multiprocessing
from multiprocessing import Manager
# from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains 
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from seleniumwire import webdriver
import js2xml
import scrapy_splash
import undetected_chromedriver as uc


def get_metrics_chart_id():
    pass


def generate_coin_config(chrome_path):
    url = 'https://live-api.cryptoquant.com/api/v2/assets'
    webdriver_service = Service(chrome_path)
    chrome_options = Options()
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.get(url)
    time.sleep(0.5)
    content = driver.find_element(By.TAG_NAME, 'body').text
    data = json.loads(content)
    
    id_dict = {item['symbol']: item['id'] for item in data}
    type_dict = {item['symbol']: item['coin'] for item in data}
    driver.close()
    return id_dict, type_dict


def generate_coin_metrics(chrome_path, id_dict):
    id_list = list(id_dict.values())
    symbols = list(id_dict.keys())
    sub = '_config'
    os.makedirs(sub, exist_ok=True)
    
    metrics_dict = {}
    for sym, cid in zip(symbols, id_list):
        url = f'https://live-api.cryptoquant.com/api/v2/assets/{cid}/metrics'
        webdriver_service = Service(chrome_path)
        chrome_options = Options()
        driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
        driver.get(url)
        time.sleep(0.5)
        content = driver.find_element(By.TAG_NAME, 'body').text
        raw_data = json.loads(content)
        single_dict = {}
        for item in raw_data:
            cat = item['category']['path']  #e.g. exchange-flow
            mets_items = item['category']['metrics']
            mets_list = [{'id': m['id'], 'name': m['path']} for m in mets_items]
            single_dict[cat] = mets_list
         
        fp = os.path.join(sub, f'{sym}_metrics.json')
        with open(fp, 'w') as json_file:
            json.dump(single_dict, json_file)
        print(f'Metrics file of {sym} saved successfully!')
        
        metrics_dict[sym] = {'coin_id': cid, 'metrics':single_dict}

    filepath = os.path.join(sub, f'all_metrics.json')
    with open(filepath, 'w') as json_file:
        json.dump(metrics_dict, json_file)
    print('Successfully created a json file storing all metrics from all coins!')
    return metrics_dict


def load_metrics_dict():
    filepath = '_config/all_metrics.json'
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    return data
      

def generate_chart_config(chrome_path, metrics_dict):
    # keys = list(metrics_dict.keys())
    keys = ['BTC', 'ETH', 'STABLE']
    result_dict = {}
    for key in keys:
        met_dict = metrics_dict[key]['metrics']
        cats = list(metrics_dict[key]['metrics'].keys())
        coin_met_ids = []
        coin_met_names = []
        for cat in cats:
           m = [item['id'] for item in met_dict[cat]] 
           n = [item['name'] for item in met_dict[cat]]
           coin_met_ids.extend(m)
           coin_met_names.extend(n)
        
        coin_full_metrics_config = []
        for mid, mn in zip(coin_met_ids, coin_met_names):
            url = f'https://live-api.cryptoquant.com/api/v3/metrics/{mid}/charts'
            webdriver_service = Service(chrome_path)
            chrome_options = Options()
            driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
            driver.get(url)
            time.sleep(0.5)
            content = driver.find_element(By.TAG_NAME, 'body').text
            raw_data = json.loads(content)
            chart_id = raw_data['charts'][0]['id']
            chart_name = raw_data['charts'][0]['title']['en'].replace(': ', ' - ')
            full_metric_name = f'{key}_{mn}'
            single_dict = {'metric_id': mid, 'metric_full_name': full_metric_name, 'chart_id': chart_id, 'chart_name': chart_name}
            coin_full_metrics_config.append(single_dict)
        
        fp = os.path.join('_config', f'{key}_full_metrics_charts.json')
        with open(fp, 'w') as json_file:
            json.dump(coin_full_metrics_config, json_file)
        print(f'All chart ids of {key} successfully fetched and put along with corresponding metrics and a full config file is created!')    
        
        result_dict[key] = coin_full_metrics_config
    
    filepath = os.path.join('_config', f'all_full_metrics_charts.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)
    print('Metrics and charts config data of all coins successfully saved as an aggregate json file!')


def read_chart_config(coin):
    filepath = f'_config/{coin}_full_metrics_charts.json'
    with open(filepath, 'r') as json_file:
        data = json.load(json_file)
    charts_data = [[item['chart_id'], item['chart_name']] for item in data]
    return charts_data


def generate_chart_link(chart_id, interval):  # interval=DAY
    start = int((datetime.now() - timedelta(days=int(365.25*20))).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()*1000)
    end = int((time.time()) * 1000)
    base = 'https://live-api.cryptoquant.com/api/v3/charts/'
    param = f'?window={interval}&from={start}&to={end}&limit=70000'
    url = base + chart_id + param
    return url


# def save_chart_data(coin, url, chart_name, chrome_path):
#     headers = {
#         "Accept": "application/json, text/plain, */*",
#         "Accept-Encoding": "gzip, deflate, br",
#         "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,ko;q=0.5",
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMjMyNiIsImlhdCI6MTcwMTE0ODkxOCwiZXhwIjoxNzAxMTUyNTE4fQ.xl075OemHorUIr9iQZalpXuEfwVSg-LnJh6uFB61yns",
#         "Dnt": "1",
#         "Origin": "https://cryptoquant.com",
#         "Referer": "https://cryptoquant.com/",
#         "Sec-Fetch-Dest": "empty",
#         "Sec-Fetch-Mode": "cors",
#         "Sec-Fetch-Site": "same-site",
#         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
#     }
#
#     webdriver_service = Service(chrome_path)
#     chrome_options = Options()
#     driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
#     driver.get(url)
#     data = driver.find_element(By.TAG_NAME, 'body').text
#     name = chart_name.replace("/", " ")
#
#     sub = f'data/{coin}'
#     os.makedirs(sub, exist_ok=True)
#     filepath = os.path.join(sub, f'{name}.json')
#     with open(filepath, 'w') as json_file:
#         json.dump(data, json_file)
#     print(f'Chart data of {chart_name} successfully saved!')
#     time.sleep(0.2)


# def test_api():
#     url = 'https://api.cryptoquant.com/v1/btc/market-indicator/estimated-leverage-ratio?exchange=binance&window=day&from=20191001&limit=100'
#     headers = {
#         "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMjMyNiIsImlhdCI6MTcwMTE0ODkxOCwiZXhwIjoxNzAxMTUyNTE4fQ.xl075OemHorUIr9iQZalpXuEfwVSg-LnJh6uFB61yns",
#     }
#     response = requests.get(url, headers=headers)
#     data = response.json()
#     print(data)


if __name__ == '__main__':

    # coin_id_dict, coin_type_dict = generate_coin_config(chrome_path)
    # generate_coin_metrics(chrome_path, coin_id_dict)
    # metrics_dict = load_metrics_dict()
    # generate_chart_config(chrome_path, metrics_dict)

    # start = int((time.time()) * 1000)
    # print(start)
    # start_date = datetime.fromtimestamp(start/1000)
    # print(start_date)
    #
    # end = int((datetime.now() - timedelta(days=int(365.25*20))).replace(hour=0, minute=0, second=0, microsecond=0).timestamp()*1000)
    # print(end)
    # end_date = datetime.fromtimestamp(end/1000)
    # print(end_date)

    # btc_charts = read_chart_config('BTC')
    # btc_urls = []
    # for chart_id, chart_name in btc_charts[36:]:
    #     url = generate_chart_link(chart_id, 'DAY')
    #     btc_urls.append(url)
    #     save_chart_data('BTC', url, chart_name, chrome_path)

    # eth_charts = read_chart_config('ETH')
    # eth_urls = []
    # for chart_id, chart_name in eth_charts:
    #     url = generate_chart_link(chart_id, 'DAY')
    #     eth_urls.append(url)
    #     save_chart_data('ETH', url, chart_name, chrome_path)

    # stable_charts = read_chart_config('STABLE')
    # for chart_id, chart_name in stable_charts:
    #     url = generate_chart_link(chart_id, 'DAY')
    #     save_chart_data('STABLE', url, chart_name, chrome_path)
    # test_api()

    chrome_path = r'C:\Users\user\Downloads\chromedriver-win32\chromedriver.exe'

    def req_interceptor(request):
        return request

    def res_interceptor(request, response):
        if '61a601d045de34521f1dcc7c' in request.url:
            print(response.text)
        return response.text

    webdriver_service = Service(chrome_path)
    driver = webdriver.Chrome(service=webdriver_service)
    driver.request_interceptor = req_interceptor
    driver.response_interceptor = res_interceptor
    test_url = 'https://cryptoquant.com/asset/btc/chart/market-indicator/adjusted-sopr-asopr?window=DAY&sma=0&ema=0&priceScale=log&metricScale=log&chartStyle=line'
    driver.get(test_url)
    time.sleep(20)

    # driver = uc.Chrome(headless=True, use_subprocess=False)
    # driver.get('https://cryptoquant.com/asset/btc/chart/market-indicator/adjusted-sopr-asopr?window=DAY&sma=0&ema=0&priceScale=log&metricScale=log&chartStyle=line')
    # time.sleep(10)
    # data = driver.find_element(By.TAG_NAME, 'body').text
    # print(data)