#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 13:44:39 2023

@author: leohoinaski
"""

import scipy
import pandas as pd
import numpy as np

def statistics(merge):
    rho, rho_pval = scipy.stats.spearmanr(merge['timeseries'],
                 merge['ref'], axis=0, nan_policy='omit')
    
    stats = pd.DataFrame(dict(rho=[], rho_pval=[]), dtype=float)
    stats= stats.append(dict(rho=rho, rho_pval=rho_pval), ignore_index=True)
    corr = [weighted_bootstrap_corr(merge,'ref','timeseries')  for i in range(201)]
    table = summarize(corr, digits=3)
    return stats, table

def weighted_bootstrap_corr(df, var1, var2):
    n = len(df)
    sample = df.sample(n=n, replace=True, weights='ref')
    rho, rho_pval = scipy.stats.spearmanr(sample[var1],
                 sample[var2], axis=0, nan_policy='omit')
    
    corr = sample[var1].corr(sample[var2])
    return rho


def summarize(t, digits=2):
    table = pd.DataFrame(columns=['Estimate', 'SE', 'CI90'])
    est = np.mean(t).round(digits)
    SE = np.std(t).round(digits)
    CI90 = np.percentile(t, [5, 95]).round(digits)
    table.loc[''] = est, SE, CI90
    return table

