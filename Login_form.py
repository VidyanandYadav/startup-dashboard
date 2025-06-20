import streamlit as st
email = st.text_input('Enter Email')
password = st.text_input('Enter password')
gender = st.selectbox('Select Gender',['Male','Female','Others'])

btn = st.button("Login karo")
# If the button is clicked
if btn:
    if email == 'deepuprince91@gmail.com' and password == '9876':
        st.success('Login Successful')
        st.balloons()
        # Dropdown
        st.write(gender)
    else:
        st.error('Login Failead !!')




# File Uploader

