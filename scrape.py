"""
This module is a modification of the `Web-Scraping-using-Python` notebook
by Karan Bhanot: https://github.com/kb22/Web-Scraping-using-Python
"""


import numpy as np
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup


def getHTMLContent(link):
    html = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

def getAdditionalDetails(url):
    try:
        country_page = getHTMLContent('https://en.wikipedia.org' + url)
        table = country_page.find('', 'infobox geography vcard')
        additional_details = []
        read_content = False
        for tr in table.find_all('tr'):
            if (tr.get('class') == ['mergedtoprow'] and not read_content):
                link = tr.find('a')
                if (link and (link.get_text().strip() == 'Area' or
                   (link.get_text().strip() == 'GDP' and tr.find('span').get_text().strip() == '(nominal)'))):
                    read_content = True
                if (link and (link.get_text().strip() == 'Population')):
                    read_content = False
            elif ((tr.get('class') == ['mergedrow'] or tr.get('class') == ['mergedbottomrow']) and read_content):
                additional_details.append(tr.find('td').get_text().strip('\n')) 
                if (tr.find('div').get_text().strip() != '•\xa0Total area' and
                   tr.find('div').get_text().strip() != '•\xa0Total'):
                    read_content = False
        return additional_details
    except Exception as error:
        print('Error occured IN HERE: {}'.format(error))
        return []

content = getHTMLContent('https://en.wikipedia.org/wiki/Member_states_of_the_United_Nations')
tables = content.find_all('table')
table = content.find('table', {'class': 'wikitable sortable'})
rows = table.find_all('tr')

data_content = []
for row in rows:
    cells = row.find_all('td')
    if len(cells) > 1:
        country_name = cells[0].find('a').get('title')
        print(country_name)
        country_link = cells[0].find('a')
        additional_details = getAdditionalDetails(country_link.get('href'))
        if (len(additional_details) == 4):
            country_info = [country_name] + additional_details
            data_content.append(country_info)

dataset = pd.DataFrame(data_content)

# Define column headings

headers = ['Country', 'Total Area', 'Percentage Water', 'Total Nominal GDP', 'Per Capita GDP']
dataset.columns = headers

dataset.to_csv("dataset.csv", index = False)
