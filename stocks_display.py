import streamlit as st
import stocks_data

default_colors = ('#fbfb00', '#fb7c01', '#560056', '#00dcdc', '#02ff0f', '#ff0000', '#0101ff', '#fe6b00', '#EC8DB0', '#7d7c7c')
st.set_page_config(layout='wide')
with st.sidebar:
    ma_input = {}
    options_input = st.text_input('Enter the different lengths of MA (example: 5, 10)', value='5, 10')
    #add option to choose color for stock price
    options = options_input.strip().split(',')
    for i in range(len(options)):
        color_input = st.color_picker(f'Choose a color for the {options[i]} MA', value=default_colors[i])
        ma_input.update({int(options[i]):color_input})


spacer1, content, spacer2 = st.columns([1,8,1])
with content:
    temp = []
    stocks = []
    stocks_input = st.text_input('Enter the stock(s) symbol you would like to see (example: SPY, AMD, TCEHY)', value='SPY, AMD, TCEHY')
    temp = stocks_input.split(',')
    for stock in temp:
        stocks.append(stock.strip())
    st.write(stocks)
    stocks_data.get_data(stocks)
    st.pyplot(fig=stocks_data.multi_plot(stocks, ma_input))


    #TODO
    #add option to choose color for stock price
    #add other technical indicators
    #add a way for users to input their own api key
    #negative coding: input letter instead of number, try except when api calls are maxed
    #stop calling get_data if csv already exists