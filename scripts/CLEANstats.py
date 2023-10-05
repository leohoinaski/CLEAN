#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 13:44:39 2023

@author: leohoinaski
"""

import scipy

def my_statistic(x, y):
    rho = scipy.stats.spearmanr(x, y, axis=0, nan_policy='omit')
    return rho

rng = np.random.default_rng()
res = scipy.stats .bootstrap((merge['timeseries'].values,merge['ref'].values), my_statistic, 
                             vectorized=False, paired=True, random_state=rng)

my_statistic(merge['timeseries'][1:100],
             merge['ref'][1:100])
