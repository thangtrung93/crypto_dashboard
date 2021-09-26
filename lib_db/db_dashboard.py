import lib.common_function as cfunc
import pandas as pd
from datetime import date, datetime, timedelta
import time
import cryptocompare as cc
from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pytz
import requests


def dashboard(slt_source):
    # get coin list
    df_coin_list_name = f"df_coin_list_{slt_source}"
    engine = cfunc.get_engine()
    df_coin_list = pd.read_sql_query(sql=f"select coin, coin_short from {df_coin_list_name}", con=engine)
