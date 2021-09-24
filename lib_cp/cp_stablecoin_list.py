from lib import common_function as cfunc
import pandas as pd
import time
import os
import psycopg2

def create_table():

    DATABASE_URL = os.environ['postgres://gqlvygaoovqdfa:3126632bee48c5cb0959e718425b340b01681bfd1e55a1c' \
                              '18af39238585f84eb@ec2-44-197-94-126.compute-1.amazonaws.com:5432/d205k31v0v76jn']

    conn = psycopg2.connect(DATABASE_URL, sslmode='require')

    cursor = conn.cursor()

    # Creating table as per requirement
    sql = '''CREATE TABLE EMPLOYEE(
       FIRST_NAME CHAR(20) NOT NULL,
       LAST_NAME CHAR(20),
       AGE INT,
       SEX CHAR(1),
       INCOME FLOAT
    )'''

    cursor.execute(sql)
    print("Table created successfully........")
    conn.commit()
    # Closing the connection
    conn.close()

def get_stablecoin_list_binance():
    create_table()
    l_stablecoin = ["BNB", "BTC"]

    url = "https://www.binance.com/en/markets"
    driver = cfunc.get_driver_heroku()
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
