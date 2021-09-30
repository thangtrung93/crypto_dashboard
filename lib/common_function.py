from datetime import date
import os.path
from selenium import webdriver
import pandas as pd
from sqlalchemy import create_engine


def get_driver_heroku():
    chorme_options = webdriver.ChromeOptions()
    chorme_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chorme_options.add_argument("--headless")
    chorme_options.add_argument("--disable-dev-shm-useage")
    chorme_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chorme_options)
    return driver

def get_driver_chrome():
    driver = webdriver.Chrome(executable_path="D:/Programs/chromedriver_win32/chromedriver.exe")
    return driver


def get_driver_none_img():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("prefs", {
        "profile.managed_default_content_settings.images": 2})  # do not load images to speed up access
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    driver = webdriver.Chrome(executable_path="D:/Programs/chromedriver_win32/chromedriver.exe", options=options)
    return driver


def get_driver():
    option = webdriver.ChromeOptions()

    # Removes navigator webdriver flag
    # For older ChromeDriver under version 79.0.3945.16
    option.add_experimental_option("excludeSwitches", ["enable-automation"])
    option.add_experimental_option('useAutomationExtension', False)

    # For ChromeDriver version 79.0.3945.16 or over
    option.add_argument('--disable-blink-features=AutomationControlled')
    driver = webdriver.Chrome(executable_path="D:/Programs/chromedriver_win32/chromedriver.exe", options=option)
    return driver


def insert_date_column(df, date_value):
    """
    :param df: target dataframe to be added date column
    :param date_value:
    :return: dataframe with new date column
    """
    df['day'] = int(date_value[:2])
    df['month'] = int(date_value[3:5])
    df['year'] = int(date_value[-4:])
    df['date'] = df[['year', 'month', 'day']].apply(lambda x: date(*x), axis=1)
    return df


def create_list(*args):
    return [a for a in args if a is not None]


def join_text(l):
    return '_'.join(l)


def get_l_date(s_date, e_date):
    l_date = pd.date_range(s_date, e_date)
    return l_date


def convert_date_dmy(date_x):
    return date_x.strftime('%d/%m/%Y')


def convert_date_ymd(date_x):
    return date_x.strftime('%Y%m%d')


def get_all_data_condition(folder=None, para=None):
    path = 'D:/OneDrive/Crypto/'+folder + '/'
    # Fetch all files in path
    file_names = os.listdir(path)
    # Filter file name list for files ending with .csv
    if para is not None:
        file_names = [file for file in file_names if para in file]
    else:
        pass
    df_all_data = pd.DataFrame()
    for file in file_names:
        # Read .csv file and append to list
        df_one_file = pd.read_csv(path + file, sep=";")
        df_all_data = df_all_data.append(df_one_file)
    return df_all_data


def get_l_file_condition(folder=None, para=None):
    path = 'D:/OneDrive/Crypto/'+folder + '/'
    # Fetch all files in path
    file_names = os.listdir(path)
    # Filter file name list for files ending with .csv
    if para is not None:
        file_names = [file for file in file_names if para in file]
    else:
        pass
    return file_names


def write_result(df, folder=None, para1=None, para2=None, para3=None):
    l_para = create_list(para1, para2, para3)
    file_name = '_'.join(l_para) + '.csv'
    path_file = 'D:/OneDrive/Crypto/' + folder + '/' + file_name
    if not os.path.isfile(path_file):
        df.to_csv(path_file, sep=';', encoding='utf-8', index=False)
    else:
        pass


def delete_file(folder,  para1=None, para2=None, para3=None):
    l_para = create_list(para1, para2, para3)
    file_name = '_'.join(l_para) + '.csv'
    path = 'D:/OneDrive/Crypto/' + folder + '/' + file_name
    if os.path.isfile(path):
        os.remove(path)
    else:
        pass


def delete_old_version_file(folder=None, para1=None, para2=None):
    l_para = create_list(para1, para2)
    condition = '_'.join(l_para)
    l_file = get_l_file_condition(folder, condition)
    l_sorted_file = sorted(l_file)
    l_sorted_file.reverse()
    newest_file = l_sorted_file[0]
    l_file.remove(newest_file)
    l_file = [x.replace('.csv', '') for x in l_file]
    for file in l_file:
        delete_file(folder, file)


def find_nth(haystack, needle, n):
    """
    find postion of any character in a string in case of character appear many times
    :param haystack: string to find
    :param needle: character need to find position
    :param n: the time of appear
    :return:
    """
    start = haystack.find(needle)
    while start >= 0 and n > 1:
        start = haystack.find(needle, start + len(needle))
        n -= 1
    return start


def get_engine():
    host = "ec2-44-197-94-126.compute-1.amazonaws.com"
    database = "d205k31v0v76jn"
    user = "gqlvygaoovqdfa"
    port = "5432"
    password = "3126632bee48c5cb0959e718425b340b01681bfd1e55a1c18af39238585f84eb"
    database_url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(database_url, echo=False)
    return engine


def get_coin_price_api_url(source):
    if source == "binance":
        base_url = "https://api.binance.com"
        end_point = "/api/v3/klines"
        url = f"{base_url}{end_point}"
    elif source == "mexc":
        base_url = "https://www.mexc.com"
        end_point = "/open/api/v2/market/kline"
        url = f"{base_url}{end_point}"
    return url


