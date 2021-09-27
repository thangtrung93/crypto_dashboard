from lib import common_function as cfunc
import pandas as pd
import time
import streamlit as st


def get_stablecoin_list_binance():
    # create_table()
    l_stablecoin = ["BNB", "BTC"]

    url = "https://www.binance.com/en/markets"
    driver = cfunc.get_driver_heroku()
    driver.get(url)
    time.sleep(1)

    driver.find_element_by_id("tab-ALTS").click()
    time.sleep(1)
    for alt_coin in driver.find_elements_by_xpath('//*[contains(@id, "market_3rd_filter_ALTS")]'):
        l_stablecoin.append(alt_coin.text)

    driver.find_element_by_id("tab-FIAT").click()
    time.sleep(1)
    for fiat_coin in driver.find_elements_by_xpath('//*[contains(@id, "market_3rd_filter_FIAT")]'):
        l_stablecoin.append(fiat_coin.text)

    l_stablecoin_result = [i for i in l_stablecoin if (not i in ["", "All"])]

    df_stablecoin = pd.DataFrame(l_stablecoin_result, columns=["stablecoin"])
    driver.quit()

    st.table(df_stablecoin)

    engine = cfunc.get_engine()
    df_stablecoin.to_sql("df_stablecoin", con=engine, if_exists='replace')
    # cfunc.delete_file("a_data_common_parameter/stablecoin_list", "stablecoin_list_binance")
    # cfunc.write_result(df_stablecoin, "a_data_common_parameter/stablecoin_list", "stablecoin_list_binance")
