import streamlit as st
import stocks_data
import re

default_colors = ('#fbfb00', '#fb7c01', '#560056', '#00dcdc', '#02ff0f', '#ff0000', '#0101ff', '#fe6b00', '#EC8DB0', '#7d7c7c')
st.set_page_config(layout='wide')

with st.sidebar:
    stock_color = st.color_picker('Enter a color for the stock close price', value='#8EA08F')
    with st.expander('EMA Customization Options'):
        ema_input = {}
        options_input = st.text_input('Enter different lengths of EMA, (example: 5, 10)', value='5, 10')
        if options_input == '' or options_input.isspace():
            st.error('Currently not using any EMAs')
        else:
            if re.match('^(([\s0-9\s]+)[,]?)*$', options_input):
                if options_input[-1] == ',':
                    options_input = options_input[0:len(options_input)-1],
                options = options_input.split(',')
                if len(options) < 10:
                    for i in range(len(options)):
                        color_input = st.color_picker(f'Choose a color for the {options[i]} EMA', value=default_colors[i])
                        ema_input.update({int(options[i].strip()):color_input})
                else:
                    st.error('You can only have up to 10 EMA.')
            else:
                st.error('You can only input numbers followed by a comma (example: 5, 10)')
        st.info('Leave the ')
    with st.expander('RSI Customization Options'):
        rsi_input = st.text_input('Enter RSI')
spacer1, content, spacer2 = st.columns([1,5,1])
with content:
    temp = []
    stocks = []
    stocks_input = st.text_input('Enter the stock(s) symbol you would like to see (example: SPY, AMD, TCEHY)', value='SPY, AMD, TCEHY')
    #stocks_input = stocks_input.strip()
    if stocks_input == '' or stocks_input.isspace():
        st.error('You can only input valid stock symbols')
    else:
        if re.match('^(([\saA-zZ\s]*)[,]?)*$', stocks_input):
            temp = stocks_input.split(',')
            #condense!!!!
            try:
                for stock in temp:
                    if len(stock) > 6:
                        raise Exception
                    if not (stock == '' or stock.isspace()):
                        stocks.append(stock.strip().upper())
            except Exception:
                st.error('Invalid Stock Error')
            try:
                if len(stocks) == 1:
                    st.pyplot(fig=stocks_data.single_plot(stocks, ema_input, stock_color))
                else:
                    st.pyplot(fig=stocks_data.multi_plot(stocks, ema_input, stock_color))
            except Exception:
                st.error('Invalid Stock Error')
        else:
            st.error('You can only input valid stock symbols')
    st.info('This can only be used for educational purposes.')

    #TODO
    #add other technical indicators
    #reformat code in stocks_display single/multi plot very messy and can broken up into different functions 
    #adding a display for each stock tab, like volume and other info