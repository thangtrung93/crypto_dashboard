import lib.common_function as cfunc
import pandas as pd
from datetime import date, datetime, timedelta
import time
import cryptocompare as cc
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pytz
import requests


# binance
def get_content_coin_price_binance(url, coin, date_target):
    date_x = datetime.combine(date_target, datetime.min.time())
    date_epoch = int(pytz.utc.localize(date_x, is_dst=False).timestamp())*1000

    params = {'symbol': coin, 'interval': "1d", "endTime": str(date_epoch), "limit": "1"}
    response = requests.get(url, params=params).json()[0]

    d_coin_price = dict()
    d_coin_price.update({
        "coin": coin,
        "date": date_target.strftime('%Y%m%d'),
        "price_close": response[4],
        "volume": response[5]
        })

    df_coin_price = pd.DataFrame(d_coin_price, index=[0, ])
    return df_coin_price


def get_coin_price_binance(slt_source, l_date):
    # url
    base_url = "https://www.binance.com"
    end_point = "/api/v3/klines"
    url = f"{base_url}{end_point}"

    # get coin list
    df_coin = pd.read_csv("D:/OneDrive/Crypto/a_data_common_parameter/coin_list/coin_list_binance.csv", sep=";")
    l_coin = df_coin["coin"].tolist()
    l_coin.sort()

    for date_target in l_date:
        df = pd.DataFrame()
        for coin in l_coin:
            try:
                df_result = get_content_coin_price_binance(url, coin, date_target)
                df = df.append(df_result)
                print(coin)
                time.sleep(0.00001)
            except:
                pass

        folder = "a_data_daily_coin_price/" + slt_source
        file_name = "stock_price_" + str(date_target.strftime('%Y%m%d'))
        print(date_target)

        cfunc.delete_file(folder=folder, para1=file_name)
        cfunc.write_result(df, folder, file_name)


def get_content_coin_price_binance_v1(client, coin, date_target):
    d_coin_price = dict()
    d_coin_price.update({
        "coin": coin,
        "date": date_target.strftime('%Y%m%d'),
        "price_close": client.get_historical_klines(coin, client.KLINE_INTERVAL_1DAY
                                                    , date_target.strftime("%Y/%m/%d"))[0][4],
        "volume": client.get_historical_klines(coin, client.KLINE_INTERVAL_1DAY,
                                               date_target.strftime("%Y/%m/%d"))[0][5]
        })

    df_coin_price = pd.DataFrame(d_coin_price, index=[0, ])
    return df_coin_price


def get_coin_price_binance_v1(slt_source, l_date):
    # get coin list
    df_coin = pd.read_csv("D:/OneDrive/Crypto/a_data_common_parameter/coin_list/coin_list_binance.csv", sep=";")
    l_coin = df_coin["coin"].tolist()
    l_coin.sort()

    # get client
    api_key = "DA59ac1n2dIZui2nDVnRUb7Jc8QOuqyRdTNncBxcZ0MYFmx2VwzmgAcWSLJ2Edx3"
    api_secret = "olCFcNF9hiwNcCIJxXU6xa52wAcvmIalKDDUTDTJzW2K4w7REJo07P03jRqm4WCS"
    client = Client(api_key, api_secret)

    for date_target in l_date:

        df = pd.DataFrame()
        for coin in l_coin:
            try:
                df_result = get_content_coin_price_binance_v1(client, coin, date_target)
                df = df.append(df_result)
                print(coin)
                time.sleep(0.00001)
            except:
                pass

        folder = "a_data_daily_coin_price/" + slt_source
        file_name = "stock_price_" + str(date_target.strftime('%Y%m%d'))
        print(date_target)

        cfunc.delete_file(folder=folder, para1=file_name)
        cfunc.write_result(df, folder, file_name)


# mexc
def get_content_coin_price_mexc(url, coin, date_target):
    date_x = datetime.combine(date_target, datetime.min.time())
    date_epoch = int(pytz.utc.localize(date_x, is_dst=False).timestamp())

    params = {'symbol': coin, 'interval': "1d", "start_time": str(date_epoch)}
    response = requests.get(url, params=params).json()["data"][0]

    d_coin_price = dict()
    d_coin_price.update({
        "coin": coin,
        "date": date_target.strftime('%Y%m%d'),
        "price_close": response[2],
        "volume": response[5]
        })

    df_coin_price = pd.DataFrame(d_coin_price, index=[0, ])
    return df_coin_price


def get_coin_price_mexc(slt_source, l_date):
    # url
    base_url = "https://www.mexc.com"
    end_point = "/open/api/v2/market/kline"
    url = f"{base_url}{end_point}"

    # get coin list
    engine = cfunc.get_engine()
    df_coin_list_name = f"df_coin_list_{slt_source}"
    df_coin = pd.read_sql_query(sql=f"select coin, coin_short from {df_coin_list_name}", con=engine)
    # df_coin = pd.read_csv("D:/OneDrive/Crypto/a_data_common_parameter/coin_list/coin_list_mexc.csv", sep=";")
    l_coin = df_coin["coin"].tolist()
    l_coin.sort()

    for date_target in l_date:
        df = pd.DataFrame()
        for coin in l_coin:
            try:
                df_result = get_content_coin_price_mexc(url, coin, date_target)
                df = df.append(df_result)
                print(coin)
                time.sleep(0.00001)
            except:
                pass

        df.to_sql("df_coin_price_mexc", con=engine, if_exists='replace')
        engine.execute("alter table df_coin_price_mexc add primary key(coin)")


# cryptocompare
def get_content_coin_price_cryptocompare(coin, date_target):
    date_x = date_target+timedelta(1)

    d_coin_price = dict()
    d_coin_price.update({
        "coin": coin,
        "date": date_target.strftime('%Y%m%d'),
        "price_close": cc.get_historical_price_day(coin, "USDT", limit=1, toTs=date_x)[1]["close"]
        })

    df_coin_price = pd.DataFrame(d_coin_price, index=[0, ])
    return df_coin_price


def get_coin_price_cryptocompare(slt_source, l_date):
    df_coin = pd.read_csv("D:/OneDrive/Crypto/a_data_common_parameter/coin_list/coin_list_cryptocompare.csv", sep=";")

    l_coin = df_coin["coin"].tolist()

    l_coin.sort()

    for date_target in l_date:

        df = pd.DataFrame()
        for coin in l_coin:
            try:
                df_result = get_content_coin_price_cryptocompare(coin, date_target)
                df = df.append(df_result)
                print(coin)
                time.sleep(0.001)
            except:
                pass

        folder = "a_data_daily_coin_price/" + slt_source
        file_name = "stock_price_" + str(date_target.strftime('%Y%m%d'))
        print(date_target)

        cfunc.delete_file(folder=folder, para1=file_name)
        cfunc.write_result(df, folder, file_name)

