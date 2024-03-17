
import requests
from bs4 import BeautifulSoup
from csv import writer
import sqlite3 as sq
from datetime import datetime
import pandas as pd




source = requests.get('https://www.worldometers.info/coronavirus/').text
soup = BeautifulSoup(source, 'lxml')
table = soup.find('table', {'id': 'main_table_countries_today'})
body = table.find('tbody')

x = ["Asia","South America","North America","Europe","Africa","Australia/Oceania","South America"]

def super_continent(x):

    for row in body.find_all('tr', {'data-continent': [x]}):
        continent = row.find_all('td')[1].text.strip().replace(',', '')
        total_case = row.find_all('td')[2].text.strip().replace(',', '')
        new_case = row.find_all('td')[3].text.strip().replace(',', '').replace('+', '')
        total_death = row.find_all('td')[4].text.strip().replace(',', '')
        serious_case = row.find_all('td')[9].text.strip().replace(',', '')
        summary = [continent, total_case, new_case, total_death, serious_case]

    return summary

liste = [super_continent(x) for x in x]


with open('test.csv', 'w', encoding='utf8', newline='') as f:
    thewriter = writer(f)
    header = ['continent', 'total_case', 'new_case', 'total_death', 'serious_case']
    thewriter.writerow(header)
    for row in liste:
        for z in row:
            f.write(str(z) + ',')
        f.write('\n')

df = pd.read_csv('test.csv', index_col=False)
df['date']= datetime.today().strftime('%Y-%m-%d')

conn = sq.connect('test.db')
c = conn.cursor()

df.to_sql('final', conn, if_exists='append', index = False)
































