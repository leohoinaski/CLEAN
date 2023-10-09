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


CLEANfolder_path = '/mnt/sdb1/CLEAN/data/2.input_equipo/dados_brutos'
Reffolder_path = '/mnt/sdb1/CLEAN/data/ref/diamante'

#folder_path="C:/Users/Leonardo.Hoinaski/Documents/CLEAN_Calibration/scripts/data/2.input_equipo/dados_brutos"

Reffolder_path = '/media/leohoinaski/HDD/CLEAN/data/ref/diamante'
CLEANfolder_path = '/media/leohoinaski/HDD/CLEAN/data/2.input_equipo/dados_brutos'

outPath = '/media/leohoinaski/HDD/CLEAN/data/Outputs'


pollutants=['O3','CO','NO2','SO2']

samplePerctg=0.5

nIteration = 1000

op = 'raw'

deviceId = '01'

dataModel = pd.DataFrame()
dataBestModel = pd.DataFrame()

for pollutant in pollutants:
    
    refData = REFprepData.mainREFprepData(Reffolder_path,pollutant)
    dataModel['ref_'+pollutant] =  refData
    
    cleanData = CLEANprepData.mainCLEANprepData(CLEANfolder_path,pollutant,op)
    dataModel[pollutant] =  cleanData
    
    merge=pd.merge(cleanData,refData, how='inner', left_index=True, right_index=True)
    
    stats,table,bestSample = CLEANstats.statistics(merge,samplePerctg,nIteration)
    dataBestModel['ref_'+pollutant] =  bestSample['ref'].drop_duplicates()
    dataBestModel[pollutant] =  cleanData['timeseries'].drop_duplicates()
    
    #CLEANfigures.scatterCLEANvsREF(bestSample)
    
    # cleanDataboots = CLEANprepData.mainCLEANprepDataBootstrap(CLEANfolder_path,pollutant,bestSample)

    # merge2=pd.merge(cleanDataboots,refData, how='inner', left_index=True, right_index=True)
    
    # stats,table,bestSample2 = CLEANstats.statistics(merge2,samplePerctg,nIteration)
    
    #CLEANfigures.plotCLEANvsREF(bestSample2,pollutant)

    print(table)
    
for pollutant in pollutants:
    #model = CLEANmodel.CLEANann(dataBestModel,pollutant)
    #model = CLEANmodel.CLEANrandomForest (dataModel,pollutant)
    models = CLEANmodel.CLEANbestModel(dataBestModel,pollutant)
    bestModel = CLEANmodel.modelsEvaluation(dataModel,models,pollutant)
    CLEANfigures.scatterModelvsObs(dataModel,bestModel,pollutant)
    CLEANmodel.saveModel(outPath,pollutant,deviceId,1,bestModel)