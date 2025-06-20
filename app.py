import streamlit as st
import pandas as pd

df = pd.read_csv('startup_cleaned.csv')

st.sidebar.title('Startup Funding Analysis')

option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
elif option == 'StartUp':
    st.sidebar.selectbox('Select StartUp',sorted(df['startup'].unique().tolist()))
    btn2 = st.sidebar.button('Find Investor Analysis')
    st.title('StartUp Analysis')
else:
     st.sidebar.selectbox('Select StartUp',sorted(set(df['investors'].str.split(',').sum())))
     btn2 = st.sidebar.button('Find Investor Analysis')
     st.title('Investor Analysis')