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

pollutants=['O3','CO','NO2','SO2']
samplePerctg=0.5

for pollutant in pollutants:
    refData = REFprepData.mainREFprepData(Reffolder_path,pollutant)
    
    cleanData = CLEANprepData.mainCLEANprepData(CLEANfolder_path,pollutant,'fix')
    
    merge=pd.merge(cleanData,refData, how='inner', left_index=True, right_index=True)
    
    stats,table,bestSample = CLEANstats.statistics(merge,samplePerctg)
    
    #CLEANfigures.scatterCLEANvsREF(bestSample)
    
    cleanDataboots = CLEANprepData.mainCLEANprepDataBootstrap(CLEANfolder_path,pollutant,bestSample)

    merge=pd.merge(cleanDataboots,refData, how='inner', left_index=True, right_index=True)
    
    stats,table,bestSample = CLEANstats.statistics(merge,samplePerctg)
    
    CLEANfigures.plotCLEANvsREF(bestSample,pollutant)
    
    print(table)