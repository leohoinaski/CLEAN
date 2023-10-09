#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:31:56 2023

@author: leohoinaski
"""

import numpy as np
import os



def CLEANrandomForest (dataBestModel, pollutant):
    from sklearn.ensemble import RandomForestRegressor
    import forestci as fci
    n_trees = 500
    
    cols = dataBestModel.columns.values
    rcol=[]
    for col in cols:
        if col.startswith('ref')==False:
            rcol.append(col)
    rcol.append('ref_'+pollutant)
            
    bestSample = dataBestModel[rcol]
    X = np.array(bestSample.dropna()[rcol[:-1]])
    y = np.array(bestSample.dropna()[rcol[-1]]).ravel()
    model = RandomForestRegressor(n_estimators=n_trees,max_depth=2, random_state=40).fit(X, y)
    model.score(X,y)

    
    # model_ci = fci.random_forest_error(model,
    #                                    np.array(merge3.dropna().timeseries).reshape(-1, 1),
    #                                    np.array(merge.dropna().timeseries).reshape(-1, 1))

    return model

def CLEANsvm(dataBestModel, pollutant):
    from sklearn.pipeline import make_pipeline
    from sklearn import svm
    from sklearn.preprocessing import StandardScaler
    cols = dataBestModel.columns.values
    rcol=[]
    for col in cols:
        if col.startswith('ref')==False:
            rcol.append(col)
    rcol.append('ref_'+pollutant)
            
    bestSample = dataBestModel[rcol]
    X = np.array(bestSample.dropna()[rcol[:-1]])
    y = np.array(bestSample.dropna()[rcol[-1]]).ravel()
    model = make_pipeline(StandardScaler(), svm.SVC(gamma='auto'))
    model = svm.SVR()
    model.fit(X.astype('int'), y)
    model.score(X.astype('int'),y)
    
    return model

def CLEANann(dataBestModel, pollutant):
    from sklearn.neural_network import MLPRegressor
    cols = dataBestModel.columns.values
    rcol=[]
    for col in cols:
        if col.startswith('ref')==False:
            rcol.append(col)
    rcol.append('ref_'+pollutant)
            
    bestSample = dataBestModel[rcol]
    X = np.array(bestSample.dropna()[rcol[:-1]])
    y = np.array(bestSample.dropna()[rcol[-1]]).ravel()
    model = MLPRegressor(random_state=1, max_iter=1000).fit(X, y)
    model.score(X,y)
    
    return model

def CLEANbestModel(dataBestModel,pollutant):
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
            
    bestSample = dataBestModel[rcol]
    X = np.array(bestSample.dropna()[rcol[:-1]])
    y = np.array(bestSample.dropna()[rcol[-1]]).ravel()
    scorei=0
    models=[]
    for item in classifiers:
        #print(item)
        model = item
        model.fit(X,y)
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
    scorei=0
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

def saveModel(outPath,pollutant,deviceId,sensor,model):    
    import joblib
    os.makedirs(outPath+'/Calibration/'+str(deviceId), exist_ok=True)
    with open(outPath+'/Calibration/'+str(deviceId)+'/CLEANmodel_'+
              str(deviceId)+'_'+pollutant+'_'+str(sensor), 'wb') as f:
        joblib.dump(model, f)
    
    return model


def CLEANpredict(outPath,pollutant,deviceId,sensor,signal):
    import joblib
    model = joblib.load(outPath+'/Calibration/'+str(deviceId)+'/CLEANmodel_'+\
              str(deviceId)+'_'+pollutant+'_'+str(sensor))
    preds = model.predict(np.array(signal).reshape(-1,1))
    
    
    return preds