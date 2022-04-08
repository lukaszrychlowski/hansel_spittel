import pandas as pd
from matplotlib import pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

path = '/Users/ryszard/Desktop/Skawina24.02.2022_80i87P_hotcompression/80P_87P_100 stopni C.is_comp_RawData/output.csv'

def close_figure(event):
    if event.key == 'escape':
        plt.close(event.canvas.figure)

def hansel_spittel(T, strain_rate, A, m1, m3, m8, m9):
    #flow_stress = A * np.exp(m1 * T) * T**m9 * strain**m2 * np.exp(m4/strain) * (1+strain)**(m5*T) * np.exp(m7*strain) * strain_rate**m3 * strain_rate**(m8*T)
    flow_stress = A * np.exp(m1 * T) * T**m9 * strain_rate**m3 * strain_rate**(m8*T)
    return flow_stress

def plotter(df):
    ax = plt.subplot(projection='3d')
    p = ax.plot_trisurf(df['temp'], df['_strain_rate'], df['flow_stress'], alpha=0.2)
    q = ax.scatter(df['temp'], df['_strain_rate'], df['flow_stress'], c=df['flow_stress'], s=5, cmap='jet')
    r = ax.plot_trisurf(df['temp'], df['_strain_rate'], df['hansel_spittel'], color=(0,0,0,0), alpha=0.2)
    s = ax.scatter(df['temp'],df['_strain_rate'], df['hansel_spittel'], c='black', s=5)
    ax.set_xlim3d(100,500)
    #ax.set_ylim3d(-4,2)
    ax.set_zlim3d(0,1000)
    ax.set_ylabel('log strain rate')
    ax.set_xlabel('temp')
    ax.set_zlabel('flow stress')
    plt.colorbar(q)
    plt.gcf().canvas.mpl_connect('key_press_event', close_figure)
    return None

A = 950
m1 = -0.001188480220000008
m3 = -0.05903
m8 = 0.000564663
m9 = -0.042986383700000026

fig, ax = plt.subplots()
df = pd.read_csv(path, header=0)
df = df.assign(hansel_spittel=hansel_spittel(df['temp'], df['strain_rate'], A, m1, m3, m8, m9))
plotter(df)
plt.show()

# while m9 < 0.1:
#     df['hansel_spittel'] = hansel_spittel(df['temp'], df['strain_rate'], A, m1, m3, m8, m9)
#     m9 += 0.0001
#     print(m9)
#     plotter(df)
#     plt.pause(0.01)
#     plt.draw()

