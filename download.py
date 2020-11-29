#Autor: Marius Iustin Grossu xgross10
#Projekt 1 do IZV 
#!/usr/bin/python3
import os 
import sys 
import re
import requests 
import gzip
import pickle
import csv
import zipfile
import numpy as np
from bs4 import BeautifulSoup
from urllib.parse import urlparse, unquote, urlunparse
from datetime import date
from io import TextIOWrapper


def read_data_from_zip_and_csv(zip_file, csv_file, my_list):
    with zipfile.ZipFile(zip_file) as zf:
            with zf.open(csv_file, 'r') as infile:
                reader = csv.reader(TextIOWrapper(infile, 'windows-1250'), delimiter=';', quotechar='"')
                for row in reader:
                    my_list.append(row)
                    

class DataDownloader:
    def __init__(self, url="https://ehw.fit.vutbr.cz/izv/", folder="data", cache_filename="data_{}.pkl.gz"):
        self.url = url
        self.folder = folder
        self.cache_filename = cache_filename
        self.regions_parsed = {
            "PHA" : None,
            "STC" : None,
            "JHC" : None,
            "PLK" : None,
            "KVK" : None,
            "ULK" : None,
            "LBK" : None,
            "HKK" : None,
            "PAK" : None,
            "OLK" : None,
            "MSK" : None,
            "JHM" : None,
            "ZLK" : None,
            "VYS" : None
        }

    def download_data(self):
        cwd = os.getcwd()
        data_dir = cwd + '/' + self.folder
        month_year = date.today().strftime("%m-%Y")


        if not os.path.isdir(data_dir):
            try:
                os.mkdir(data_dir)
            except OSError:
                print ("Creation of the directory %s failed" % data_dir)

        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"}
        r1 = requests.get(self.url, headers=headers)
        parsedurl = urlparse(self.url)
        pth, bfn = os.path.split(unquote(parsedurl.path))
        soup = BeautifulSoup(r1.text, 'html.parser')
        links = []
        for link in soup.find_all('a', text = re.compile('ZIP')):
            url = link.get('href')
            if url == 'data/datagis2016.zip':
                links.append(url)
            if url == 'data/datagis-rok-2017.zip':
                links.append(url)
            if url == 'data/datagis-rok-2018.zip':
                links.append(url)
            if url == 'data/datagis-rok-2019.zip':
                links.append(url)
            if (int(month_year[3:]) == 2020):
                if (int(month_year[0:2]) < 12):
                    if url == 'data/datagis-11-2020.zip':
                        links.append(url)

                    elif url == 'data/datagis-10-2020.zip':
                        links.append(url)

                    elif url == 'data/datagis-09-2020.zip':
                        links.append(url)
            else:
                if url == 'data/datagis-rok-2020.zip':
                    links.append(url)
        for newlink in links:
            file_name = newlink[4:]
            newurl = urlunparse(parsedurl._replace(path='/'.join((pth, newlink))))
            r2 = requests.get(newurl, stream = True)
            #print(newurl)
            path_to_file = data_dir + file_name
            with open(path_to_file, 'wb') as fd:
                for chunk in r2.iter_content(chunk_size=128):
                    fd.write(chunk)

    def parse_region_data(self, region):
        cwd = os.getcwd()
        data_dir = cwd + '/' + self.folder + '/'
        parsed_region_data = data_dir + self.cache_filename.format(region)
        month_year = date.today().strftime("%m-%Y")
        regions = {
            "PHA" : "00.csv",
            "STC" : "01.csv",
            "JHC" : "02.csv",
            "PLK" : "03.csv",
            "KVK" : "19.csv",
            "ULK" : "04.csv",
            "LBK" : "18.csv",
            "HKK" : "05.csv",
            "PAK" : "17.csv",
            "OLK" : "14.csv",
            "MSK" : "07.csv",
            "JHM" : "06.csv",
            "ZLK" : "15.csv",
            "VYS" : "16.csv"
        }
        number_csv = regions[region]
        #https://www.policie.cz/soubor/polozky-formulare-hlavicky-souboru-xlsx.aspx popis datovych slozek
        name_of_data = ["p1", "p36", "p37", "p2a", "weekday(p2a)", "p2b", "p6", "p7", "p8", "p9", "p10", "p11", "p12", "p13a", "p13b", "p13c", "p14", "p15", "p16", "p17", "p18", "p19", "p20", "p21", "p22", "p23", "p24", "p27", "p28", "p34", "p35", "p39", "p44", "p45a", "p47", "p48a", "p49", "p50a", "p50b", "p51", "p52", "p53", "p55a", "p57", "p58", "a", "b", "d", "e", "f", "g", "h", "i", "j", "k", "l", "n", "o", "p", "q", "r", "s", "t", "p5a", "region"]
        data = []
        my_file = []

        if not os.path.isdir(data_dir):
            self.download_data()

        if (int(month_year[3:]) > 2016):
            zip_file2016 = data_dir + "datagis2016.zip"
        if (int(month_year[3:]) > 2017):
            zip_file2017 = data_dir + "datagis-rok-2017.zip"
        if (int(month_year[3:]) > 2018):
            zip_file2018 = data_dir + "datagis-rok-2018.zip"
        if (int(month_year[3:]) > 2019):
            zip_file2019 = data_dir + "datagis-rok-2019.zip"
        if (int(month_year[3:]) == 2020):
            if (int(month_year[0:2]) < 12):
                zip_file2020 = data_dir + "datagis-09-2020.zip" 
            else:
                zip_file2020 = data_dir + "datagis-rok-2020.zip"

        list_zip = [zip_file2016, zip_file2017, zip_file2018, zip_file2019, zip_file2020]

        for fz in list_zip:
            read_data_from_zip_and_csv(fz, number_csv, my_file)

        #print(my_file)
        array = np.array(my_file)
        #for missing data or wrong I replace the cell with number -42
        for i in range(0,array.shape[1]):
            arr = array[:,[i]]
            shape = arr.shape
            newshape = (shape[0])
            arr = np.reshape(arr,newshape)
            if i == 0:
                for j in range(shape[0]):
                    if arr[j] == '':
                        arr[j] = -42
                arr = arr.astype(np.int64)
            elif i == 2:
                for j in range(shape[0]):
                    if arr[j] == '':
                        arr[j] = -42
                arr = arr.astype(np.int32)
            elif i == 3:
                for j in range(shape[0]):
                    arr[j] = np.datetime64(arr[j])
                arr = arr.astype('datetime64[D]')
            elif i == 5:
                for j in range(shape[0]):
                    hours_minute = arr[j]
                    hours = int(hours_minute[0:2])
                    minutes = int(hours_minute[2:])
                    if hours == 25:
                        arr[j] = -42
                    elif hours < 25:
                        if minutes == 60:
                            arr[j] = hours
                arr = arr.astype(np.int16)
            elif i == 12:
                for j in range(shape[0]):
                    if arr[j] == '':
                        arr[j] = -42
                arr = arr.astype(np.int16)
            elif i == 41:
                for j in range(shape[0]):
                    if arr[j] == '':
                        arr[j] = -42
                arr = arr.astype(np.int16)
            elif i in range(45,51):
                for j in range(shape[0]):
                    arr[j] = arr[j].replace(',','.')
                    if arr[j] == '':
                        arr[j] = -42
                    if arr[j] == 'A:':
                        arr[j] = -42
                    if arr[j] == 'B:':
                        arr[j] = -42
                    if arr[j] == 'D:':
                        arr[j] = -42
                    if arr[j] == 'E:':
                        arr[j] = -42
                    if arr[j] == 'F:':
                        arr[j] = -42
                    if arr[j] == 'G:':
                        arr[j] = -42
                    if arr[j] == 'H:':
                        arr[j] = -42
                    if arr[j] == 'I:':
                        arr[j] = -42
                    if arr[j] == 'L:':
                        arr[j] = -42
                arr = arr.astype(np.float64)
            elif i in range(51, 60):
                for j in range(shape[0]):
                    if arr[j] == '':
                        arr[j] = -42
                arr = arr.astype(np.str)
            elif i in range(60, 62):
                for j in range(shape[0]):
                    if arr[j] == '':
                        arr[j] = -42
                arr = arr.astype(np.int64)
            elif i == 62:
                arr = arr.astype(np.str)
            else:
                for j in range(shape[0]):
                    if arr[j] == '':
                        arr[j] = -42
                    if arr[j] == 'XX':
                        arr[j] = -42
                arr = arr.astype(np.int8)
            data.append(arr)
        
        region_shape = data[0].shape

        region_arr = np.full((region_shape), region)

        data.append(region_arr)

        region_parsed = (name_of_data, data)
 
        with gzip.open(parsed_region_data,'wb') as f: 
            pickle.dump(region_parsed, f)

        self.regions_parsed[region] = region_parsed

        return region_parsed

    def get_list(self, regions=None):
        cwd = os.getcwd()
        data_dir = cwd + '/' + self.folder + '/'
        regions_body = []
        regions_head = []

        if regions is None:
            regions = ['PHA','STC','JHC','PLK','KVK','ULK','LBK','HKK','PAK','OLK','MSK','JHM','ZLK','VYS']
        
        first_region = regions[0]
        #print(first_region)
        parsed_region_data = data_dir + self.cache_filename.format(first_region)
        if self.regions_parsed[first_region] is not None:
            y = list(self.regions_parsed[first_region])
            regions_head = y[0]
            regions_body = y[1]
        elif os.path.isfile(parsed_region_data):
            with gzip.open(parsed_region_data,'r') as f:
                parsed_region = pickle.load(f)
            self.regions_parsed[first_region] = parsed_region
            y = list(self.regions_parsed[first_region])
            regions_head = y[0]
            regions_body = y[1]
        else:
            (regions_head, regions_body) = self.parse_region_data(first_region)

        regions = regions[1:]

        if len(regions) > 0:
            for region in regions:
                parsed_region_data = data_dir + self.cache_filename.format(region)
                if self.regions_parsed[region] is not None:
                    y = list(self.regions_parsed[region])
                    for i in range(0,65):
                        regions_body[i] = np.concatenate((regions_body[i], y[1][i]))
                elif os.path.isfile(parsed_region_data):
                    with gzip.open(parsed_region_data,'r') as f:
                        parsed_region = pickle.load(f)
                    self.regions_parsed[region] = parsed_region
                    y = list(self.regions_parsed[region])
                    for i in range(0,65):
                        regions_body[i] = np.concatenate((regions_body[i], y[1][i]))
                        #print(y[1][i].shape)
                else:
                   (regions_head_local, regions_body_local) = self.parse_region_data(region)
                   for i in range(0,65):
                       regions_body[i] = np.concatenate((regions_body_local[i], regions_body[i]))

        result = (regions_head, regions_body)
        
        return result
        

