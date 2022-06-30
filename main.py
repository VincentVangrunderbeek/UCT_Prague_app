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
    thickness = st.sidebar.number_input('What is the thickness of the sample (μm)')
    width = st.sidebar.number_input('What is the width of the sample (μm)')

