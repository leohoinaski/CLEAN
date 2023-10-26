import json
from random import randint
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from .CLEANpredict import mainCLEANpredict
from .GetSensorDataService import GetSensorDataService
import os
import numpy as np

class GraphConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
		# deviceId = 1
		# sensor = 1
		# pollutant = 'O3'
		# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		# # #print(BASE_DIR)
		# outPath = BASE_DIR+ '/static'
		# # print(outPath)

		# preds,model,df_covariates = mainCLEANpredict(outPath,pollutant,deviceId,sensor)

		# print(preds)

		# for i,pred in enumerate(preds):

		# 	await self.send(json.dumps({'value': pred}))
		# 	await sleep(1)
	
		ALPHA_OX_1_ID      =  135
		HOST = "renovar.lcqar.ufsc.br"
		PORT = 8080
		GET_SAMPLES_BY_SENSOR = "/sample/sensor/all/"
		HTTP_REQUEST_MAIN = 'http://' + HOST + ':' + str(PORT) + GET_SAMPLES_BY_SENSOR
		sensor_service = GetSensorDataService(HOST, PORT)

		sensor_data = sensor_service.get_samples_by_sensor(ALPHA_OX_1_ID)
		for value in sensor_data['measuring']:
			await self.send(json.dumps({'value': value}))
			await sleep(1)
