import numpy as np
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
plt.rcParams['lines.linewidth'] = 1.5
import streamlit as st
import pandas as pd

def temperature_RH(df, T, RH, L_RH, H_RH, drying_time, times_immeresed, immersion_time, spraying_time, times_cycles):
    days = [4, 3, 4, 3, 4, 3]
    day = 0
    while day < times_cycles:
        total_hours = days[day] * 24

        salt_app_time = (immersion_time + spraying_time) * times_immeresed
        cycle_time = 96/drying_time

        day = day + 1

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

        # for i in range(len(outlier_pairs)):
        #     df_x1 = df_outlier.loc[(df_outlier['Outlier'] == outlier_pairs[i][0])]
        #     df_x2 = df_outlier.loc[(df_outlier['Outlier'] == outlier_pairs[i][1])]
        # #         ax.axvspan(df_x1.index, df_x2.index, alpha = 0.2, color = 'red')

        ax.set_title('Thickness loss of a ' + str(thickness) + ' micron Fe substrate', fontsize=20)
        plt.xticks(fontsize=15)
        plt.yticks(fontsize=15)
        ax.set_xlabel('Hours', fontsize=20)
        ax.set_ylabel('Thickness loss (µm)', fontsize=20)
        ax.legend(fontsize=15)

    st.pyplot(fig)