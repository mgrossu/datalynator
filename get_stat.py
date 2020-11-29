#Autor: Marius Iustin Grossu xgross10
#Projekt 1 do IZV 
#!/usr/bin/python3
import os
import sys
import argparse
import matplotlib.pyplot as plt
import numpy as np
from download import DataDownloader


def create_arg_parser():
    parser = argparse.ArgumentParser(description='Script to show the stats of accidents in Czechia for the last years.')
    parser.add_argument('--fig_location', nargs=1, help='The path where to store the image.')
    parser.add_argument('--show_figure', action='store_true', help='Show the fig.')

    return parser


def sort_data_in_dict(dict):
    data_sorted = {k: v for k, v in sorted(dict.items(), key=lambda item:item[1])}
    numbers = list(data_sorted.values())
    order = {}
    j = len(numbers)
    for i in range(j):
        order[numbers[i]] = j
        j -= 1
    
    return  order


def set_order_on_bars(bar, ax, dict):
    for rect in bar:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.0, height-100, '%d' % int(dict[height]), ha='center', va='bottom')


def plot_stat(data_source, fig_location = None, show_figure = False):

    data = data_source[1]
    total_number_of_accidents = data[0].shape[0]
    data_2016 = {}
    data_2017 = {}
    data_2018 = {}
    data_2019 = {}
    data_2020 = {}

    for i in range(total_number_of_accidents):
        if data[64][i] == 'VYS':
            if 'VYS' not in data_2016:
                data_2016['VYS'] = 0
            if 'VYS' not in data_2017:
                data_2017['VYS'] = 0
            if 'VYS' not in data_2018:
                data_2018['VYS'] = 0
            if 'VYS' not in data_2019:
                data_2019['VYS'] = 0
            if 'VYS' not in data_2020:
                data_2020['VYS'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['VYS'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['VYS'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['VYS'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['VYS'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['VYS'] += 1
        
        if data[64][i] == 'JHM':
            if 'JHM' not in data_2016:
                data_2016['JHM'] = 0
            if 'JHM' not in data_2017:
                data_2017['JHM'] = 0
            if 'JHM' not in data_2018:
                data_2018['JHM'] = 0
            if 'JHM' not in data_2019:
                data_2019['JHM'] = 0
            if 'JHM' not in data_2020:
                data_2020['JHM'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['JHM'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['JHM'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['JHM'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['JHM'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['JHM'] += 1
        
        if data[64][i] == 'ZLK':
            if 'ZLK' not in data_2016:
                data_2016['ZLK'] = 0
            if 'ZLK' not in data_2017:
                data_2017['ZLK'] = 0
            if 'ZLK' not in data_2018:
                data_2018['ZLK'] = 0
            if 'ZLK' not in data_2019:
                data_2019['ZLK'] = 0
            if 'ZLK' not in data_2020:
                data_2020['ZLK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['ZLK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['ZLK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['ZLK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['ZLK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['ZLK'] += 1
        
        if data[64][i] == 'PLK':
            if 'PLK' not in data_2016:
                data_2016['PLK'] = 0
            if 'PLK' not in data_2017:
                data_2017['PLK'] = 0
            if 'PLK' not in data_2018:
                data_2018['PLK'] = 0
            if 'PLK' not in data_2019:
                data_2019['PLK'] = 0
            if 'PLK' not in data_2020:
                data_2020['PLK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['PLK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['PLK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['PLK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['PLK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['PLK'] += 1
        
        if data[64][i] == 'HKK':
            if 'HKK' not in data_2016:
                data_2016['HKK'] = 0
            if 'HKK' not in data_2017:
                data_2017['HKK'] = 0
            if 'HKK' not in data_2018:
                data_2018['HKK'] = 0
            if 'HKK' not in data_2019:
                data_2019['HKK'] = 0
            if 'HKK' not in data_2020:
                data_2020['HKK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['HKK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['HKK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['HKK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['HKK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['HKK'] += 1
        
        if data[64][i] == 'PAK':
            if 'PAK' not in data_2016:
                data_2016['PAK'] = 0
            if 'PAK' not in data_2017:
                data_2017['PAK'] = 0
            if 'PAK' not in data_2018:
                data_2018['PAK'] = 0
            if 'PAK' not in data_2019:
                data_2019['PAK'] = 0
            if 'PAK' not in data_2020:
                data_2020['PAK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['PAK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['PAK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['PAK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['PAK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['PAK'] += 1


        if data[64][i] == 'PHA':
            if 'PHA' not in data_2016:
                data_2016['PHA'] = 0
            if 'PHA' not in data_2017:
                data_2017['PHA'] = 0
            if 'PHA' not in data_2018:
                data_2018['PHA'] = 0
            if 'PHA' not in data_2019:
                data_2019['PHA'] = 0
            if 'PHA' not in data_2020:
                data_2020['PHA'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['PHA'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['PHA'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['PHA'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['PHA'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['PHA'] += 1

        if data[64][i] == 'STC':
            if 'STC' not in data_2016:
                data_2016['STC'] = 0
            if 'STC' not in data_2017:
                data_2017['STC'] = 0
            if 'STC' not in data_2018:
                data_2018['STC'] = 0
            if 'STC' not in data_2019:
                data_2019['STC'] = 0
            if 'STC' not in data_2020:
                data_2020['STC'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['STC'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['STC'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['STC'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['STC'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['STC'] += 1

        if data[64][i] == 'JHC':
            if 'JHC' not in data_2016:
                data_2016['JHC'] = 0
            if 'JHC' not in data_2017:
                data_2017['JHC'] = 0
            if 'JHC' not in data_2018:
                data_2018['JHC'] = 0
            if 'JHC' not in data_2019:
                data_2019['JHC'] = 0
            if 'JHC' not in data_2020:
                data_2020['JHC'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['JHC'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['JHC'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['JHC'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['JHC'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['JHC'] += 1


        if data[64][i] == 'KVK':
            if 'KVK' not in data_2016:
                data_2016['KVK'] = 0
            if 'KVK' not in data_2017:
                data_2017['KVK'] = 0
            if 'KVK' not in data_2018:
                data_2018['KVK'] = 0
            if 'KVK' not in data_2019:
                data_2019['KVK'] = 0
            if 'KVK' not in data_2020:
                data_2020['KVK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['KVK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['KVK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['KVK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['KVK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['KVK'] += 1


        if data[64][i] == 'ULK':
            if 'ULK' not in data_2016:
                data_2016['ULK'] = 0
            if 'ULK' not in data_2017:
                data_2017['ULK'] = 0
            if 'ULK' not in data_2018:
                data_2018['ULK'] = 0
            if 'ULK' not in data_2019:
                data_2019['ULK'] = 0
            if 'ULK' not in data_2020:
                data_2020['ULK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['ULK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['ULK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['ULK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['ULK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['ULK'] += 1


        if data[64][i] == 'LBK':
            if 'LBK' not in data_2016:
                data_2016['LBK'] = 0
            if 'LBK' not in data_2017:
                data_2017['LBK'] = 0
            if 'LBK' not in data_2018:
                data_2018['LBK'] = 0
            if 'LBK' not in data_2019:
                data_2019['LBK'] = 0
            if 'LBK' not in data_2020:
                data_2020['LBK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['LBK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['LBK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['LBK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['LBK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['LBK'] += 1

        if data[64][i] == 'OLK':
            if 'OLK' not in data_2016:
                data_2016['OLK'] = 0
            if 'OLK' not in data_2017:
                data_2017['OLK'] = 0
            if 'OLK' not in data_2018:
                data_2018['OLK'] = 0
            if 'OLK' not in data_2019:
                data_2019['OLK'] = 0
            if 'OLK' not in data_2020:
                data_2020['OLK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['OLK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['OLK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['OLK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['OLK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['OLK'] += 1

        if data[64][i] == 'MSK':
            if 'MSK' not in data_2016:
                data_2016['MSK'] = 0
            if 'MSK' not in data_2017:
                data_2017['MSK'] = 0
            if 'MSK' not in data_2018:
                data_2018['MSK'] = 0
            if 'MSK' not in data_2019:
                data_2019['MSK'] = 0
            if 'MSK' not in data_2020:
                data_2020['MSK'] = 0

            if (data[3][i] > np.datetime64('2016-01-01')) and (data[3][i] < np.datetime64('2016-12-31')):
                data_2016['MSK'] += 1
            if (data[3][i] > np.datetime64('2017-01-01')) and (data[3][i] < np.datetime64('2017-12-31')):
                data_2017['MSK'] += 1
            if (data[3][i] > np.datetime64('2018-01-01')) and (data[3][i] < np.datetime64('2018-12-31')):
                data_2018['MSK'] += 1
            if (data[3][i] > np.datetime64('2019-01-01')) and (data[3][i] < np.datetime64('2019-12-31')):
                data_2019['MSK'] += 1
            if (data[3][i] > np.datetime64('2020-01-01')) and (data[3][i] < np.datetime64('2020-12-31')):
                data_2020['MSK'] += 1

    order16 = sort_data_in_dict(data_2016)
    order17 = sort_data_in_dict(data_2017)
    order18 = sort_data_in_dict(data_2018)
    order19 = sort_data_in_dict(data_2019)
    order20 = sort_data_in_dict(data_2020)

    name16 = list(data_2016.keys())
    values16 = list(data_2016.values())

    name17 = list(data_2017.keys())
    values17 = list(data_2017.values())

    name18 = list(data_2018.keys())
    values18 = list(data_2018.values())

    name19 = list(data_2019.keys())
    values19 = list(data_2019.values())

    name20 = list(data_2020.keys())
    values20 = list(data_2020.values())

    fig = plt.figure(constrained_layout=True, figsize=(9,8))
    ax16, ax17, ax18, ax19, ax20 = (fig.add_gridspec(nrows=5, ncols=1).subplots())
    bar16 = ax16.bar(name16, values16, width=0.28, color='red', align='center')
    bar17 = ax17.bar(name17, values17, width=0.28, color='red', align='center')
    bar18 = ax18.bar(name18, values18, width=0.28, color='red', align='center')
    bar19 = ax19.bar(name19, values19, width=0.28, color='red', align='center') 
    bar20 = ax20.bar(name20, values20, width=0.28, color='red', align='center')
    ax16.title.set_text('Počet nehod v jednotlivých krajích za rok 2016')
    ax17.title.set_text('Počet nehod v jednotlivých krajích za rok 2017')
    ax18.title.set_text('Počet nehod v jednotlivých krajích za rok 2018')
    ax19.title.set_text('Počet nehod v jednotlivých krajích za rok 2019')
    ax20.title.set_text('Počet nehod v jednotlivých krajích za rok 2020')
    ax16.spines["top"].set_visible(False) 
    ax16.spines["right"].set_visible(False)
    ax17.spines["top"].set_visible(False) 
    ax17.spines["right"].set_visible(False)
    ax18.spines["top"].set_visible(False) 
    ax18.spines["right"].set_visible(False)
    ax19.spines["top"].set_visible(False) 
    ax19.spines["right"].set_visible(False)
    ax20.spines["top"].set_visible(False) 
    ax20.spines["right"].set_visible(False)
    
    set_order_on_bars(bar16, ax16, order16)
    set_order_on_bars(bar17, ax17, order17)
    set_order_on_bars(bar18, ax18, order18)
    set_order_on_bars(bar19, ax19, order19)
    set_order_on_bars(bar20, ax20, order20)

    if fig_location is not None:
        if not os.path.exists(fig_location):
             try:
                os.mkdir(fig_location)
             except OSError:
                print ("Creation of the directory %s failed" % fig_location)
        if not os.path.isabs(fig_location):
            fig_location = os.path.join(os.path.abspath(os.path.dirname(__file__)), fig_location)
        fig.savefig(os.path.join(fig_location, 'plot.png'))
    
    if show_figure:
        plt.show()


if __name__ == "__main__":
    fig_location = None
    show_figure = False

    if len(sys.argv) > 1:  
        arg_parser = create_arg_parser()
        parsed_args = arg_parser.parse_args(sys.argv[1:])
        if parsed_args.fig_location:
            fig_location = parsed_args.fig_location[0]
        if parsed_args.show_figure: 
            show_figure = parsed_args.show_figure
    
    data_source = DataDownloader().get_list()
    plot_stat(data_source, fig_location=fig_location, show_figure=show_figure)