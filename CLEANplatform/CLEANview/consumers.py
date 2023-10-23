import json
from random import randint
from asyncio import sleep
from channels.generic.websocket import AsyncWebsocketConsumer
from .CLEANpredict import mainCLEANpredict
import os
import numpy as np

class GraphConsumer(AsyncWebsocketConsumer):
	async def connect(self):
		await self.accept()
		deviceId = 1
		sensor = 1
		pollutant = 'O3'
		BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
		#print(BASE_DIR)
		outPath = BASE_DIR+ '/static'
		print(outPath)

		preds,model,df_covariates = mainCLEANpredict(outPath,pollutant,deviceId,sensor)

		print(preds)

		for i,pred in enumerate(preds):

			await self.send(json.dumps({'value': pred,'date': df_covariates.index[i]}))
			await sleep(1)
