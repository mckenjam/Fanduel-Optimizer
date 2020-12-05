# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 11:51:26 2020

@author: James McKenna
"""

import os 
import sys 
import pandas as pd 
import urllib.request
from bs4 import BeautifulSoup 
   
path = 'https://www.footballdiehards.com/fantasyfootball/dailygames/FanDuel-Salary-data.cfm'
   
# empty list 
data = [] 
   
# for getting the header from 
# the HTML file 
list_header = [] 
req = urllib.request.Request(path, headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36","X-Requested-With": "XMLHttpRequest"})
page = urllib.request.urlopen(req)
soup = BeautifulSoup(page,"html.parser")

header = soup.find_all("table")[0].find("tr") 
  
for items in header: 
    try: 
        list_header.append(items.get_text()) 
    except: 
        continue
  
# for getting the data  
HTML_data = soup.find_all("table")[0].find_all("tr")[1:] 
  
for element in HTML_data: 
    sub_data = [] 
    for sub_element in element: 
        try: 
            sub_data.append(sub_element.get_text()) 
        except: 
            continue
    data.append(sub_data) 
  
# Storing the data into Pandas 
# DataFrame  
dataFrame = pd.DataFrame(data = data, columns = list_header) 

new_header = dataFrame.iloc[0] #grab the first row for the header
dataFrame = dataFrame[1:] #take the data less the header row
dataFrame.columns = new_header #set the header row as the df header

del dataFrame['year']
del dataFrame['week']
del dataFrame['Factor']
del dataFrame['Rank']

dataFrame = dataFrame.loc[dataFrame['Score']!='-']

dataFrame.to_csv('Geeks.csv', index=False) 

dataFrame['SALARY'] = dataFrame['SALARY'].map(lambda x: x.lstrip('$'))

QBs = dataFrame.loc[dataFrame['Pos']=='QB'].reset_index(drop=True)
QBs.columns = ['QB', 'Pos', 'QBcost', 'QBpoints']
RBs = dataFrame.loc[dataFrame['Pos']=='RB'].reset_index(drop=True)
RBs.columns = ['RB', 'Pos', 'RBcost', 'RBpoints']
WRs = dataFrame.loc[dataFrame['Pos']=='WR'].reset_index(drop=True)
WRs.columns = ['WR', 'Pos', 'WRcost', 'WRpoints']
TEs = dataFrame.loc[dataFrame['Pos']=='TE'].reset_index(drop=True)
TEs.columns = ['TE', 'Pos', 'TEcost', 'TEpoints']
DEFs = dataFrame.loc[dataFrame['Pos']=='D'].reset_index(drop=True)
DEFs.columns = ['DEF', 'Pos', 'DEFcost', 'DEFpoints']

del QBs['Pos']
del RBs['Pos']
del WRs['Pos']
del TEs['Pos']
del DEFs['Pos']

dataFrame = pd.concat([QBs, RBs], axis=1)
dataFrame = pd.concat([dataFrame, WRs], axis=1)
dataFrame = pd.concat([dataFrame, TEs], axis=1)
dataFrame = pd.concat([dataFrame, DEFs], axis=1)

# Converting Pandas DataFrame 
# into CSV file 
dataFrame.to_csv('Fanduel_Players.csv', index=False) 
