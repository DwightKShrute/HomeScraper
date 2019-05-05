#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests
from lxml import html, etree
import re


# In[2]:


#url = r'https://www.otodom.pl/sprzedaz/mieszkanie/warszawa/?search%5Bfilter_float_price%3Ato%5D=530000&search%5Bfilter_float_m%3Afrom%5D=45&search%5Bfilter_enum_extras_types%5D%5B0%5D=garage&search%5Bdescription%5D=1&search%5Bdist%5D=0&search%5Bsubregion_id%5D=197&search%5Bcity_id%5D=26&page=2'


# In[40]:


nazwa_mieszkania_val = []
cena_mieszkania_val = []
powierzchnia_mieszkania_val = []
rynek_mieszkania_val = []
pietro_mieszkania_val = []
rokbudowy_mieszkania_val = []
lat_mieszkania_val = []
long_mieszkania_val = []
id_url_val = []


for i in range(1, 3):
    url = r'https://www.otodom.pl/sprzedaz/mieszkanie/warszawa/?search%5Bfilter_float_price%3Ato%5D=530000&search%5Bfilter_float_m%3Afrom%5D=45&search%5Bfilter_enum_extras_types%5D%5B0%5D=garage&search%5Bdescription%5D=1&search%5Bdist%5D=0&search%5Bsubregion_id%5D=197&search%5Bcity_id%5D=26&page=' + str(i)
    #+ "\'"
    zapytanie = requests.get(url)
    parser = html.fromstring(zapytanie.content)
    strona = parser.xpath('//article/@data-url')
    
    for j in range(1, len(strona)):
        
        new_url = strona[j]
        zapytanie_strona = requests.get(new_url)
        parser_strona = html.fromstring(zapytanie_strona.content)
        
        nazwa_mieszkania = parser_strona.xpath('//div/h1[@class="css-19829c-AdHeader-className"]/text()')
        
        cena_mieszkania = parser_strona.xpath('//div/div[@class="css-c0ipkw-AdHeader"]/text()')
        
        powierzchnia_mieszkania = parser_strona.xpath('//div/ul/li[1]/strong/text()')
        
        rynek_mieszkania = parser_strona.xpath('//div/ul/li[3]/strong/text()')
        
        pietro_mieszkania = parser_strona.xpath('//div/ul/li[4]/strong/text()')
        
        rokbudowy_mieszkania = parser_strona.xpath('//div/ul/li[8]/strong/text()')
        
        lat_mieszkania = parser_strona.xpath('//div/script/text()')
        lat_mieszkania = re.findall(r"latitude\":\d*[.]\d*", str(lat_mieszkania))
        lat_mieszkania = re.findall(r'\d*[.]\d*' , str(lat_mieszkania))
        
        long_mieszkania = parser_strona.xpath('//div/script/text()')
        long_mieszkania = re.findall(r"longitude\":\d*[.]\d*", str(long_mieszkania))
        long_mieszkania = re.findall(r'\d*[.]\d*' , str(long_mieszkania))
        
        
        nazwa_mieszkania_val.append(nazwa_mieszkania)
        cena_mieszkania_val.append(cena_mieszkania)
        powierzchnia_mieszkania_val.append(powierzchnia_mieszkania)
        rynek_mieszkania_val.append(rynek_mieszkania)
        pietro_mieszkania_val.append(pietro_mieszkania)
        rokbudowy_mieszkania_val.append(rokbudowy_mieszkania)
        lat_mieszkania_val.append(lat_mieszkania)
        long_mieszkania_val.append(long_mieszkania)
        id_url_val.append(new_url)


# In[41]:


nazwa_mieszkania_val = pd.DataFrame(nazwa_mieszkania_val).rename(columns = {0:'NazwaMieszkania'})
cena_mieszkania_val = pd.DataFrame(cena_mieszkania_val).rename(columns = {0:'Cena'})
powierzchnia_mieszkania_val = pd.DataFrame(powierzchnia_mieszkania_val).rename(columns = {0:'Powierzchnia'})
rynek_mieszkania_val = pd.DataFrame(rynek_mieszkania_val).rename(columns = {0:'Rynek'})
pietro_mieszkania_val = pd.DataFrame(pietro_mieszkania_val).rename(columns = {0:'RokPietro'})
rokbudowy_mieszkania_val = pd.DataFrame(rokbudowy_mieszkania_val).rename(columns = {0:'RokBudowy'})
lat_mieszkania_val = pd.DataFrame(lat_mieszkania_val).astype(float).rename(columns = {0 : 'Latitude'})
long_mieszkania_val = pd.DataFrame(long_mieszkania_val).astype(float).rename(columns = {0: 'Longitude'})
id_url_val = pd.DataFrame(id_url_val).rename(columns = {0:'Adres'})


# In[62]:


dfs = pd.concat([nazwa_mieszkania_val, cena_mieszkania_val, powierzchnia_mieszkania_val, rynek_mieszkania_val, pietro_mieszkania_val, rokbudowy_mieszkania_val, lat_mieszkania_val, long_mieszkania_val, id_url_val], axis=1)
dfs.drop(1, axis=1, inplace=True)
dfs.head()


# In[63]:


dfs['Cena'] = dfs['Cena'].str.replace("zł", '')
dfs['Cena'] = dfs['Cena'].str.replace(" ", '')
dfs['Cena'] = dfs['Cena'].str.replace(",", '.').astype(float)


# In[64]:


dfs.dtypes


# In[ ]:




