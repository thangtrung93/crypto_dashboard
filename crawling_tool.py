import streamlit as st
from datetime import date, timedelta
import lib.common_function as cfunc
import lib_dd.dd_coin_price as dd_coin_price
import lib_cp.cp_coin_list as cp_coin_list
import lib_cp.cp_stablecoin_list as cp_stablecoin_list
from PIL import Image

# @st.echo
d_menu = {"daily_data": "Daily Data",
          "common_parameter": "Common Parameter"
          }

opt_daily_data = ["coin_price"]
opt_common_parameter = ["coin_list", "stablecoin_list"]
opt_source = ["binance", "mexc", "cryptocompare"]

# img = Image.open("D:/OneDrive/Crypto/Cardano.ico")
# st.set_page_config(page_icon=img)


def main():

    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Go to", list(d_menu.values()))

    # daily data
    if menu == d_menu['daily_data']:
        st.markdown("<h1 style='font-weight:bold'>{}</h1>".format(d_menu['daily_data']+" Crawling"), unsafe_allow_html=True)
        col1, col2, col3 = st.columns([2, 2, 3])
        with col1:
            slt_tag = st.selectbox(label="Select Tag", options=opt_daily_data)
        with col2:
            slt_source = st.selectbox(label="Select Source", options=opt_source)
        with col3:
            slt_date = st.date_input("Select Date Range", value=(date.today()-timedelta(1), date.today()-timedelta(1)))

        bt_download = st.button("Download")
        s_date = slt_date[0]
        e_date = slt_date[1]
        l_date = cfunc.get_l_date(s_date, e_date)

        if slt_tag == 'coin_price':
            if bt_download:
                if slt_source == "binance":
                    dd_coin_price.get_coin_price_binance(slt_source, l_date)
                    st.write('success')
                elif slt_source == "mexc":
                    dd_coin_price.get_coin_price_mexc(slt_source, l_date)
                    st.write('success')
                elif slt_source == "cryptocompare":
                    dd_coin_price.get_coin_price_cryptocompare(slt_source, l_date)
                    st.write('success')

    # common parameter
    elif menu == d_menu['common_parameter']:
        st.markdown('<h1 style="font-weight:bold">{}</h1>'.format(d_menu['common_parameter']+" Crawling"), unsafe_allow_html=True)
        slt_tag = st.selectbox(label="Select Tag", options=opt_common_parameter)

        if slt_tag == "coin_list":
            slt_source = st.selectbox(label="Select Source", options=opt_source)
            bt_download = st.button("Download")
            if bt_download:
                if slt_source == "binance":
                    cp_coin_list.get_coin_list_binance()
                elif slt_source == "mexc":
                    cp_coin_list.get_coin_list_mexc()
                elif slt_source == "cryptocompare":
                    cp_coin_list.get_coin_list_cryptocompare()

        elif slt_tag == "stablecoin_list":
            slt_source = st.selectbox(label="Select Source", options=opt_source)
            bt_download = st.button("Download")
            if bt_download:
                if slt_source == "binance":
                    cp_stablecoin_list.get_stablecoin_list_binance()


if __name__ == '__main__':
    main()
