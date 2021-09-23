import streamlit as st
from typing import List, Optional
import markdown
from datetime import date, timedelta
import pandas as pd


# @st.echo
d_menu = {"daily_data": "Daily Data",
          "common_parameter": "Common Parameter",
          "financial_statement": "Financial Statement",
          "download_file": "Download File"
          }
opt_daily_data = ['stock_price', 'VNINDEX', 'foreign_trade', 'bid_ask']
opt_common_parameter = ['ticker_list', 'industry_classification', 'company_name', "key_shareholders"]
opt_financial_statement = ['balance_sheet', 'income', 'cash_flow_indirect', 'cash_flow_direct']
opt_stock_exchange = ['HOSE', 'HASTC', 'UPCOM']
opt_source = {"ticker_list": ["SSI"], "industry_classification": ["stockbiz"], "company_name": ["cafef"],
              "key_shareholders": ["stockbiz"]
              }
opt_source_fs = ['cafef']
opt_source_document = ["vietstock", "cafef"]

opt_type = ['year', 'quarter']
opt_quarter = {'quarter': [1, 2, 3, 4], 'year': [0]}

opt_document = ["financial_statement",
                "annual_report",
                "meeting_resolution",
                "meeting_document"]

opt_source_report = ["fpts", "cafef"]


def main():
    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Go to", list(d_menu.values()))

    # daily data
    if menu == d_menu['daily_data']:
        st.markdown("<h1 style='font-weight:bold'>{}</h1>".format(d_menu['daily_data']+" Crawling"), unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            slt_tag = st.selectbox(label="Select Tag", options=opt_daily_data)
        with col2:
            slt_date = st.date_input("Select Date Range", value=(date.today()-timedelta(1), date.today()-timedelta(1)))
        with col3:
            slt_stock_exchange = st.selectbox(label="Stock Exchange", options=opt_stock_exchange)


if __name__ == '__main__':
    main()
