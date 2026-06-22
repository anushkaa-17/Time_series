import streamlit as st

st.set_page_config(
    page_title = "Trading App",
    page_icon = "heavy_dollar_sign:",
    layout = "wide"
)
st.title("Trading Guide App :bar_chart:")
st.header("We provide a platform for you to analyse a stock before you choose to invest in it.")

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.image("app.png")

st.markdown("## We provide the following services:")

# Create a 2-column layout
col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown("#### 📊 Stock Information")
        st.write("Explore all the information about historical performance for any selected stock.")
        

with col2:
    with st.container(border=True):
        st.markdown("#### 🔮 Stock Prediction")
        st.write("Explore predicted closing prices for the next 30 days for any selected stock.")
        