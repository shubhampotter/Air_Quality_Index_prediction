# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 14:45:00 2022

@author: ADMIN
"""

import os
import time
import requests
import sys

def retrieve_data(start_year,end_year):
    for year in range(start_year,end_year+1):
        for month in range(1,13):
            if month<10:
                url=f"https://en.tutiempo.net/climate/0{month}-{year}/ws-421820.html"
            else:
                url=f"https://en.tutiempo.net/climate/{month}-{year}/ws-421820.html"
            data=requests.get(url).text
            
            if not os.path.exists(f'Data/html_data/{year}'):
                os.makedirs(f'Data/html_data/{year}')
                
            #file handling
            with open(f'Data/html_data/{year}/{month}.html','w') as f:
                f.write(data)
                
        sys.stdout.flush()
                
if __name__=='__main__':
    start_time=time.time()
    retrieve_data(2013,2018)
    stop_time=time.time()
    print("Time_taken:",stop_time-start_time)