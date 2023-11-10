#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:31:56 2023

@author: leohoinaski
"""

import numpy as np
import os
import pandas as pd
import ismember
from contextlib import redirect_stdout
from sklearn.metrics import mean_absolute_error,mean_squared_error,accuracy_score
import scipy.stats

def CLEANbestModel(dataBestModel,pollutant,outPath,deviceId,sensor,covariates):
    from sklearn.tree import DecisionTreeRegressor
    from sklearn import linear_model
    from sklearn.neural_network import MLPRegressor
    from sklearn import svm
    from sklearn.ensemble import RandomForestRegressor
    from sklearn import neighbors
    

    classifiers = [
        DecisionTreeRegressor(max_depth=3, random_state=0),
        neighbors.KNeighborsRegressor(n_neighbors=5, weights='distance'),
        RandomForestRegressor(n_estimators=500,max_depth=2, random_state=40),
        svm.SVR(),
        MLPRegressor(random_state=1, max_iter=1000),
        linear_model.SGDRegressor(),
        linear_model.BayesianRidge(),
        linear_model.LassoLars(),
        linear_model.ARDRegression(),
        linear_model.PassiveAggressiveRegressor(),
        linear_model.TheilSenRegressor(),
        linear_model.LinearRegression()]
   
    df_models = pd.DataFrame()   
    df_models['model'] = np.zeros(len(classifiers))
    df_models['score'] = np.zeros(len(classifiers))
    df_models['covariates'] = np.zeros(len(classifiers))
        
    # cols = dataBestModel.columns.values
    # rcol=[]
    # for col in cols:
    #     if col.startswith('ref')==False:
    #         rcol.append(col)
    # rcol.append('ref_'+pollutant)
    # #covariates = '_'.join(rcol[:-1])  
    
    bestSample = dataBestModel[covariates]
    X = np.array(bestSample.dropna()[covariates[:-1]])
    y = np.array(bestSample.dropna()[covariates[-1]]).ravel()
    
    scorei=-100
    models=[]
    for ii,item in enumerate(classifiers):
        print(item)
        model = item
        model.fit(X,y)
        saveAllModels(outPath,pollutant,covariates,deviceId,sensor,model,
                      str(dataBestModel.index.min()))
        score = model.score(X,y)
        df_models['model'][ii] = str(model).split('(')[0]
        df_models['score'][ii] = score
        df_models['covariates'][ii] = '_'.join(covariates[:-1]) 

        # with open(outPath+'/modelsScores/'+
        #     'modelsummary'+'_target-'+pollutant+'_covariates-'+'-'.join(covariates[:-1]) +'.txt', 'w') as f:
        #     with redirect_stdout(f):
        #         model.summary()

        #print(score)
        if score>scorei:
            scorei=score
            bestModel = model
        models.append(model)
    print('-------Best model-------')
    print(bestModel)
    print(scorei)

    return models


def modelsEvaluation(dataModel,dataBestModel,models,pollutant):
    cols = dataModel.columns.values
    rcol=[]
    for col in cols:
        if col.startswith('ref')==False:
            rcol.append(col)
    rcol.append('ref_'+pollutant)
            
    #bestSample = dataModel[rcol]
    dataAll = dataModel[rcol].copy()
    dataTrain = dataBestModel[rcol].copy()
    dataTest = pd.merge(dataAll,dataTrain, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)

    X = np.array(dataTest.dropna()[rcol[:-1]])
    y = np.array(dataTest.dropna()[rcol[-1]]).ravel()
    scorei=-100
    bestModel=[]
    df_models = pd.DataFrame()   
    df_models['model'] = np.zeros(len(models))
    df_models['score'] = np.zeros(len(models))
    df_models['bias'] = np.zeros(len(models))
    df_models['mae'] = np.zeros(len(models))
    df_models['mse'] = np.zeros(len(models))
    #df_models['accuracy'] = np.zeros(len(models))
    df_models['spearman']= np.zeros(len(models))
    df_models['spearman_pval']= np.zeros(len(models))
    df_models['covariates'] = np.zeros(len(models))
    for ii, model in enumerate(models):
        print(model)
        score = model.score(X,y)
        df_models['model'][ii] = str(model).split('(')[0]
        df_models['score'][ii] = score
        preds = model.predict(np.array(X))
        df_models['bias'][ii] = np.nanmean(preds-y)
        df_models['mae'][ii] = mean_absolute_error(y, preds)
        df_models['mse'][ii] = mean_squared_error(y, preds)
        #df_models['accuracy'][ii] = accuracy_score(y, preds)
        corr, p_value = scipy.stats.spearmanr(y, preds)
        df_models['spearman'][ii] =corr
        df_models['spearman_pval'][ii] =p_value
        
        df_models['covariates'][ii] = '-'.join(rcol[:-1]) 
        print(score)
        if score>scorei:
            scorei=score
            bestModel = model
    print('-------Best model-------')
    print(bestModel)
    print(scorei)

    
    return bestModel,df_models,dataTest,dataTrain


def saveAllModels(outPath,pollutant,covariates,deviceId,sensor,model,calibDate):    
    import joblib
    covariates = '-'.join(covariates[:-1]) 
    os.makedirs(outPath+'/allModels/'+pollutant, exist_ok=True)
    with open(outPath+'/allModels/'+pollutant+'/CLEAN_model-'+
              str(model).split('(')[0]+'_id-'+str(deviceId)+'_Sensor-'+str(sensor)+
              '_target-'+pollutant+'_covariates-'+covariates+'_calib-'+calibDate, 'wb') as f:
        joblib.dump(model, f)
    
    return model


def saveBestModel(outPath,pollutant,covariates,deviceId,sensor,model):    
    import joblib
    covariates = '-'.join(covariates) 
    os.makedirs(outPath+'/bestModel/'+pollutant, exist_ok=True)
    with open(outPath+'/bestModel/'+pollutant+'/CLEAN_bestModel-'+
              str(model).split('(')[0]+'_id-'+str(deviceId)+'_Sensor-'+str(sensor)+
              '_target-'+pollutant+'_covariates-'+covariates, 'wb') as f:
        joblib.dump(model, f)
    
    return model


def CLEANpredict(outPath,pollutant,deviceId,sensor,df_covariates):
    import joblib
    # data = {'NO2': [2], 'SO2': [4],'PM10': [4]}
    # df_covariates=pd.DataFrame(data)
    path = outPath+'/modelsScores'
    files = os.listdir(path)
    for file in files:
        if file.startswith('modelsScores_'+pollutant):
            scores = pd.read_csv(path+'/'+file).sort_values('score', ascending=False)
        
    s1 = pd.Series(df_covariates.columns)
    for index, row in scores.iterrows():
        lia,loc = ismember.ismember(row.covariates.split('-'),s1)
        if lia.all():
            print('This is the model: ' + row.model + ' - ' + row.covariates)
            model = joblib.load(outPath+'/bestModel/'+pollutant+'/CLEAN_bestModel-'+
                      str(row.model)+'_id-'+str(deviceId)+'_Sensor-'+str(sensor)+
                      '_target-'+pollutant+'_covariates-'+row.covariates)
            break
        else:
            #print('Model not found')
            model=[]
    
    coValues = np.array(df_covariates[row.covariates.split('-')]).reshape(1, -1)   
    preds = model.predict(np.array(coValues))
    
    
    return preds,model


