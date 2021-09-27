import streamlit as st
from datetime import datetime, date, timedelta
import lib.common_function as cfunc
import lib_dd.dd_coin_price as dd_coin_price
import lib_cp.cp_coin_list as cp_coin_list
import lib_cp.cp_stablecoin_list as cp_stablecoin_list
from PIL import Image
import lib_db.db_dashboard as db_dashboard
import time


# @st.echo
d_menu = {"common_parameter": "Common Parameter",
          "daily_data": "Daily Data",
          "dashboard": "Dashboard"
          }

opt_daily_data = ["coin_price"]
opt_common_parameter = ["coin_list", "stablecoin_list"]
opt_source = ["binance", "mexc", "cryptocompare"]

# img = Image.open("D:/OneDrive/Crypto/Cardano.ico")
# st.set_page_config(page_icon=img)


def main():

    st.sidebar.title("Menu")
    menu = st.sidebar.radio("Go to", list(d_menu.values()))

    # common parameter
    if menu == d_menu['common_parameter']:
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

    # daily data
    elif menu == d_menu['daily_data']:
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


    # dashboard
    elif menu == d_menu['dashboard']:
        st.markdown('<h1 style="font-weight:bold">{}</h1>'.format(d_menu['dashboard']), unsafe_allow_html=True)
        current_date = date.today()
        st.text("Today: " + current_date.strftime("%Y/%m/%d"))
        slt_source = st.selectbox(label="Select Source", options=opt_source)

        bt_run = st.button("Run")
        st_current_time = st.empty()
        st_table = st.empty()
        if bt_run:
            for i in range(2):
                current_time = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
                st_current_time.text(f"update at: {current_time}, id: {str(i)}")
                df_coin_price_result = db_dashboard.get_dashboard(slt_source, current_date)
                st_table.table(df_coin_price_result)
                time.sleep(60)


if __name__ == '__main__':
    main()
