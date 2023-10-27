#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:34:39 2023

@author: leohoinaski
"""
from .REFprepData import mainREFprepData
from .CLEANprepData import mainCLEANprepData
from .CLEANstats  import statistics
#from .CLEANfigures import 
import pandas as pd
from .CLEANmodel import CLEANbestModel, modelsEvaluation, saveBestModel
from itertools import combinations
import shutil
import os

#folder_path = r'C:\Users\rafab\OneDrive\Documentos\CLEAN_Calibration\data\data_clean\dados_brutos'

# PC LAB
# CLEANfolder_path = '/mnt/sdb1/CLEAN/data/Inputs/CLEAN'
# Reffolder_path = '/mnt/sdb1/CLEAN/data/Inputs/Reference/diamante'
# outPath = '/mnt/sdb1/CLEAN/data/Outputs'

# PC CASA
# Reffolder_path = '/media/leohoinaski/HDD/CLEAN/data/Inputs/Reference/diamante'
# CLEANfolder_path = '/media/leohoinaski/HDD/CLEAN/data/Inputs/CLEAN'
# outPath = '/media/leohoinaski/HDD/CLEAN/data/Outputs'


# Inputs
# pollutants=['O3','CO','NO2','SO2']
# samplePerctg=0.5 # Percentage of data for training 
# nIteration = 1000 # Number of random samples
# op = 'raw' # option to data preparing
# deviceId = '01' # Device Identification
# sensor ='01'



def mainCLEANcalibration(BASE,deviceId,CLEANpollutants,REFpollutants,sensor,samplePerctg,nIteration,op):

#------------------------------PROCESSING--------------------------------------
    # Directories
    
    CLEANfolder_path = BASE + "/media/calibration/"+ str(deviceId) +'/Inputs/CLEAN'
    Reffolder_path = BASE + "/media/calibration/"+ str(deviceId) +'/Inputs/Reference'
    outPath = BASE + "/media/calibration/"+ str(deviceId) +'/Outputs'

    dataModel = pd.DataFrame()
    dataBestModel = pd.DataFrame()

    # Loop for each pollutant
    for pollutant in REFpollutants:
        # Reference data
        refData = mainREFprepData(Reffolder_path,pollutant)
        dataModel['ref_'+pollutant] =  refData
        
        # CLEAN data
        cleanData = mainCLEANprepData(CLEANfolder_path,pollutant,op)
        dataModel[pollutant] =  cleanData
        
        # Merging DataFrames
        merge=pd.merge(cleanData,refData, how='inner', left_index=True, right_index=True)
        
        # Get best sample for training
        stats,table,bestSample = statistics(merge,samplePerctg,nIteration)
        print(table)
        
        # Extracting data 
        dataBestModel['ref_'+pollutant] =  bestSample['ref'].drop_duplicates()
        dataBestModel[pollutant] =  cleanData['timeseries'].drop_duplicates()

        # CLEANfigures.scatterCLEANvsREF(bestSample)
        
        # cleanDataboots = CLEANprepData.mainCLEANprepDataBootstrap(CLEANfolder_path,pollutant,bestSample)

        # merge2=pd.merge(cleanDataboots,refData, how='inner', left_index=True, right_index=True)
        
        # stats,table,bestSample2 = CLEANstats.statistics(merge2,samplePerctg,nIteration)
        
        # CLEANfigures.plotCLEANvsREF(bestSample2,pollutant)


    covariates = REFpollutants
    polcombs = sum([list(map(list, combinations(covariates, i))) for i in range(len(covariates) + 1)], [])
     
    if os.path.isdir(outPath+'/bestModel/'):
        shutil.rmtree(outPath+'/bestModel/')

    os.makedirs(outPath+'/modelsScores/', exist_ok=True)

    # Model for each pollutant   
    for pollutant in REFpollutants:
        all_models=[]
        for combs in polcombs:
            if any(pollutant in s for s in combs):
                #print(combs)
                combi=combs.copy()
                combi.append('ref_'+pollutant)
                print(combi)
                models = CLEANmodel.CLEANbestModel(dataBestModel[combi],pollutant,outPath,deviceId,sensor,combi)
                bestModel,df_models,dataTest,dataTrain = CLEANmodel.modelsEvaluation(dataModel[combi],dataBestModel,models,pollutant)
                os.makedirs(outPath+'/trainAndTest', exist_ok=True)
                dataTest.to_csv(outPath+'/trainAndTest/test_'+
                         '-'.join(combi) +'.csv', index=False)
                dataTrain.to_csv(outPath+'/trainAndTest/train_'+
                         '-'.join(combi) +'.csv', index=False)
                all_models.append(df_models)
                #CLEANfigures.scatterModelvsObs(dataTest,bestModel,pollutant)
                CLEANmodel.saveBestModel(outPath,pollutant,combi[:-1],deviceId,sensor,bestModel)
        df_models = pd.concat(all_models).sort_values('score', ascending=False)
        df_models.to_csv(outPath+'/modelsScores/modelsScores_'+
                         pollutant+'.csv', index=False)
            
    return covariates