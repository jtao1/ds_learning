import streamlit as st
import stocks_data
import re

default_colors = ('#fbfb00', '#fb7c01', '#560056', '#00dcdc', '#02ff0f', '#ff0000', '#0101ff', '#fe6b00', '#EC8DB0', '#7d7c7c')
st.set_page_config(layout='wide')

error = False
stocks = []

spacer1, content, spacer2 = st.columns([1,5,1])
with content:
    stocks_input = st.text_input('Enter the stock(s) symbol you would like to see (example: SPY, AMD, TCEHY)', value='SPY, AMD, TCEHY')
    if stocks_input == '' or stocks_input.isspace():
        st.error('You can only input valid stock symbols')
    else:
        try:
            if re.match('^(([\sA-z\s]*)[,]?)*$', stocks_input):
                for stock in stocks_input.split(','):
                    if not (stock == '' or stock.isspace()) and len(stock) <= 6:
                        stocks.append(stock.strip().upper())
                    else: 
                        raise Exception
            else:
                raise Exception
        except Exception:
            error = True
    st.info('This can only be used for educational purposes.')

with st.sidebar:
    stock_color = st.color_picker('Enter a color for the stock close price', value='#8EA08F')
    with st.expander('EMA Customization Options'):
        ema_input = {}
        ema_stock = st.multiselect('Which stocks do you want EMA for:', stocks, stocks)
        options_input = st.text_input('Enter different lengths of EMA, (example: 5, 10)', value='5, 10')
        if options_input == '' or options_input.isspace():
            st.error('Currently not using any EMAs')
        else:
            if re.match('^(([\s0-9\s]+)[,]?)*$', options_input):
                options_input = options_input.rstrip(',')
                options = options_input.split(',')
                if len(options) < 10:
                    for i in range(len(options)):
                        color_input = st.color_picker(f'Choose a color for the {options[i]} EMA', value=default_colors[i])
                        ema_input.update({int(options[i].strip()):color_input})
                else:
                    st.error('You can only have up to 10 EMA.')
            else:
                st.error('You can only input numbers followed by a comma (example: 5, 10)')
    with st.expander('RSI Customization Options'):
        rsi_input = st.multiselect('Which stocks do you want RSI for:', stocks)

with content:
    if not error:
        st.pyplot(fig=stocks_data.plot(stocks, [ema_input, ema_stock], rsi_input, stock_color))
    else:
        st.error('Invalid Stock Error')

#TODO
#add other technical indicators (macd?)
#adding a display for each stock tab, like volume and other info