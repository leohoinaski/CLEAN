# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 11:38:21 2023

@author: rafab
"""


import pandas as pd
import os
import numpy as np


def openRefMonitor(folder_path,pollutant):
    """

    Parameters
    ----------
    folder_path : String
        Path to the folder with .csv files containing small sensors data
        
    pollutant : String
        Pollutant specie to be analyzed

    Returns
    -------
    monitors : Dataframe
        Pandas dataframe containig the dataset with datetime index and
        measured pollutant concentrations 
        Columns = DataTime (index), Sensor_(n), year, month, day, hour, datetime

    """
    # Listing files within the folder_path
    file_list = os.listdir(folder_path)
    print(file_list) 
    
    # Appending data in monitors list
    monitors = []
    for file_name in file_list:
        if file_name.startswith('ref_'+pollutant):
            print(file_name) 
            mon = pd.read_csv(folder_path+'/'+file_name)
            idx = pd.DatetimeIndex(mon['DateTime'])
            mon.set_index(idx, inplace=True)
            monitors.append(mon)
    
    # Converting to pandas DataFrame
    monitors = pd.concat(monitors, axis=1)
    monitors = monitors[['measuring']]

    monitors.columns = ['ref']
        
    return monitors

def refFixDatetime(refData):
    df = pd.DataFrame({'year': refData.index.year,
                   'month':refData.index.month,
                   'day': refData.index.day,
                   'hour':refData.index.hour})
    #refData['datetime'] = pd.to_datetime(df)
    refData = refData.set_index(pd.to_datetime(df))
    return refData
    

def mainREFprepData(Reffolder_path,pollutant):
    refData = openRefMonitor(Reffolder_path,pollutant)
    refData = refFixDatetime(refData)
    refData['ref'][refData['ref']<0]=np.nan
    return refData
