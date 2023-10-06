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


#folder_path = r'C:\Users\rafab\OneDrive\Documentos\CLEAN_Calibration\data\data_clean\dados_brutos'


CLEANfolder_path = '/mnt/sdb1/CLEAN/data/2.input_equipo/dados_brutos'
Reffolder_path = '/mnt/sdb1/CLEAN/data/ref/diamante'

#folder_path="C:/Users/Leonardo.Hoinaski/Documents/CLEAN_Calibration/scripts/data/2.input_equipo/dados_brutos"

# Reffolder_path = '/media/leohoinaski/HDD/CLEAN/data/ref/diamante'
# CLEANfolder_path = '/media/leohoinaski/HDD/CLEAN/data/2.input_equipo/dados_brutos'

pollutants=['O3','CO']

samplePerctg=0.5

nIteration = 1000

op = 'raw'

for pollutant in pollutants:
    
    refData = REFprepData.mainREFprepData(Reffolder_path,pollutant)
    
    cleanData = CLEANprepData.mainCLEANprepData(CLEANfolder_path,pollutant,op)
    
    merge=pd.merge(cleanData,refData, how='inner', left_index=True, right_index=True)
    
    stats,table,bestSample = CLEANstats.statistics(merge,samplePerctg,nIteration)
    
    CLEANfigures.scatterCLEANvsREF(bestSample)
    
    cleanDataboots = CLEANprepData.mainCLEANprepDataBootstrap(CLEANfolder_path,pollutant,bestSample)

    merge2=pd.merge(cleanDataboots,refData, how='inner', left_index=True, right_index=True)
    
    stats,table,bestSample2 = CLEANstats.statistics(merge2,samplePerctg,nIteration)
    
    CLEANfigures.plotCLEANvsREF(bestSample2,pollutant)
    
    print(table)