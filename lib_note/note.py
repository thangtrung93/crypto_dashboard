import streamlit as st


# note for first-reading
def get_note():
    st.markdown(
        """ 
## Dashboard Processing

**1. Binance:**

Get stablecoin -> coin list -> update last coin price via Daily Data tab -> update current dashboard
        
**2. Mexc:**

Get coin list -> update last coin price via Daily Data tab -> update current dashboard
        """,
        unsafe_allow_html=True
    )
