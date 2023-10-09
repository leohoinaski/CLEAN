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
import CLEANmodel



#folder_path = r'C:\Users\rafab\OneDrive\Documentos\CLEAN_Calibration\data\data_clean\dados_brutos'

# PC LAB
CLEANfolder_path = '/mnt/sdb1/CLEAN/data/Inputs/CLEAN'
Reffolder_path = '/mnt/sdb1/CLEAN/data/Inputs/Reference/diamante'
outPath = '/mnt/sdb1/CLEAN/data/Outputs'

# PC CASA
Reffolder_path = '/media/leohoinaski/HDD/CLEAN/data/Inputs/Reference/diamante'
CLEANfolder_path = '/media/leohoinaski/HDD/CLEAN/data/Inputs/CLEAN'
outPath = '/media/leohoinaski/HDD/CLEAN/data/Outputs'

# Inputs
pollutants=['O3','CO','NO2','SO2']
samplePerctg=0.7 # Percentage of data for training 
nIteration = 1000 # Number of random samples
op = 'raw' # option to data preparing
deviceId = '01' # Device Identification
sensor ='01'
#------------------------------PROCESSING--------------------------------------
dataModel = pd.DataFrame()
dataBestModel = pd.DataFrame()

# Loop for each pollutant
for pollutant in pollutants:
    # Reference data
    refData = REFprepData.mainREFprepData(Reffolder_path,pollutant)
    dataModel['ref_'+pollutant] =  refData
    
    # CLEAN data
    cleanData = CLEANprepData.mainCLEANprepData(CLEANfolder_path,pollutant,op)
    dataModel[pollutant] =  cleanData
    
    # Merging DataFrames
    merge=pd.merge(cleanData,refData, how='inner', left_index=True, right_index=True)
    
    # Get best sample for training
    stats,table,bestSample = CLEANstats.statistics(merge,samplePerctg,nIteration)
    print(table)
    
    # Extracting data 
    dataBestModel['ref_'+pollutant] =  bestSample['ref'].drop_duplicates()
    dataBestModel[pollutant] =  cleanData['timeseries'].drop_duplicates()
    
    #CLEANfigures.scatterCLEANvsREF(bestSample)
    
    # cleanDataboots = CLEANprepData.mainCLEANprepDataBootstrap(CLEANfolder_path,pollutant,bestSample)

    # merge2=pd.merge(cleanDataboots,refData, how='inner', left_index=True, right_index=True)
    
    # stats,table,bestSample2 = CLEANstats.statistics(merge2,samplePerctg,nIteration)
    
    #CLEANfigures.plotCLEANvsREF(bestSample2,pollutant)
   
# Model for each pollutant   
for pollutant in pollutants:
    models = CLEANmodel.CLEANbestModel(dataBestModel,pollutant)
    bestModel = CLEANmodel.modelsEvaluation(dataModel,models,pollutant)
    CLEANfigures.scatterModelvsObs(dataModel,bestModel,pollutant)
    CLEANmodel.saveModel(outPath,pollutant,deviceId,sensor,bestModel)