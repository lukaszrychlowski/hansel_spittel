import random as rand
import pandas as pd
from matplotlib import pyplot as plt
import numpy as np

'''
prep
'''
path = '/Users/ryszard/Desktop/Skawina24.02.2022_80i87P_hotcompression/80P_87P_100 stopni C.is_comp_RawData/output_80P.csv'
lower = 0.97    #defines range size in randomization for positive numbers
_lower = 1.03   #defines range size in randomization for negative numbers
higher = _lower
_higher = lower
_hansel_dict = {'A': 1110.2171809910833, 'm1': -0.005458398840888382, 'm3': -0.05571287983210331, 'm8': 0.0005572456450404376, 'm9': -0.02371389209026133}

# _A1 = rand.uniform(100,1200)
# _m1 = rand.uniform(-0.1, 0)
# _m3 = rand.uniform(-0.2,0.2)
# _m8 = rand.uniform(0, 0.01)
# _m9 = rand.uniform(-0.1, 0)
#_hansel_dict = {'A': _A1, 'm1': _m1, 'm3': _m3, 'm8': _m8, 'm9': _m9}

'''
calculate the difference between calculated flow stress using hansel spittel equation and experimental
'''
def hansel_compare(df):
    df = df.assign(hansel_compare=np.abs((df['hansel_spittel'] - df['flow_stress']))*df['score'])
    compare_sum = df['hansel_compare'].sum()
    return compare_sum

'''
randomize new hansel-spittel coefficients based on previously used values
'''
def random_hansel():
    A = rand.uniform(_hansel_dict['A']*lower, _hansel_dict['A']*higher)
    m1 = rand.uniform(_hansel_dict['m1']*_lower, _hansel_dict['m1']*_higher)
    m3 = rand.uniform(_hansel_dict['m3']*_lower, _hansel_dict['m3']*_higher)
    m8 = rand.uniform(_hansel_dict['m8']*lower, _hansel_dict['m8']*higher)
    m9 = rand.uniform(_hansel_dict['m9']*_lower, _hansel_dict['m9']*_higher)
    hansel_dict = {'A': A, 'm1': m1, 'm3': m3, 'm8': m8, 'm9': m9}
    return hansel_dict

'''
calculate the flow stress using hansel spittel, strain-dependant coefficients are skipped
'''
def hansel_spittel(T, strain_rate, hansel_dict):
    flow_stress = hansel_dict['A'] * np.exp(hansel_dict['m1'] * T) * T**hansel_dict['m9'] * strain_rate**hansel_dict['m3'] * strain_rate**(hansel_dict['m8']*T)
    #flow_stress = A * np.exp(m1 * T) * T**m9 * strain**m2 * np.exp(m4/strain) * (1+strain)**(m5*T) * np.exp(m7*strain) * strain_rate**m3 * strain_rate**(m8*T)
    #flow_stress = A * np.exp(m1 * T) * T**m9 * strain_rate**m3 * strain_rate**(m8*T)
    return flow_stress

'''
weights used to compare the flow stresses, we're focusing on higher temps
'''
def hansel_score(df):
    df=df.assign(score=0)
    df.loc[df['temp'] == 100, 'score'] = 0.01
    df.loc[df['temp'] == 200, 'score'] = 0.01
    df.loc[df['temp'] == 300, 'score'] = 0.5
    df.loc[df['temp'] == 400, 'score'] = 0.7
    df.loc[df['temp'] == 450, 'score'] = 1
    df.loc[df['temp'] == 500, 'score'] = 1
    return df

'''
plot
'''
def plotter(df):
    ax = plt.subplot(projection='3d')
    p = ax.plot_trisurf(df['temp'], df['_strain_rate'], df['flow_stress'], alpha=0.2)
    q = ax.scatter(df['temp'], df['_strain_rate'], df['flow_stress'], c=df['flow_stress'], s=5, cmap='jet')
    r = ax.plot_trisurf(df['temp'], df['_strain_rate'], df['hansel_spittel'], color=(0,0,0,0), alpha=0.2)
    s = ax.scatter(df['temp'],df['_strain_rate'], df['hansel_spittel'], c='black', s=5)
    ax.set_xlim3d(100,500)
    #ax.set_ylim3d(-4,2)
    ax.set_zlim3d(0,700)
    ax.set_ylabel('log strain rate')
    ax.set_xlabel('temp')
    ax.set_zlabel('flow stress')
    plt.colorbar(q)
    return None

'''
prep before loop
'''
fig, ax = plt.subplots()
df = pd.read_csv(path, header=0)
df = hansel_score(df)
hansel_dict = random_hansel()
df = df.assign(hansel_spittel=hansel_spittel(df['temp'], df['strain_rate'], hansel_dict))
hansel_compare_sum_check = hansel_compare(df)
plotter(df)

'''
loop randomizing different coefficients, if the difference between calculated and experimental flow stress is getting lower the 
alghoritm will use previous coefficients to randomize new ones - getting closer to optimal values
'''
while 1:
    hansel_dict = random_hansel()
    df['hansel_spittel'] = hansel_spittel(df['temp'], df['strain_rate'], hansel_dict)
    hansel_compare_sum = hansel_compare(df)
    if hansel_compare_sum < hansel_compare_sum_check:
        hansel_difference = hansel_compare_sum_check - hansel_compare_sum
        hansel_compare_sum_check = hansel_compare_sum
        _hansel_dict = hansel_dict
        print(hansel_compare_sum)
        print(hansel_dict)
        plotter(df)
    plt.pause(0.1)
    plt.draw()


