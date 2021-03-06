import lib.common_function as cfunc
import pandas as pd
import time
import lib_dd.dd_coin_price as dd_coin_price
import numpy as np


def get_dashboard(slt_source, current_date):
    # get coin list
    df_coin_list_name = f"df_coin_list_{slt_source}"
    engine = cfunc.get_engine()
    df_coin = pd.read_sql_query(sql=f"select coin, coin_short from {df_coin_list_name}", con=engine)
    l_coin = df_coin["coin"].tolist()
    l_coin.sort()

    # get coin price in the last day
    df_coin_price_previous_name = f"df_coin_price_{slt_source}"
    df_coin_price_previous = pd.read_sql_query(sql=f"select coin, date, price_close, volume from {df_coin_price_previous_name}",
                                               con=engine)

    # get today coin price
    url = cfunc.get_coin_price_api_url(slt_source)

    df = pd.DataFrame()
    if slt_source == "binance":
        for coin in l_coin:
            try:
                df_result = dd_coin_price.get_content_coin_price_binance(url, coin, current_date)
                df = df.append(df_result)
                # print(coin)
                time.sleep(0.00001)
            except:
                pass
    elif slt_source == "mexc":
        for coin in l_coin:
            try:
                df_result = dd_coin_price.get_content_coin_price_mexc(url, coin, current_date)
                df = df.append(df_result)
                # print(coin)
                time.sleep(0.00001)
            except:
                pass

    df_coin_price_current = df[["coin", "date", "price_close", "volume"]].copy()
    df_coin_price_current = df_coin_price_current.append(df_coin_price_previous)
    df_coin_price_sort = df_coin_price_current.sort_values(["coin", "date"]).reset_index(drop=True)
    df_coin_price_sort[["price_close", "volume"]] = df_coin_price_sort[["price_close", "volume"]].astype(float)
    df_coin_price_sort["price_shift_1"] = df_coin_price_sort.groupby(["coin"])["price_close"].shift(1)
    # df_coin_price_sort.fillna(0, inplace=True)

    df_coin_price_tail = df_coin_price_sort.groupby("coin").tail(1).reset_index(drop=True).copy()
    df_coin_price_tail["price_change_1"] = df_coin_price_tail.apply(lambda x: round((x["price_close"] /
                                                                                     x["price_shift_1"] - 1) * 100, 1),
                                                                    axis=1)
    df_coin_price_tail["market_cap"] = df_coin_price_tail["price_close"] * df_coin_price_tail["volume"]
    df_coin_price_tail.fillna(0, inplace=True)
    df_coin_price_tail.replace([np.inf, -np.inf], 0, inplace=True)

    l_col = ["coin", "date", "price_close", "volume", "market_cap", "price_change_1"]
    df_coin_price_result = df_coin_price_tail[l_col].copy()
    df_coin_price_result = df_coin_price_result.merge(df_coin[["coin", "coin_short"]], how="left", on="coin")
    df_coin_price_result.sort_values(["price_change_1"], ascending=False, inplace=True)
    df_coin_price_format = df_coin_price_result.style.format('{:,.0f}', subset=["volume", "market_cap", "price_change_1"])\
        .bar(subset=["price_change_1"], align='mid', color=['#d65f5f', '#5fba7d'])
    return df_coin_price_format
