import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import math
import numpy as np
import process_data

@st.cache
def import_data(file):
    df = pd.read_csv(file, delimiter=";", index_col='Scan Time Stamp')
    df.index = pd.to_datetime(df.index)
    print(df.index)
    return df

st.write("""
# The accelerated experiments application for UCT Prague

In this application, the user can upload data from accelerated experiments and generate a corrosion profile over the testing time.

Please carefully check the parameters in the left channel of the UI!!
""")

# ---------------------------------#
# Sidebar - Collects the raw input data from the accelerated experiment into a dataframe
with st.sidebar.header('1. Upload your data'):
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file", type=["csv"])

# Sidebar - select the reference channel
with st.sidebar.header('2. Select your reference channel'):
    if uploaded_file is not None:
        df = import_data(uploaded_file)
        columns = df.columns
        reference_channel = st.sidebar.selectbox('Select the reference channel used', columns)

# Sidebar - Select the other channels that need to be examined
with st.sidebar.header('3. Select your reference channel'):
    if uploaded_file is not None:
        columns_1 = columns.drop(reference_channel)
        other_channels = st.sidebar.multiselect('Select the other channels to be examined', columns_1)

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
        # amount_of_immersions = st.sidebar.number_input('How many times are the samples immersed per week ?', value=2)
        # immersion_time = st.sidebar.number_input('What is the duration of the immersion time (min) ?', value=15)
        # spraying_time = st.sidebar.number_input('What is the duration of the spraying time (min) ?', value=105)
        # repeated_times = st.sidebar.number_input('How many times are these steps repeated ?', value=3)

    else:
        temperature = st.sidebar.number_input('What is the temperature (°C) ?', step=1)
        rh_lower = st.sidebar.slider('What is the lower RH boundary (%) ?', 50, 100, 10, 5)
        rh_higher = st.sidebar.slider('What is the higher RH boundary (%) ?', 95, 100, 10, 5)
        dyring_wetting_time = st.sidebar.number_input('What is the duration of drying/wetting phase (hours) ?', step=1)
        # amount_of_immersions = st.sidebar.number_input('How many times are the samples immersed per week ?', step=1)
        # immersion_time = st.sidebar.number_input('What is the duration of the immersion time (min) ?', step=1)
        # spraying_time = st.sidebar.number_input('What is the duration of the spraying time (min) ?', step=1)
        # repeated_times = st.sidebar.number_input('How many times are these steps repeated ?', step=1)

st.subheader('1. Dataset')

if uploaded_file is not None:
    st.markdown('**1.1. Glimpse of dataset**')
    channel_columns = list(other_channels)
    channel_columns.append(reference_channel)
    data = df.loc[:, df.columns.intersection(channel_columns)]
    data.rename({reference_channel: 'REF'}, axis=1, inplace=True)
    data['minutes'] = np.round((data.index - data.index[0]).total_seconds() / 60)
    data['hours'] = data['minutes'] / 60
    st.write(data)
    start_process = st.button('Start the data processing')
    if start_process:
        process_data.data_processing(data, thickness, width, other_channels)
else:
    st.info('Awaiting for excel file to be uploaded.')
