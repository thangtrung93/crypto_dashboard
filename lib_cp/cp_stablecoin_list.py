from lib import common_function as cfunc
import pandas as pd
import time


def get_stablecoin_list_binance():
    l_stablecoin = ["BNB", "BTC"]

    url = "https://www.binance.com/en/markets"
    driver = cfunc.get_driver_none_img()
    driver.get(url)
    time.sleep(1)

    driver.find_element_by_id("market_filter_spot_ALTS").click()
    time.sleep(1)
    for alt_coin in driver.find_elements_by_xpath('//*[contains(@id, "market_3rd_filter_ALTS")]'):
        l_stablecoin.append(alt_coin.text)

    driver.find_element_by_id("market_filter_spot_FIAT").click()
    time.sleep(1)
    for fiat_coin in driver.find_elements_by_xpath('//*[contains(@id, "market_3rd_filter_FIAT")]'):
        l_stablecoin.append(fiat_coin.text)

    l_stablecoin_result = [i for i in l_stablecoin if i != "All"]

    df_stablecoin = pd.DataFrame(l_stablecoin_result, columns=["stablecoin"])
    driver.quit()

    cfunc.delete_file("a_data_common_parameter/stablecoin_list", "stablecoin_list_binance")
    cfunc.write_result(df_stablecoin, "a_data_common_parameter/stablecoin_list", "stablecoin_list_binance")
