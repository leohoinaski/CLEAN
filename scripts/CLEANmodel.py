#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:31:56 2023

@author: leohoinaski
"""

import numpy as np
import os


def CLEANbestModel(dataBestModel,pollutant,outPath,deviceId,sensor):
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
    
    cols = dataBestModel.columns.values
    rcol=[]
    for col in cols:
        if col.startswith('ref')==False:
            rcol.append(col)
    rcol.append('ref_'+pollutant)
    covariates = '_'.join(rcol[:-1])  
    
    bestSample = dataBestModel[rcol]
    X = np.array(bestSample.dropna()[rcol[:-1]])
    y = np.array(bestSample.dropna()[rcol[-1]]).ravel()
    
    scorei=-100
    models=[]
    for item in classifiers:
        #print(item)
        model = item
        model.fit(X,y)
        saveAllModels(outPath,pollutant,covariates,deviceId,sensor,model,
                      str(dataBestModel.index.min()))
        score = model.score(X,y)
        #print(score)
        if score>scorei:
            scorei=score
            bestModel = model
        models.append(model)
    print('-------Best model-------')
    print(bestModel)
    print(scorei)
    
    return models


def modelsEvaluation(dataModel,models,pollutant):
    cols = dataModel.columns.values
    rcol=[]
    for col in cols:
        if col.startswith('ref')==False:
            rcol.append(col)
    rcol.append('ref_'+pollutant)
            
    bestSample = dataModel[rcol]
    X = np.array(bestSample.dropna()[rcol[:-1]])
    y = np.array(bestSample.dropna()[rcol[-1]]).ravel()
    scorei=-100
    bestModel=[]
    for model in models:
        print(model)
        score = model.score(X,y)
        print(score)
        if score>scorei:
            scorei=score
            bestModel = model
    print('-------Best model-------')
    print(bestModel)
    print(scorei)
    
    return bestModel


def saveAllModels(outPath,pollutant,covariates,deviceId,sensor,model,calibDate):    
    import joblib
    covariates = '_'.join(covariates) 
    os.makedirs(outPath+'/Calibration/'+str(deviceId)+'/allModels', exist_ok=True)
    with open(outPath+'/Calibration/'+str(deviceId)+'/allModels/CLEAN_model-'+
              str(model).split('(')[0]+'_id-'+str(deviceId)+'_Sensor-'+str(sensor)+
              '_target-'+pollutant+'_covariates-'+covariates+'_calib-'+calibDate, 'wb') as f:
        joblib.dump(model, f)
    
    return model


def saveBestModel(outPath,pollutant,covariates,deviceId,sensor,model):    
    import joblib
    covariates = '_'.join(covariates) 
    os.makedirs(outPath+'/Calibration/'+str(deviceId)+'/bestModel', exist_ok=True)
    with open(outPath+'/Calibration/'+str(deviceId)+'/bestModel/CLEAN_bestModel_'+
              str(model).split('(')[0]+'_id-'+str(deviceId)+'_Sensor-'+str(sensor)+
              '_target-'+pollutant+'_covariates-'+covariates, 'wb') as f:
        joblib.dump(model, f)
    
    return model

def CLEANpredict(outPath,pollutant,deviceId,sensor,signal):
    import joblib
    model = joblib.load(outPath+'/Calibration/'+str(deviceId)+'/CLEANmodel_'+\
              str(deviceId)+'_'+pollutant+'_'+str(sensor))
    preds = model.predict(np.array(signal).reshape(-1,1))
    
    return preds


