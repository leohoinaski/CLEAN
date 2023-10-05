#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:34:39 2023

@author: leohoinaski
"""
import REFprepData
import CLEANprepData
import CLEANstats 
import CLEANfigures
import pandas as pd

Reffolder_path = '/media/leohoinaski/HDD/CLEAN/data/ref/diamante'
CLEANfolder_path = '/media/leohoinaski/HDD/CLEAN/data/2.input_equipo/dados_brutos'

pollutant='CO'

refData = REFprepData.mainREFprepData(Reffolder_path,pollutant)

cleanData = CLEANprepData.mainCLEANprepData(CLEANfolder_path,pollutant,'raw')

merge=pd.merge(cleanData,refData, how='inner', left_index=True, right_index=True)

stats,table = CLEANstats.statistics(merge)

#CLEANfigures.plotCLEANvsREF(merge)

print(table)