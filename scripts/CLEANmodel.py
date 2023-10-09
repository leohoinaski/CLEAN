#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:31:56 2023

@author: leohoinaski
"""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
import joblib
import os
import forestci as fci


def CLEANrandomForest (dataBestModel, pollutant):
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


def saveModel(outPath,pollutant,deviceId,sensor,model):    
    os.makedirs(outPath+'/Calibration/'+str(deviceId), exist_ok=True)
    with open(outPath+'/Calibration/'+str(deviceId)+'/CLEANmodel_'+
              str(deviceId)+'_'+pollutant+'_'+str(sensor), 'wb') as f:
        joblib.dump(model, f)
    
    return model


def CLEANpredict(outPath,pollutant,deviceId,sensor,signal):
    model = joblib.load(outPath+'/Calibration/'+str(deviceId)+'/CLEANmodel_'+\
              str(deviceId)+'_'+pollutant+'_'+str(sensor))
    preds = model.predict(np.array(signal).reshape(-1,1))
    
    
    return preds