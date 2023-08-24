
from matplotlib.pyplot import axis
import streamlit as st  
import pandas as pd  
import yfinance as yf  
import datetime  
from datetime import date
from plotly import graph_objs as go  #
from plotly.subplots import make_subplots
from prophet import Prophet  
from prophet.plot import plot_plotly
import time  
from streamlit_option_menu import option_menu  

st.set_page_config(layout="wide", initial_sidebar_state="expanded")

def add_meta_tag():
    meta_tag = """
        <head>
            <meta name="google-site-verification" content="QBiAoAo1GAkCBe1QoWq-dQ1RjtPHeFPyzkqJqsrqW-s" />
        </head>
    """
    st.markdown(meta_tag, unsafe_allow_html=True)


add_meta_tag()


today = date.today()  
st.write('''# StockStream ''') 
st.sidebar.image("StockStream/Images/237e57514b5e59a375c74748a055d4cd-removebg-preview.png", width=250,
                 use_column_width=False)  # logo
st.sidebar.write('''# StockStream ''')
with st.sidebar: 
        selected = option_menu("Utilities", ["Stocks Performance Comparison", "Real-Time Stock Price", "Stock Prediction"])

start = st.sidebar.date_input(
    'Start', datetime.date(2022, 1, 1)) 
end = st.sidebar.date_input('End', datetime.date.today())  


stock_df = pd.read_csv("StockStream/StockData.csv")


