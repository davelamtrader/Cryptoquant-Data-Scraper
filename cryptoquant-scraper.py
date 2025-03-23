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
import multiprocessing
from multiprocessing import Manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from seleniumwire import webdriver
from config import load_metrics_dict


def get_btc_exchange_netflow(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a5fbaf45de34521f1dcad1?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    print(response.text)
    empty = {'errorMsg': f'Failed to fetch exchange netflow details of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    netflow_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(netflow_dict)

    subfolder = 'exchange netflow'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_exchange_netflow_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(netflow_dict, json_file)

    return netflow_dict


def get_btc_exchange_inflow(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a5fbc145de34521f1dcae9?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch exchange inflow details of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    inflow_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(inflow_dict)

    subfolder = 'exchange inflow'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_exchange_inflow_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(inflow_dict, json_file)

    return inflow_dict


def get_btc_exchange_outflow(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a5fbf145de34521f1dcb49?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch exchange outflow details of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    outflow_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(outflow_dict)

    subfolder = 'exchange outflow'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_exchange_outflow_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(outflow_dict, json_file)

    return outflow_dict


def get_btc_top10_exchange_inflow(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a5fbda45de34521f1dcb1a?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch top10 inflow details of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    inflow_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(inflow_dict)

    subfolder = 'exchange inflow'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_top10_exchange_inflow_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(inflow_dict, json_file)

    return inflow_dict


def get_btc_top10_exchange_outflow(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a5fc0545de34521f1dcb7a?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch top10 outflow details of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    outflow_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(outflow_dict)

    subfolder = 'exchange outflow'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_top10_exchange_outflow_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(outflow_dict, json_file)

    return outflow_dict


def get_btc_exchange_reserve(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a5fb0c45de34521f1dcaad?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch exchange reserve details of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    reserve_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(reserve_dict)

    subfolder = 'exchange reserve'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_exchange_reserve_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(reserve_dict, json_file)

    return reserve_dict


def get_btc_exchange_supply_ratio(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/625fb832a09f3d33d55ed2f2?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch exchange supply ratio of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'exchange reserve'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_exchange_supply_ratio_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_exchange_stablecoins_ratio_usd(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a601a145de34521f1dcc65?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch exchange stablecoins ratio data.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'exchange reserve'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'exchange_stablecoins_ratio_usd_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_exchange_whale_ratio(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a6017c45de34521f1dcc28?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch exchange whale ratio of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    whale_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(whale_dict)

    subfolder = 'exchange whale ratio'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_exchange_whale_ratio_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(whale_dict, json_file)

    return whale_dict


def get_btc_est_leverage_ratio(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a601ac45de34521f1dcc78?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch leverage ratio data of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    leverage_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(leverage_dict)

    subfolder = 'estimated leverage ratio'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_est_leverage_ratio_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(leverage_dict, json_file)

    return leverage_dict


def get_btc_inflow_spent_output_ageband(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/621736973bde403580faf28f?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch spent output ageband of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    ageband_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(ageband_dict)

    subfolder = 'exchange inflow'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_inflow_spent_output_ageband_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(ageband_dict, json_file)

    return ageband_dict


def get_btc_inflow_spent_output_ageband_pct(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/621736a23bde403580faf2b5?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch spent output ageband percentage of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    ageband_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(ageband_dict)

    subfolder = 'exchange inflow'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_inflow_spent_output_ageband_pct_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(ageband_dict, json_file)

    return ageband_dict


def get_btc_short_term_sopr(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a601d445de34521f1dcc7d?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch short term sopr of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    sopr_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(sopr_dict)

    subfolder = 'sopr'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_short_term_sopr_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(sopr_dict, json_file)

    return sopr_dict


def get_btc_long_term_sopr(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a601d845de34521f1dcc7e?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch long term sopr of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    sopr_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(sopr_dict)

    subfolder = 'sopr'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_long_term_sopr_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(sopr_dict, json_file)

    return sopr_dict


def get_btc_adjusted_sopr(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a601d045de34521f1dcc7c?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch adjusted sopr of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    sopr_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(sopr_dict)

    subfolder = 'sopr'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_adjusted_sopr_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(sopr_dict, json_file)

    return sopr_dict


def get_btc_sopr_ratio(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61ade689b535b9646cab7c6a?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch lth/sth sopr ratio of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    sopr_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(sopr_dict)

    subfolder = 'sopr'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_sopr_ratio_lth-sth_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(sopr_dict, json_file)

    return sopr_dict


def get_btc_mvrv_ratio(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61a601c545de34521f1dcc7a?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch mvrv ratio of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    mvrv_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(mvrv_dict)

    subfolder = 'mvrv ratio'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_mvrv_ratio_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(mvrv_dict, json_file)

    return mvrv_dict


def get_btc_open_interest(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2916bc0e955292d727b?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch open interest data of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'open interest'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_open_interest_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_funding_rates(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2ab6bc0e955292d7291?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch funding rates data of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'funding rates'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_funding_rates_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_taker_buysell_ratio(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2c26bc0e955292d72b4?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch taker buy sell ratio data of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'taker buy sell ratio'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_taker_buy_sell_ratio_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_long_liq_usd(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2cf6bc0e955292d72d7?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch long liquidation data of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'liquidation'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_long_liquidation_usd_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_short_liq_usd(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2d36bc0e955292d72e8?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch short liquidation data of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'liquidation'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_short_liquidation_usd_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_market_cap(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2d56bc0e955292d72f9?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch market cap of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'market cap'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_market_cap_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_realized_cap(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2d96bc0e955292d72fa?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch realized cap of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'market cap'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_realized_cap_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_thermo_cap(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2e56bc0e955292d72fd?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch thermo cap of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'market cap'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_thermo_cap_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_korea_premium(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2f26bc0e955292d7300?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch korea premium of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'market cap'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_korea_premium_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_coinbase_premium(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc2ed6bc0e955292d72ff?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch coinbase premium of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'market cap'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_coinbase_premium_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_active_addresses(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc75d6bc0e955292d7307?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch active addresses of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'active addresses'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_active_addresses_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_fund_volume(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc1e26bc0e955292d7268?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch fund volume of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'fund data'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_fund_volume_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_btc_fund_holdings(headers):
    url = 'https://live-api.cryptoquant.com/api/v3/charts/61adc1ea6bc0e955292d7274?window=DAY&from=1068998400000&to=1700195442452&limit=70000'
    response = requests.get(url, headers=headers)
    empty = {'errorMsg': f'Failed to fetch fund holdings of BTC.'}
    data = response.json() if response.status_code == 200 else empty

    result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
    print(result_dict)

    subfolder = 'fund data'
    if not os.path.exists(subfolder):
        os.makedirs(subfolder)
    today = datetime.today().strftime('%Y%m%d')
    filepath = os.path.join(subfolder, f'btc_fund_holdings_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(result_dict, json_file)

    return result_dict


def get_summary_of_today(chrome_path):
    today = datetime.today().strftime('%Y-%m-%d')
    url = 'https://live-api.cryptoquant.com/api/v2/summary/summary-of-today?id=61712eb35a176168a02409e8'
    webdriver_service = Service(chrome_path)
    chrome_options = Options()
    driver = webdriver.Chrome(service=webdriver_service, options=chrome_options)
    driver.get(url)
    data = driver.find_element(By.TAG_NAME, 'body').text

    sub = f'data'
    os.makedirs(sub, exist_ok=True)
    filepath = os.path.join(sub, f'market_summary_{today}.json')
    with open(filepath, 'w') as json_file:
        json.dump(data, json_file)
    print(f'Market summary of today successfully saved!')
    time.sleep(0.2)


def get_supported_assets():
    filepath = 'supported_assets.json'
    with open(filepath, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        symbols = [item['symbol'] for item in data]
    symbols[2] = 'STABLECOIN'
    print(symbols)
    return symbols


def save_chart_data(all_coins, all_urls, all_endpoints):
    from playwright.sync_api import sync_playwright
    sign_in = "https://www.cryptoquant.com/sign-in"

    with sync_playwright() as p:

        def handle_response(response):
            if "api/v3/charts" in response.url:
                data = response.json()
                print(response.url)
                print(data['result']['data'][:4])
                if data != [] and data != {}:
                    # result_dict = {'keys': data['dataKeys'], 'result': data['result']['data']}
                    filepath = os.path.join(sub, f'{name}.json')
                    with open(filepath, 'w') as json_file:
                        json.dump(data, json_file)
                    print(f'{name} chart data of {coin} successfully saved!')

        browser = p.firefox.launch(headless=False, slow_mo=300, args=['--start-maximized'])
        page = browser.new_page(no_viewport=True)
        page.goto(sign_in, wait_until="networkidle")
        email = 'dalvin.lam@proton.me'
        page.fill("input[id=\"email\"]", email)
        time.sleep(1)
        password = '9R52JzbD@'
        page.fill("input[id=\"password\"]", password)
        time.sleep(1)
        page.click('text=Submit')
        time.sleep(3)
        test_url = 'https://cryptoquant.com/asset/btc/chart/network-indicator/net-unrealized-profit-loss-nupl?window=DAY&sma=0&ema=0&priceScale=log&metricScale=linear&chartStyle=line'
        page.goto(test_url, wait_until='domcontentloaded', timeout=60000)
        page.get_by_text('All', exact=True).click()
        page.locator('body').press('PageDown')
        time.sleep(3)

        for coin, coin_urls, coin_endpoints in zip(all_coins, all_urls, all_endpoints):
            if coin not in ['BTC', 'ETH', 'STABLECOIN']:
                break
            print(f'Getting data of {coin} from cryptoquant...')
            sub = f'data/{coin}'
            os.makedirs(sub, exist_ok=True)
            print(coin_endpoints)

            for url, name in zip(coin_urls, coin_endpoints):
                page.on("response", handle_response)
                page.goto(url, wait_until="domcontentloaded", timeout=60000)
                time.sleep(1)
                # page.locator('body').press('PageDown')
                coin_files = os.listdir(sub)
                fn = name + '.json'
                while fn not in coin_files:
                    page.reload(wait_until='domcontentloaded', timeout=60000)
                    time.sleep(2)
                    coin_files = os.listdir(sub)
                    if fn in coin_files:
                        break
                time.sleep(random.uniform(3, 7))

        page.context.close()
        browser.close()



if __name__ == '__main__':

    headers = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOiIyMjMyNiIsImlhdCI6MTcwMTE0ODkxOCwiZXhwIjoxNzAxMTUyNTE4fQ.xl075OemHorUIr9iQZalpXuEfwVSg-LnJh6uFB61yns',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        'Referer': 'https://cryptoquant.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
    }

    chrome_path = r'C:\Users\user\Downloads\chromedriver-win32\chromedriver.exe'

    def main(resolution):
        exceptions = []
        coins_list = get_supported_assets()
        coins_list = [c for c in coins_list if c not in exceptions]

        all_coins = []
        all_urls = []
        all_endpoints = []
        for coin in coins_list:
            sub = f'data/{coin}'
            os.makedirs(sub, exist_ok=True)
            coin_param = coin.lower().replace('(', '_').replace(')', '')

            coin_metrics = load_metrics_dict(coin)
            coin_urls = []
            coin_endpoints = []

            files = os.listdir(f'data/{coin}')
            for key in list(coin_metrics.keys()):
                for item in coin_metrics[key]:
                    endpoint = item['name']
                    url = f'https://cryptoquant.com/asset/{coin_param}/chart/{key}/{endpoint}?window={resolution}'
                    f = endpoint + '.json'
                    if f not in files:
                        coin_urls.append(url)
                        coin_endpoints.append(endpoint)

            if len(files) == 0:
                os.removedirs(f'data/{coin}')

            if len(coin_endpoints) > 0 and len(coin_urls) > 0:
                all_coins.append(coin)
                all_urls.append(coin_urls)
                all_endpoints.append(coin_endpoints)

        save_chart_data(all_coins, all_urls, all_endpoints)

    main('DAY')

    # get_btc_exchange_netflow(headers)
    # get_btc_exchange_inflow(headers)
    # get_btc_exchange_outflow(headers)
    # get_btc_top10_exchange_inflow(headers)
    # get_btc_top10_exchange_outflow(headers)
    # get_btc_exchange_reserve(headers)
    # get_btc_exchange_supply_ratio(headers)
    # get_exchange_stablecoins_ratio_usd(headers)
    # get_btc_exchange_whale_ratio(headers)
    # get_btc_est_leverage_ratio(headers)
    # get_btc_short_term_sopr(headers)
    # get_btc_long_term_sopr(headers)
    # get_btc_adjusted_sopr(headers)
    # get_btc_sopr_ratio(headers)
    # get_btc_mvrv_ratio(headers)
    # get_btc_inflow_spent_output_ageband(headers)
    # get_btc_inflow_spent_output_ageband_pct(headers)
    # get_btc_open_interest(headers)
    # get_btc_funding_rates(headers)
    # get_btc_taker_buysell_ratio(headers)
    # get_btc_long_liq_usd(headers)
    # get_btc_short_liq_usd(headers)
    # get_btc_market_cap(headers)
    # get_btc_realized_cap(headers)
    # get_btc_thermo_cap(headers)
    # get_btc_korea_premium(headers)
    # get_btc_coinbase_premium(headers)
    # get_btc_active_addresses(headers)
    # get_btc_fund_volume(headers)
    # get_btc_fund_holdings(headers)
    # get_summary_of_today(chrome_path)
