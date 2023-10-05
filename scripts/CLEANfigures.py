#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 09:40:28 2023

@author: leohoinaski
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plotWindows(windows,timeWindows):
    
    winLen = len(windows)
    fig, ax = plt.subplots(winLen)
    stat = pd.DataFrame()
    stat['autocorr'] = np.zeros(winLen)
    stat['min']=  np.zeros(winLen)
    stat['max'] =  np.zeros(winLen)
    stat['mean']=  np.zeros(winLen)
    stat['std'] = np.zeros(winLen)

    for ii in range(0,winLen):
        ax[ii].plot(timeWindows[ii],windows[ii])
        print(np.isnan(windows[ii]).sum())
        #print(np.(windows[ii], windows[ii], mode='full'))
        #stat['autocorr'][ii] = np.correlate(windows[ii], windows[ii], mode='full')
        stat['min'][ii] = np.nanmin(windows[ii])
        stat['max'][ii] = np.nanmax(windows[ii])
        stat['mean'][ii] = np.nanmax(windows[ii])
        stat['std'][ii] = np.nanstd(windows[ii])
        

    fig, ax = plt.subplots()
    
    for ii in range(0,winLen):
        ax.plot(timeWindows[ii],windows[ii])
        print(np.isnan(windows[ii]).sum())
        
    # fig, ax = plt.subplots(winLen)
    # for ii in range(0,winLen):
    #     data = pd.DataFrame()
    #     data['timeseries'] = windows[ii]
    #     data_filled = data.fillna(np.nanmean(windows[ii]))
    #     gtsa.plot_acf(data_filled, lags=len(windows[ii])-1, alpha=0.05, missing ='raise',
    #                  title='',ax = ax[ii])
    
    # fig, ax = plt.subplots(winLen)
    # for ii in range(0,winLen):
    #     data = pd.DataFrame()
    #     data['timeseries'] = windows[ii]
    #     data_filled = data.fillna(np.nanmean(windows[ii]))
    #     gtsa.plot_pacf(data_filled, lags=len(windows[ii])/50,  method="ywm",
    #                  title='',ax = ax[ii])

    return stat


def plotCLEANvsREF(merge):
          

    fig, ax = plt.subplots(2)
    ax[0].plot(merge['ref'],color='red')
    ax2 = ax[0].twinx()
    ax2.plot(merge['timeseries'])
    
    ax[1].scatter(merge['timeseries'],merge['ref'],color='gray',
                  s=1, alpha=0.5,edgecolors='gray')
    


    # fig, ax = plt.subplots(winLen)
    # for ii in range(0,winLen):
    #     data = pd.DataFrame()
    #     data['timeseries'] = windows[ii]
    #     data_filled = data.fillna(np.nanmean(windows[ii]))
    #     gtsa.plot_acf(data_filled, lags=len(windows[ii])-1, alpha=0.05, missing ='raise',
    #                  title='',ax = ax[ii])
    
    # fig, ax = plt.subplots(winLen)
    # for ii in range(0,winLen):
    #     data = pd.DataFrame()
    #     data['timeseries'] = windows[ii]
    #     data_filled = data.fillna(np.nanmean(windows[ii]))
    #     gtsa.plot_pacf(data_filled, lags=len(windows[ii])/50,  method="ywm",
    #                  title='',ax = ax[ii])

    return stat