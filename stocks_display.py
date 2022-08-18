import streamlit as st
import stocks_data
import re

default_colors = ('#fbfb00', '#fb7c01', '#560056', '#00dcdc', '#02ff0f', '#ff0000', '#0101ff', '#fe6b00', '#EC8DB0', '#7d7c7c')
st.set_page_config(layout='wide')
with st.sidebar:
    ma_input = {}
    options_input = st.text_input('Enter the different lengths of EMA, (example: 5, 10)', value='5, 10')
    stock_color = st.color_picker('Enter a color for the stock close price', value='#8EA08F')
    if options_input.isspace:
        if options_input[-1] == ',':
            options_input = options_input[0:len(options_input)-1]
        options = options_input.split(',')
        if len(options) < 10:
            for i in range(len(options)):
                if re.match('^[0-9]*$', options[i].strip()):
                    color_input = st.color_picker(f'Choose a color for the {options[i]} EMA', value=default_colors[i])
                    ma_input.update({int(options[i].strip()):color_input})
                else:
                    st.write('You can only input numbers followed by a comma, (example: 5, 10)')
        else:
            st.write('You can only have up to 10 EMA.')

spacer1, content, spacer2 = st.columns([1,6,1])
with content:
    temp = []
    stocks = []
    stocks_input = st.text_input('Enter the stock(s) symbol you would like to see (example: SPY, AMD, TCEHY)', value='SPY, AMD, TCEHY')
    if stocks_input[-1] == ',':
        stocks_input = stocks_input[0:len(stocks_input)-1]
    if re.match('^[A-Z],*$', stocks_input):
        temp = stocks_input.split(',')
        for stock in temp:
            stocks.append(stock.strip())
        stocks_data.check_data(stocks)
        st.pyplot(fig=stocks_data.multi_plot(stocks, ma_input, stock_color))
    else:
        st.write('You can only input valid stock symbols')

    #TODO
    #add other technical indicators
    #negative coding: input letter instead of number, try except when api calls are maxed
    #stop calling get_data if csv already exists
    #using a stock symbol that does not exist
    #adding a display for each stock tab, like volume and other info
    #breaks when user enters in multiple spaces