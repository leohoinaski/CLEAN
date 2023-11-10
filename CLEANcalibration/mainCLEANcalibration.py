#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 14:34:39 2023

@author: leohoinaski
"""
from REFprepData import mainREFprepData
from CLEANprepData import mainCLEANprepData
from CLEANstats  import statistics
import CLEANfigures 
import pandas as pd
from CLEANmodel import CLEANbestModel, modelsEvaluation, saveBestModel
from itertools import combinations
import shutil
import os


def mainCLEANcalibration(BASE,deviceId,CLEANpollutants,REFpollutants,sensor,
                         samplePerctg,nIteration,op):

#------------------------------PROCESSING--------------------------------------
    # Directories
    
    CLEANfolder_path = BASE + "/media/calibration/"+ str(deviceId) +'/Inputs/CLEAN'
    Reffolder_path = BASE + "/media/calibration/"+ str(deviceId) +'/Inputs/Reference'
    outPath = BASE + "/media/calibration/"+ str(deviceId) +'/Outputs'

    if os.path.isdir(outPath+'/bestModel/'):
        shutil.rmtree(outPath+'/bestModel/')

    os.makedirs(outPath+'/modelsScores/', exist_ok=True)
    os.makedirs(outPath+'/figures/', exist_ok=True)

    dataModel = pd.DataFrame()
    dataBestModel = pd.DataFrame()

    pollutants= list(set(CLEANpollutants) | set(REFpollutants))


    # Loop for each pollutant
    for pollutant in REFpollutants:
        # Reference data
        refData = mainREFprepData(Reffolder_path,pollutant)
        dataModel['ref_'+pollutant] =  refData
        
        for cleanpol in CLEANpollutants:
            # CLEAN data
            cleanData = mainCLEANprepData(CLEANfolder_path,cleanpol,op)
            dataModel[cleanpol] =  cleanData
        
        # Merging DataFrames
        merge=pd.merge(dataModel,refData, how='inner', left_index=True, right_index=True)
        #merge = merge.rename(columns={'ref': 'ref_'+pollutant})
        merge = merge.drop('ref', axis=1)
        print(merge)
        
        # Get best sample for training
        stats,table,dataBestModel = statistics(merge,samplePerctg,nIteration,pollutant)
        print(table)
        
        # Extracting data 
        dataBestModel = dataBestModel.rename(columns={'ref': 'ref_'+pollutant})

        #dataBestModel['ref_'+pollutant] =  bestSample['ref'].drop_duplicates()

        #dataBestModel[pollutant] =  cleanData['timeseries'].drop_duplicates()

        # CLEANfigures.scatterCLEANvsREF(bestSample)
        
        # cleanDataboots = CLEANprepData.mainCLEANprepDataBootstrap(CLEANfolder_path,pollutant,bestSample)

        # merge2=pd.merge(cleanDataboots,refData, how='inner', left_index=True, right_index=True)
        
        # stats,table,bestSample2 = CLEANstats.statistics(merge2,samplePerctg,nIteration)
        
        # CLEANfigures.plotCLEANvsREF(bestSample2,pollutant)


        covariates = CLEANpollutants
        polcombs = sum([list(map(list, combinations(covariates, i))) for i in range(len(covariates) + 1)], [])
         
        all_models=[]
        for combs in polcombs:
            if any(pollutant in s for s in combs):
                #print(combs)
                combi=combs.copy()
                combi.append('ref_'+pollutant)
                print(combi)
                models = CLEANbestModel(dataBestModel[combi],pollutant,outPath,deviceId,sensor,combi)
                bestModel,df_models,dataTest,dataTrain = modelsEvaluation(dataModel[combi],dataBestModel,models,pollutant)
                os.makedirs(outPath+'/trainAndTest', exist_ok=True)
                dataTest.to_csv(outPath+'/trainAndTest/test_'+
                         '-'.join(combi) +'.csv', index=False)
                dataTrain.to_csv(outPath+'/trainAndTest/train_'+
                         '-'.join(combi) +'.csv', index=False)
                all_models.append(df_models)
                #CLEANfigures.scatterModelvsObs(dataTest,bestModel,pollutant)
                fig = CLEANfigures.modelScatterplot(dataTest,bestModel,pollutant)
                fig.savefig(outPath+'/figures/modelScatterplot_'+
                                      str(bestModel).split('(')[0]+
                                      '_id-'+str(deviceId)+
                                      '_Sensor-'+str(sensor)+
                                      '_target-'+pollutant+
                                      '_covariates-'+'-'.join(combi[:-1]) )
                saveBestModel(outPath,pollutant,combi[:-1],deviceId,sensor,bestModel)
        df_models = pd.concat(all_models).sort_values('score', ascending=False)
        df_models.to_csv(outPath+'/modelsScores/modelsScores_'+
                         pollutant+'.csv', index=False)
            
    return pollutants





CLEANpollutants=['O3','CO','NO2','SO2']
REFpollutants=['O3','CO','NO2','SO2']
samplePerctg=0.5 # Percentage of data for training 
nIteration = 1000 # Number of random samples
op = 'raw' # option to data preparing
deviceId = '01' # Device Identification
sensor ='01'
BASE= '/media/leohoinaski/HDD/CLEAN'
#BASE= '/media/leohoinaski/HDD/CLEAN' 
BASE = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

mainCLEANcalibration(BASE,deviceId,CLEANpollutants,REFpollutants,sensor,
                          samplePerctg,nIteration,op)