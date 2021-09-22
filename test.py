import numpy as np
import pandas as pd
import xlwings as xl

import os
from datetime import datetime, date, timedelta



def get_result(sht_name):
    wb = xl.Book.caller()
    sht = wb.sheets(sht_name)

    # set range for first cell of pivot and note tables
    rg_stock = sht.range("stock")
    rg_pivot = sht.range("stock_pivot")

    # get table of stock notes
    df_pivot = rg_pivot.options(pd.DataFrame, index=False, expand="table").value
    df_stock = rg_stock.options(pd.DataFrame, index=False, expand="table").value

    # filter stock belong to df_pivot among with df_stock
    df_stock_filter = df_pivot[['stock']].merge(df_stock, how='left', on='stock')

    # sort df_stock by stock to ensure the position of each stocks in two table is the same
    df_stock_filter.sort_values('stock', inplace=True)

    # paste df_stock_filter into new position of stock table
    rg_stock.expand("table").clear()
    rg_stock.options(index=False).value = df_stock_filter


    ### Paste the result into excel file

    # sht.range('A2').expand('table').clear_contents()
    # sht.range('A2').options(index=False).value  = df_result
    # sht.range('F1').value = str(datetime.today())
    # sht.range('F1').number_format = 'm/d/yyyy h:mm'

if __name__ == '__main__':
    xl.Book('test.xlsm').set_mock_caller()
    xl.Book('test1.xlsm').set_mock_caller()

