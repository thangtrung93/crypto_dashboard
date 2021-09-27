from lib import common_function as cfunc
import re
import pandas as pd
import requests
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager


# get stock list
def convert_col_name(col_name):
    return '_'.join(re.findall('[A-Z][a-z]*', col_name)).lower()


def get_coin_list_binance():
    api_key = "DA59ac1n2dIZui2nDVnRUb7Jc8QOuqyRdTNncBxcZ0MYFmx2VwzmgAcWSLJ2Edx3"
    api_secret = "olCFcNF9hiwNcCIJxXU6xa52wAcvmIalKDDUTDTJzW2K4w7REJo07P03jRqm4WCS"
    client = Client(api_key, api_secret)
    l_coin_list = client.get_all_tickers()
    df_coin_list = pd.DataFrame(l_coin_list)[["symbol"]].rename(columns={"symbol": "coin"})

    # short coin name
    engine = cfunc.get_engine()
    df_stablecoin_list = pd.read_sql_query("select * from df_stablecoin")
    l_stablecoin = df_stablecoin_list["stablecoin"].tolist()

    df_coin_list["check"] = df_coin_list["coin"].apply(lambda x: [x[-3:]] + [x[-4:]])
    df_coin_list["check_common"] = df_coin_list["check"].apply(
        lambda x: "" if not list(set(x).intersection(l_stablecoin)) else list(set(x).intersection(l_stablecoin))[0])
    df_coin_list["coin_short"] = df_coin_list.apply(lambda x: x["coin"].replace(x["check_common"], ""), axis=1)
    df_coin_list_result = df_coin_list[["coin", "coin_short"]].copy()

    # write result
    # cfunc.delete_file("a_data_common_parameter/coin_list", "coin_list_binance")
    # cfunc.write_result(df_coin_list_result, "a_data_common_parameter/coin_list", "coin_list_binance")

    df_coin_list.to_sql("df_coin_list_binance", con=engine, if_exists='replace')
    engine.execute("alter table df_coin_list_binance add primary key(coin)")


def get_coin_list_mexc():
    base_url = "https://www.mexc.com"
    end_point = "/open/api/v2/market/symbols"
    url = f"{base_url}{end_point}"

    response = requests.get(url).json()
    df_coin_list = pd.DataFrame(response["data"])
    df_coin_list.rename(columns={"symbol": "coin", "vcoinName": "coin_short"}, inplace=True)

    # write result
    # cfunc.delete_file("a_data_common_parameter/coin_list", "coin_list_mexc")
    # cfunc.write_result(df_coin_list, "a_data_common_parameter/coin_list", "coin_list_mexc")

    engine = cfunc.get_engine()
    df_coin_list.to_sql("df_coin_list_mexc", con=engine, if_exists='replace')
    engine.execute("alter table df_coin_list_mexc add primary key(coin)")

