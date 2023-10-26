#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 13:55:01 2023

@author: leohoinaski
"""
import joblib
import os
import pandas as pd
import numpy as np
import ismember
from .GetSensorDataService import GetSensorDataService
from django.views.decorators.csrf import csrf_exempt

def CLEANpredict(outPath,pollutant,deviceId,sensor,df_covariates):
    """
    Essa função retorna a concentração de poluentes e melhor modelo de calibração
    para corrigir as medições dos equipamentos CLEAN. Como requisito, 
    o usuário precisará rodar o script mainCLENcalibration para prover os modelos
    e seus respectivos ranqueamentos (scores). O modelo com melhor score será
    selecionado para um dado conjunto de inputs contidos no df_covariates. Logo,
    é importante que as colunas deste dataFrame tenham os mesmos nomes utilizados
    na calibração. 

    Parameters
    ----------
    outPath : String
        caminho para a pasta com os outputs da calibração
    pollutant : String
        Poluente para se estimado
    deviceId : Integer
        Numero ou código do CLEAN monitor.
    sensor : Integer
        Número do sensor dentro do CLEAN monitor. Usar 1 se existir apenas
        um sensor para o poluente.
    df_covariates : DataFrame
        Dataframe com os dados coletados no CLEAN monitor que serão utilizados 
        no modelo. ESTE DATAFRAME DEVE CONTER APENAS UMA LINHA!

    Returns
    -------
    preds : Numpy array
        Concentração prevista para o poluente
    model : objeto
        Modelo de calibração utilizado para estimativa da concentração do poluente.

    """
    # Remove as colunas com NaN
    # Aqui podemos pensar em remover colunas com dados ruins tb (fora dos 
    # limites do conjunto de calibração)
    
    df_covariates = df_covariates.dropna(axis='columns')

    path = outPath+'/Calibration/'+str(deviceId).zfill(2)+'/modelsScores'
    files = os.listdir(path)
    for file in files:
        if file.startswith('modelsScores_'+pollutant):
            scores = pd.read_csv(path+'/'+file).sort_values('score', ascending=False)
        
    s1 = pd.Series(df_covariates.columns)
    for index, row in scores.iterrows():
        lia,loc = ismember.ismember(row.covariates.split('-'),s1)
        if lia.all():
            print('This is the model: ' + row.model + ' - ' + row.covariates)
            print('-')
            print(outPath+'/Calibration/'+str(deviceId).zfill(2)+'/bestModel/'+pollutant+'/CLEAN_bestModel-'+
                      str(row.model)+'_id-'+str(deviceId).zfill(2)+'_Sensor-'+str(sensor).zfill(2)+
                      '_target-'+pollutant+'_covariates-'+row.covariates)
            print('-')
            model = joblib.load(outPath+'/Calibration/'+str(deviceId).zfill(2)+'/bestModel/'+pollutant+'/CLEAN_bestModel-'+\
                      str(row.model)+'_id-'+str(deviceId).zfill(2)+'_Sensor-'+str(sensor).zfill(2)+\
                      '_target-'+pollutant+'_covariates-'+row.covariates)

            break
        else:
            #print('Model not found')
            model=[]
    
    coValues = np.array(df_covariates[row.covariates.split('-')])  
    preds = model.predict(np.array(coValues))
    
    
    return preds,model


@csrf_exempt
def mainCLEANpredict(outPath,pollutant,deviceId,sensor):

    TEMPERATURE_ID     =  130
    PRESSURE_ID        =  131
    ALPHA_CO_ID        =  132
    ALPHA_NO2_ID       =  133
    ALPHA_SO2_1_ID     =  134
    ALPHA_OX_1_ID      =  135
    ALPHA_OX_2_ID      =  136
    ALPHA_SO2_2_ID     =  137
    EXT_TEMPERATURE_ID =  138
    EXT_HUMIDITY_ID    =  139
    PM10_ID            =  140
    PM25_ID            =  141
    PM01_ID            =  142
    OPC_TEMPERATURE_ID =  143
    OPC_HUMIDITY_ID    =  144

    HOST = "renovar.lcqar.ufsc.br"
    PORT = 8080
    GET_SAMPLES_BY_SENSOR = "/sample/sensor/all/"
    HTTP_REQUEST_MAIN = 'http://' + HOST + ':' + str(PORT) + GET_SAMPLES_BY_SENSOR
    sensor_service = GetSensorDataService(HOST, PORT)

    sensor_data = sensor_service.get_samples_by_sensor(ALPHA_OX_1_ID)

    df_covariates = sensor_data

    df_covariates.columns=[pollutant]

    preds,model = CLEANpredict(outPath,pollutant,deviceId,sensor,df_covariates)

    return preds,model,df_covariates



#mainCLEANpredict(outPath,'O3',1,1)