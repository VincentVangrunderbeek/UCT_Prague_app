import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1.5
import streamlit as st
import pandas as pd

def temperature_RH(df, T, L_RH, H_RH, drying_time):
    times = [96, 72, 96, 72]
    df['RH'] = H_RH
    time_passed = 0
    for time in times:
        # we devide by two because the measuring interval is 2 minutes with their accelerated experiments set-up
        minutes = time * 60 / 2
        df['RH'].iloc[time_passed + 0:time_passed + 180] = H_RH
        df['RH'].iloc[time_passed + 300:time_passed + 360] = L_RH
        minute = time_passed + 390
        while minute < minutes:
            for i in range(drying_time*30):
                df['RH'].iloc[minute] = H_RH
                minute = minute + 1

            minute = minute + 60
            for i in range(drying_time*30):
                df['RH'].iloc[minute] = L_RH
                minute = minute + 1

        time_passed = time * 30

def data_processing(df, thickness, width, channels_columns_no_ref):
    fig, ax = plt.subplots(figsize=(12, 8))
    for column in channels_columns_no_ref:
        column_name = column + ' thickness loss (µm)'
        df[column_name] = 0.0
        resistance_correction = float(1 - (df['REF'].iloc[0] / df[column].iloc[0]))
        for i in range(len(df) - 1):
            if df[column_name][i] >= 0:
                correction = df[column_name][i]
            else:
                correction = 0

            df[column_name][i + 1] = thickness * width * (
                        resistance_correction + df['REF'][i + 1] / df[column][i + 1])
            df[column_name][i + 1] = thickness - np.sqrt(
                (df[column_name][i + 1]) / ((width - 2 * correction) / (thickness - correction)))

        column_30MA = column_name + '30MA'
        df[column_30MA] = df[column_name].rolling(30, min_periods=1).mean()
        ax.plot(df['hours'], df[column_name])
        ax.plot(df['hours'], df[column_30MA], linewidth=2, label='Sample channel ' + column)
        ax.set_title('Thickness loss of a ' + str(thickness) + ' micron Fe substrate', fontsize=20)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        ax.set_xlabel('Hours', fontsize=20)
        ax.set_ylabel('Thickness loss (µm)', fontsize=20)
        ax.legend(fontsize=15)

    st.pyplot(fig)

