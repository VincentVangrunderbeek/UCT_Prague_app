import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np

def import_data(file):
    df = pd.read_csv(file, delimiter=';', parse_dates=['Scan Time Stamp'], index_col='Scan Time Stamp')


st.write("""
# The Machine Learning App

In this implementation, A *LSTM deep learning network* from the Keras library is used to build a supervised machine learning regression model that is able to predict the ACM current from temperature and relative humidity input data. 

Try adjusting the hyperparameters!
""")

# ---------------------------------#
# Sidebar - Collects the raw input data from the accelerated experiment into a dataframe
with st.sidebar.header('1. Upload your data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

# Sidebar - select the reference channel
with st.sidebar.header('2. Select your reference channel'):
    reference_channel = st.sidebar.selectbox('Select the reference channel used', [1, 2, 3])

# Sidebar - Select the other channels that need to be examined
with st.sidebar.header('3. Select your reference channel'):
    other_channels = st.sidebar.selectbox('Select the other channels to be examined', [1, 2, 3])

# Sidebar - Specify parameter settings
with st.sidebar.header('3. Set Parameters'):
    thickness = st.sidebar.number_input('What is the thickness of the sample (μm)', step=1)
    width = st.sidebar.number_input('What is the width of the sample (μm)', step=1)

with st.sidebar.header('4. Temperature and relative humidity settings'):
    iso_check = st.sidebar.checkbox('Does the temperature and relative humidity follow the ISO 16701 standard?')
    my_range = range(10, 100, 5)
    if iso_check:
        temperature = st.sidebar.number_input('What is the temperature (°C) ?', value=35)
        rh_lower = st.sidebar.slider('What is the lower RH boundary (%) ?', value=50, step=5)
        rh_higher = st.sidebar.slider('What is the higher RH boundary (%) ?', value=95, step = 5)
        dyring_wetting_time = st.sidebar.number_input('What is the duration of drying/wetting phase (hours) ?', value=4)
        amount_of_immersions = st.sidebar.number_input('How many times are the samples immersed per week ?', value=2)
        immersion_time = st.sidebar.number_input('What is the duration of the immersion time (min) ?', value=15)
        spraying_time = st.sidebar.number_input('What is the duration of the spraying time (min) ?', value=105)
        repeated_times = st.sidebar.number_input('How many times are these steps repeated ?', value=3)

    else:
        temperature = st.sidebar.number_input('What is the temperature (°C) ?', step=1)
        rh_lower = st.sidebar.slider('What is the lower RH boundary (%) ?', 50, 100, 10, 5)
        rh_higher = st.sidebar.slider('What is the higher RH boundary (%) ?', 95, 100, 10, 5)
        dyring_wetting_time = st.sidebar.number_input('What is the duration of drying/wetting phase (hours) ?', step=1)
        amount_of_immersions = st.sidebar.number_input('How many times are the samples immersed per week ?', step=1)
        immersion_time = st.sidebar.number_input('What is the duration of the immersion time (min) ?', step=1)
        spraying_time = st.sidebar.number_input('What is the duration of the spraying time (min) ?', step=1)
        repeated_times = st.sidebar.number_input('How many times are these steps repeated ?', step=1)

st.subheader('1. Dataset')

if uploaded_file is not None:
    df = import_data(uploaded_file)
    st.markdown('**1.1. Glimpse of dataset**')
    st.write(df)
else:
    st.info('Awaiting for excel file to be uploaded.')