if(selected == 'Stocks Performance Comparison'):  
    st.subheader("Stocks Performance Comparison")
    tickers = stock_df["Company Name"]
    dropdown = st.multiselect('Pick your assets', tickers)

    with st.spinner('Loading...'):  # spinner while loading
        time.sleep(2)
        # st.success('Loaded')

    dict_csv = pd.read_csv('StockStream/StockData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  
    for i in dropdown:  
        val = dict_csv.get(i)  
        symb_list.append(val)  

    def relativeret(df):  # function for calculating relative return
        rel = df.pct_change()  # calculate relative return
        cumret = (1+rel).cumprod() - 1  # calculate cumulative return
        cumret = cumret.fillna(0)  # fill NaN values with 0
        return cumret  # return cumulative return

    if len(dropdown) > 0:  # if user selects atleast one asset
        df = relativeret(yf.download(symb_list, start, end))[
            'Adj Close']  # download data from yfinance
        # download data from yfinance
        raw_df = relativeret(yf.download(symb_list, start, end))
        raw_df.reset_index(inplace=True)  # reset index

        closingPrice = yf.download(symb_list, start, end)[
            'Adj Close']  # download data from yfinance
        volume = yf.download(symb_list, start, end)['Volume']
        
        st.subheader('Raw Data {}'.format(dropdown))
        st.write(raw_df)  # display raw data
        chart = ('Line Chart', 'Area Chart', 'Bar Chart')  # chart types
        # dropdown for selecting chart type
        dropdown1 = st.selectbox('Pick your chart', chart)
        with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

        st.subheader('Relative Returns {}'.format(dropdown))
                
        if (dropdown1) == 'Line Chart':  # if user selects 'Line Chart'
            st.line_chart(df)  # display line chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)  # display line chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)  # display line chart

        elif (dropdown1) == 'Area Chart':  # if user selects 'Area Chart'
            st.area_chart(df)  # display area chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.area_chart(closingPrice)  # display area chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.area_chart(volume)  # display area chart

        elif (dropdown1) == 'Bar Chart':  # if user selects 'Bar Chart'
            st.bar_chart(df)  # display bar chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.bar_chart(closingPrice)  # display bar chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.bar_chart(volume)  # display bar chart

        else:
            st.line_chart(df, width=1000, height=800,
                          use_container_width=False)  # display line chart
            # display closing price of selected assets
            st.write("### Closing Price of {}".format(dropdown))
            st.line_chart(closingPrice)  # display line chart

            # display volume of selected assets
            st.write("### Volume of {}".format(dropdown))
            st.line_chart(volume)  # display line chart

    else:  # if user doesn't select any asset
        st.write('Please select atleast one asset')  # display message
# Stock Performance Comparison Section Ends Here
    
# Real-Time Stock Price Section Starts Here
elif(selected == 'Real-Time Stock Price'):  # if user selects 'Real-Time Stock Price'
    st.subheader("Real-Time Stock Price")
    tickers = stock_df["Company Name"]  # get company names from csv file
    # dropdown for selecting company
    a = st.selectbox('Pick a Company', tickers)

    with st.spinner('Loading...'):  # spinner while loading
            time.sleep(2)

    dict_csv = pd.read_csv('StockStream/StockData.csv', header=None, index_col=0).to_dict()[1]  # read csv file
    symb_list = []  # list for storing symbols

    val = dict_csv.get(a)  # get symbol from csv file
    symb_list.append(val)  # append symbol to list

    if "button_clicked" not in st.session_state:  # if button is not clicked
        st.session_state.button_clicked = False  # set button clicked to false

    def callback():  # function for updating data
        # if button is clicked
        st.session_state.button_clicked = True  # set button clicked to true
    if (
        st.button("Search", on_click=callback)  # button for searching data
        or st.session_state.button_clicked  # if button is clicked
    ):
        if(a == ""):  # if user doesn't select any company
            st.write("Click Search to Search for a Company")
            with st.spinner('Loading...'):  # spinner while loading
             time.sleep(2)
        else:  
            data = yf.download(symb_list, start=start, end=end)
            data.reset_index(inplace=True)  
            st.subheader('Raw Data of {}'.format(a))  
            st.write(data) 

            def plot_raw_data(): 
                fig = go.Figure()  
                fig.add_trace(go.Scatter( 
                    x=data['Date'], y=data['Open'], name="stock_open")) 
                fig.add_trace(go.Scatter( 
                    x=data['Date'], y=data['Close'], name="stock_close")) 
                fig.layout.update( 
                    title_text='Line Chart of {}'.format(a) , xaxis_rangeslider_visible=True) 
                st.plotly_chart(fig)  

            def plot_candle_data():  
                fig = go.Figure()  
                fig.add_trace(go.Candlestick(x=data['Date'], 
                                             open=data['Open'],
                                             high=data['High'], 
                                             low=data['Low'], 
                                             close=data['Close'], name='market data')) 
                fig.update_layout(  
                    title='Candlestick Chart of {}'.format(a), 
                    yaxis_title='Stock Price', 
                    xaxis_title='Date') 
                st.plotly_chart(fig) 

            chart = ('Candle Stick', 'Line Chart')  
            dropdown1 = st.selectbox('Pick your chart', chart)
            with st.spinner('Loading...'): 
             time.sleep(2)
            if (dropdown1) == 'Candle Stick':  
                plot_candle_data()  
            elif (dropdown1) == 'Line Chart':  
                plot_raw_data()  
            else: 
                plot_candle_data() 


elif(selected == 'Stock Prediction'):  
    st.subheader("Stock Prediction")

    tickers = stock_df["Company Name"]  
    a = st.selectbox('Pick a Company', tickers)
    with st.spinner('Loading...'):  
             time.sleep(2)
    dict_csv = pd.read_csv('StockStream/StockData.csv', header=None, index_col=0).to_dict()[1]  
    symb_list = []  
    val = dict_csv.get(a)  
    symb_list.append(val)  
    if(a == ""):  
        st.write("Enter a Stock Name") 
    else:  
        data = yf.download(symb_list, start=start, end=end)
        data.reset_index(inplace=True)  
        st.subheader('Raw Data of {}'.format(a))  
        st.write(data)  

        def plot_raw_data():  
            fig = go.Figure()  
            fig.add_trace(go.Scatter( 
                x=data['Date'], y=data['Open'], name="stock_open")) 
            fig.add_trace(go.Scatter(
                x=data['Date'], y=data['Close'], name="stock_close")) 
            fig.layout.update( 
                title_text='Time Series Data of {}'.format(a), xaxis_rangeslider_visible=True) 
            st.plotly_chart(fig) 

        plot_raw_data()  
        n_years = st.slider('Years of prediction:', 1, 4)
        period = n_years * 365 

        
        df_train = data[['Date', 'Close']]
        df_train = df_train.rename(
            columns={"Date": "ds", "Close": "y"})  

        m = Prophet()  
        m.fit(df_train)  
        future = m.make_future_dataframe(
            periods=period) 
        forecast = m.predict(future) 

        # Show and plot forecast
        st.subheader('Forecast Data of {}'.format(a))  
        st.write(forecast)  

        st.subheader(f'Forecast plot for {n_years} years')  
        fig1 = plot_plotly(m, forecast)  
        st.plotly_chart(fig1)  

        st.subheader("Forecast components of {}".format(a))  
        fig2 = m.plot_components(forecast)  
        st.write(fig2)  

