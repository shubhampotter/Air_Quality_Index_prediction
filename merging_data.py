

from plot_AQI import avg_data_2013,avg_data_2014,avg_data_2015,avg_data_2016,avg_data_2017, avg_data_2018
import os
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import csv

def merge_data(month,year):
    file_html=open(f'Data/html_data/{year}/{month}.html','r')
    text=file_html.read()
    
    soup=bs(text)
    temp_d=[]
    final_d=[]
    
    for table in soup.find_all('table',{'class':'medias mensuales numspan'}):
        for tbody in table:
            for tr in tbody:
                a=tr.text
                temp_d.append(a)
    rows=len(temp_d)/15           
    for i in range(round(rows)):
        new_temp_d=[]
        for i in range(15):
            new_temp_d.append(temp_d[0])
            temp_d.pop(0)
        final_d.append(new_temp_d)
    
    # remove unwanted rows
    final_d.pop(0) #it will remove 1st data
    final_d.pop(len(final_d)-1) # remove last data
    
    # remove unwanted column
    for a in range(len(final_d)):
        final_d[a].pop(6)
        final_d[a].pop(13)
        final_d[a].pop(12)
        final_d[a].pop(11)
        final_d[a].pop(10)
        final_d[a].pop(9)
        final_d[a].pop(0)
        
        
    return final_d

    

if not os.path.exists('Data/Real_data'):
    os.makedirs('Data/Real_data')
    
for year in range(2013,2018):
    final_data=[]
    with open(f'Data/Real_data/{year}.csv','w') as csvfile:
        csv_object=csv.writer(csvfile,dialect='excel')
        csv_object.writerow(['T','TM','Tm','SLP','H','VV','V','Vm','PM2.5'])
        

    for month in range(1,13):
        temp=merge_data(month, year)
        final_data+=temp
        


    
    #to make the target function dynamic

    pm=getattr(sys.modules[__name__],f'avg_data_{year}')()
    
    for i in range(len(final_data)-1):
        final_data[i].insert(-1,pm[i])
        
    with open(f'Data/Real_data/{year}.csv','a') as csvfile:
        csv_object=csv.writer(csvfile,dialect='excel')
        for row in final_data:
            flag=0
            for ele in row:
                if ele=="" or ele=="-":
                    flag=1
            if flag!=1:
                csv_object.writerow(row)
    

# code to merge all data in one single csv file with pandas
def year_range(start,end):
    df_list=[]
    for year in range(start,end):
        df=pd.read_csv(f'Data/Real_data/{year}.csv')
        df_list.append(df)
        
    return pd.concat(df_list,ignore_index=True)

df=year_range(2013, 2018)

df.to_csv('final_merged_data.csv')