if __name__ == "__main__":
    dd = DataDownloader()
    r = dd.get_list(['ZLK', 'VYS', 'JHM'])
    print("Význam jendotlivých položek sloupce: https://www.policie.cz/soubor/polozky-formulare-hlavicky-souboru-xlsx.aspx")
    print("Jednotlive sloupce:")
    print(r[0])
    print("Data:")
    print(r[1])
    print("Kraje: Zlinsky kraj (ZLK), Kraj Vysocina (VYS), Jihomoravsky kraj (JHM)")
    print("Celkovy pocet zaznamu (1 zaznam = 1 radek = 1 nehoda): {}".format(r[1][0].shape[0]))
    JHM_accidents = 0
    for i in range(r[1][0].shape[0]):
        if r[1][64][i] == 'JHM':
            JHM_accidents += 1
    print("Pocet nehod v Jihomoravksem kraji: {}".format(JHM_accidents))
    ZLK_accidents = 0
    for i in range(r[1][0].shape[0]):
       if r[1][64][i] == 'ZLK':
            ZLK_accidents += 1
    print("Pocet nehod ve Zlinskem kraji: {}".format(ZLK_accidents))
    VYS_accidents = 0
    for i in range(r[1][0].shape[0]):
       if r[1][64][i] == 'VYS':
            VYS_accidents += 1
    print("Pocet nehod v kraji Vysocina: {}".format(VYS_accidents))
