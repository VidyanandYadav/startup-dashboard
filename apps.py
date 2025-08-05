import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# reducing the space just after sidebar and by page_title when we load on browser then there will be Startup Analysis showing instead of Streamlit
st.set_page_config(layout="wide",page_title='StartUp Analysis')

# Load data
df = pd.read_csv('startup_cleaned.csv')

df['date'] = pd.to_datetime(df['date'],errors = 'coerce')
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

def load_overall_analysis():
    st.title('Overall Analysis')

    # Total Invested amount
    total = round(df['amount'].sum())
    # maximum amount infused in a startup
    max_funding = df.groupby('startup')['amount'].sum().sort_values(ascending = False).head(1).values[0]
    # average ticket size
    avg_funding = df.groupby('startup')['amount'].sum().mean()
    # Total funded startup
    num_startups = df['startup'].nunique()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        st.metric('Total', str(total) + 'Cr')
    with col2:
        st.metric('Max', str(round(max_funding)) + 'Cr')
    with col3:
        st.metric('Avg',str(round(avg_funding)) + 'Cr')
    with col4:
        st.metric('Funded Startups',num_startups)


    st.header('MoM Graph')
    selected_option = st.selectbox('Select Type',['Total', 'Count'])
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str')+ '_' + temp_df['year'].astype('str')

    # Adding this two line cause on x_axis label year is showing as 1.0_2015.0 and 7.0_2016 for July 2016 etc
    import calendar
    temp_df['x_axis'] = temp_df['month'].apply(lambda x: calendar.month_abbr[int(x)]) + ' ' + temp_df['year'].astype(int).astype(str)


    fig3, ax3 = plt.subplots()
    ax3.plot(temp_df['x_axis'], temp_df['amount'])
    plt.xticks(rotation=45)
    ax3.set_xticks(ax3.get_xticks()[::6])
    st.pyplot(fig3)

def load_investor_details(investor):
    st.title(investor)

    # load the recent 5 investments of the Investor
    last5_df = df[df['investors'].str.contains(investor,na = False)].head()[['date','startup','vertical','city','round','amount']]
    st.subheader('Most Recent Investments')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # biggest Investments
        big_series = df[df['investors'].str.contains(investor, na=False)].groupby('startup')[
            'amount'].sum().sort_values(ascending=False).head()
        st.subheader('Biggest Investments')
        # Plotting graph using matplotlib
        fig, ax = plt.subplots()
        ax.bar(big_series.index, big_series.values)
        st.pyplot(fig)
    with col2:
        vertical_series = df[df['investors'].str.contains(investor,na = False)].groupby('vertical')['amount'].sum()
        st.subheader('Sectors Invested In')
        fig1, ax1 = plt.subplots()
        ax1.pie(vertical_series,labels = vertical_series.index,autopct="%0.01f") # autopct = "%0.01f" is used to show percentage in pie chart
        st.pyplot(fig1)

    df['year'] = df['date'].dt.year
    year_series = df[df['investors'].str.contains(investor, na=False)].groupby('year')['amount'].sum()
    st.subheader('YoY Investment')
    fig2, ax2 = plt.subplots()
    ax2.plot(year_series.index, year_series.values)
    st.pyplot(fig2)

def load_startup_details(startup):
    st.title(startup)
    # Filter data for the selected startup
    startup_df = df[df['startup'].str.contains(startup, case=False, na=False)]


    # 1. Most recent funding rounds
    st.subheader('Most Recent Funding Rounds')
    st.dataframe(startup_df[['date', 'startup', 'vertical', 'city', 'round', 'amount']].head())


    col1, col2 = st.columns(2)
    with col1:
        yearly_funding = startup_df.groupby(startup_df['date'].dt.year)['amount'].sum()
        st.subheader('Yearly Funding Trend')


        fig1, ax1 = plt.subplots()
        ax1.plot(yearly_funding.index, yearly_funding.values,marker = 'o')
        ax1.set_ylabel('Funding Amount (Cr)')
        st.pyplot(fig1)

    with col2:
        # Funding by round type
        round_counts = startup_df.groupby('round')['amount'].sum().sort_values(ascending=False)
        st.subheader('Funding By Round Type')
        fig2, ax2 = plt.subplots()
        ax2.bar(round_counts.index, round_counts.values)
        plt.xticks(rotation = 45)
        st.pyplot(fig2)


    # Top Investors for this Startups
    st.subheader('Top Investors in this Startup')
    investors_list = (
        startup_df['investors']
        .dropna()
        .astype(str)  # Ensure all are strings
        .str.split(',')
        .explode()  # Flatten instead of sum()
        .str.strip()  # Remove whitespace
    )

    investors_series = investors_list.value_counts().head(5)

    fig3, ax3 = plt.subplots()
    ax3.bar(investors_series.index, investors_series.values)
    plt.xticks(rotation = 45)
    st.pyplot(fig3)

# Clean basic whitespace
df['startup'] = df['startup'].astype(str).str.strip()
df['investors'] = df['investors'].astype(str).str.strip()

# Sidebar Title
st.sidebar.title('Startup Funding Analysis')

# Dropdown to select type
option = st.sidebar.selectbox('Select One', ['Overall Analysis', 'Startup', 'Investor'])

# Overall Analysis
if option == 'Overall Analysis':
        load_overall_analysis()

# Startup Analysis
elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select StartUp', sorted(df['startup'].dropna().unique().tolist()))
    btn1 = st.sidebar.button('Find StartUp Details')
    if btn1:
        load_startup_details(selected_startup)
    # st.title('StartUp Analysis')


# Investor Analysis
else:

    # Handle missing values before splitting
    all_investors = df['investors'].dropna().str.split(',').sum()
    unique_investors = sorted(set(i.strip() for i in all_investors if isinstance(i, str)))
    selected_investor = st.sidebar.selectbox('Select Investors', unique_investors)
    btn2 = st.sidebar.button('Find Investor Details')
    if btn2:
        load_investor_details(selected_investor)