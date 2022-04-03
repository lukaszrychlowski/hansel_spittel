import pandas as pd
import os
from matplotlib import pyplot as plt
import numpy as np
import mplcursors

def importer(file):
    df = pd.read_csv(path+file, delimiter=',', dtype=float, skiprows=6, names=['time', 'extension','load','comp_strain'])
    df = df.drop(columns=['time', 'comp_strain'])
    sample_parameters = get_sample_parameters(file)
    extension_shift(df)
    df = df.assign(strain=calc_strain(df['extension'], sample_parameters['height']))
    df = df.assign(stress=calc_stress(df['load'], sample_parameters['area']))
    df = df.assign(true_strain=calc_true_strain(df['strain']))
    df = df.assign(true_stress=calc_true_stress(df['stress'], df['strain']))
    return df

def extension_shift(df):
    shift_value = df['extension'].min()
    shift_value = float(shift_value)
    df['extension'] = df['extension'] - shift_value
    return None

def get_sample_parameters(file):
    df = pd.read_csv(path+file, nrows=3, dtype=str, header=None)
    try:
        sample_parameters = {'diameter': float(df[1].iloc[0]), 'temp': 0, 'height': float(df[1].iloc[1]), 'strain_rate': 0, 'label': df[1].iloc[2], 'area': 0, 'flow_stress': 0}
        
        if '10^-3' in sample_parameters['label']:
            sample_parameters['strain_rate'] = '10^-3'
        elif '10^-2' in sample_parameters['label']:
            sample_parameters['strain_rate'] = '10^-2'
        elif '10^-1' in sample_parameters['label']:
            sample_parameters['strain_rate'] = '10^-1'
        elif '10^0' in sample_parameters['label']: 
            sample_parameters['strain_rate'] = '10^0'

        sample_parameters['area'] = 0.25 * np.pi * sample_parameters['diameter']**2
        sample_parameters['temp'] = sample_parameters['label'][4:7]
        sample_parameters['label'] = sample_parameters['label'][:3]
    except TypeError:
        sample_parameters['temp'] = 'Null'
        sample_parameters['label'] = 'Null'
        sample_parameters['strain_rate'] = 'Null'
    return sample_parameters

def plotter(df, x, y):
    ax.plot(df[x], df[y], linewidth=1, label=sample_parameters['label'] + ', ' + sample_parameters['temp'] + ', ' + sample_parameters['strain_rate'] )
    ax.grid(which='both', color='gray', linewidth=0.5, alpha=0.5)
    ax.minorticks_on()
    plt.xlabel(x)
    plt.ylabel(y)
    return None

def calc_stress(load, area):
    stress = load/area
    return stress

def calc_strain(extension, length):
    strain = extension/length
    return strain

def calc_true_strain(strain):
    true_strain = -np.log(1 - strain)
    return true_strain

def calc_true_stress(stress, strain):
    true_stress = stress * (1 - strain)
    return true_stress

def get_avg_flow_stress(df, col):
    filter_df = df[(df[col] >= 0.2) & (df[col] < 1.2)]
    avg_flow_stress = filter_df['true_stress'].mean()
    #print(avg_flow_stress)
    return avg_flow_stress

path = '/Users/ryszard/Desktop/Skawina24.02.2022_80i87P_hotcompression/80P_87P_100 stopni C.is_comp_RawData/'

counter = 0
fig, ax = plt.subplots()

output_df = pd.DataFrame(columns=['diameter', 'temp', 'height', 'strain_rate', 'label', 'area', 'flow_stress'])
for file in os.listdir(path):
    if file.endswith('.csv'):
        try:
            df = importer(file)
            sample_parameters = get_sample_parameters(file)
            sample_parameters['flow_stress'] = get_avg_flow_stress(df,'true_strain')
            if sample_parameters['label'] == '80P':
                df['load'] = df['load'] * 0.000101971621
                #output_df = output_df.append(sample_parameters, ignore_index=True)
                plotter(df, 'extension', 'load')

        except ValueError:
            pass
#output_df.to_csv(path+'output.csv')
#plt.legend(fontsize='xx-small')
mplcursors.cursor(highlight=True).connect("add", lambda sel: sel.annotation.set_text(sel.artist.get_label()))
plt.show()