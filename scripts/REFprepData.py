# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 11:38:21 2023

@author: rafab
"""


import pandas as pd
import os
import numpy as np
import CLEANprepData

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
    

Reffolder_path = '/media/leohoinaski/HDD/CLEAN_Calibration/data/ref/diamante'
CLEANfolder_path = '/media/leohoinaski/HDD/CLEAN_Calibration/data/2.input_equipo/dados_brutos'

pollutant='CO'
refData = openRefMonitor(Reffolder_path,pollutant)
refData = refFixDatetime(refData)


cleanData = CLEANprepData.mainCLEANprepData(CLEANfolder_path,pollutant)

merge=pd.merge(cleanData,refData, how='inner', left_index=True, right_index=True)

