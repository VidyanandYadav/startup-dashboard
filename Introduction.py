import streamlit as st
import pandas as pd

# Titles and text
st.title('Startup Dashboard')
st.header('I am learning Streamlit')
st.subheader('And I am loving it easily')
st.write('This is a normal text')

# Markdown content
st.markdown("""
### My favourite movies
- Race 3
- Tare Zameen Par 
- Uri
""")

# Displaying code
st.code("""
def foo(input):
    return foo*2
x = foo(5)
""")

# Maths rendering
st.latex('x^2+y^2+2=0')

# DataFrame display
df = pd.DataFrame({
    'name':['Nitish','Ankit','Yashna'],
    'marks':[50,60,80],
    'package':[10,12,15]
})
st.dataframe(df)


# Metrix widgets
st.metric('Revenue','Rs 3Lakh','3%')
st.metric('Revenue','Rs 3Lakh','-3%')

# Display JSON
st.json({
    'name': ['Nitish', 'Ankit', 'Yashna'],
    'marks': [50, 60, 80],
    'package': [10, 12, 15]
})

# Media content
st.image('Photo.jpg')
st.video('Video.mp4')
st.audio('Audio.m4a')

# Sidebar
st.sidebar.title('Sidebar ka Title')

# Columns layout
col1 , col2 = st.columns(2)
with col1:
    st.image('Photo.jpg')
with col2:
    st.image('photo(3).jpg')

# Status messages
st.error('Login Failed')
st.success('Login Successfully')
st.info('Login Success')
st.warning('Login Successful')

# Progress bar
bar = st.progress(0)

for i in range(1,101):
    # time.sleep(0.1)
    bar.progress(i)

# Input widgets
email = st.text_input('Enter Email')
number = st.number_input('Enter your age')
st.date_input('Enter registration date')


