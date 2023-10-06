#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:31:56 2023

@author: leohoinaski
"""

from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression

def mainCLEANmodel (merge):
    merge3 = merge.dropna(axis='rows')
    X, y = make_regression(n_features=4, n_informative=2,
                            random_state=0, shuffle=False)
    regr = RandomForestRegressor(max_depth=2, random_state=0)
    regr.fit(np.array(merge3['timeseries']).reshape(-1, 1),
            np.array(merge3['ref']).reshape(-1, 1))
    print(regr.predict(merge3['timeseries']).reshape(-1, 1))
    regr.score(np.array(merge3['timeseries']).reshape(-1, 1),
            np.array(merge3['ref']).reshape(-1, 1))
    return regr


