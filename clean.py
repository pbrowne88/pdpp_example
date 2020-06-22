"""
This module is a modification of the `Web-Scraping-using-Python` notebook
by Karan Bhanot: https://github.com/kb22/Web-Scraping-using-Python
"""

import re
import numpy as np
import pandas as pd

dataset = pd.read_csv("../input/dataset.csv")

dataset.rename(columns={'Total Area': 'Total Area (km2)'}, inplace = True)

for column in dataset.columns:
    dataset[column] = dataset[column].str.replace(r"\(.*\)", "")
    dataset[column] = dataset[column].str.replace(r"\[.*\]", "")


dataset['Percentage Water'] = dataset['Percentage Water'].str.strip('%')
dataset['Percentage Water'] = dataset['Percentage Water'].str.strip()

dataset['Total Area (km2)'] = dataset['Total Area (km2)'].str.replace(',', '')

for x in range(len(dataset['Total Area (km2)'])):
    area = dataset.iloc[x]['Total Area (km2)']
    if ('sq\xa0mi' in area):
        area = area.split('-')[0]
        area = re.sub(r'[^0-9.]+', '', area)
        area = int(float(area) * 2.58999)
    else:
        area = area.split('-')[0]
        area = re.sub(r'[^0-9.]+', '', area)
        area = int(float(area))
    dataset.iloc[x]['Total Area (km2)'] = area
    
dataset['Percentage Water'] = dataset['Percentage Water'].replace('negligible', '0.0')
dataset['Percentage Water'] = dataset['Percentage Water'].replace('Negligible', '0.0')
dataset['Percentage Water'] = dataset['Percentage Water'].str.replace(r'[^0-9]', '')
dataset.at[99, 'Percentage Water'] = '0.0' 

dataset = dataset[dataset['Percentage Water'].astype(float) <= 100]

dataset['Total Nominal GDP'] = dataset['Total Nominal GDP'].str.replace('$', '')

for x in range(len(dataset['Total Nominal GDP'])):
    gdp = dataset.iloc[x]['Total Nominal GDP']
    if ('trillion' in dataset.iloc[x]['Total Nominal GDP']):
        gdp = re.sub(r'[^0-9.]+', '', gdp)
        gdp = int(float(gdp) * 1000000000000)
    elif ('billion' in dataset.iloc[x]['Total Nominal GDP']):
        gdp = re.sub(r'[^0-9.]+', '', gdp)
        gdp = int(float(gdp) * 1000000000)
    elif ('million' in dataset.iloc[x]['Total Nominal GDP']):
        gdp = re.sub(r'[^0-9.]+', '', gdp)
        gdp = int(float(gdp) * 1000000)
    else:
        gdp = int(re.sub(r'[^0-9.]+', '', gdp))
    dataset.iloc[x]['Total Nominal GDP'] = gdp
    
dataset['Per Capita GDP'] = dataset['Per Capita GDP'].str.replace(r'[^0-9.]+', '')

dataset.to_csv("../output/final_dataset.csv", index = False)
