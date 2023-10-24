import requests
import pandas as pd
import datetime as dt
import json

class GetSensorDataService:
    def __init__(self, host, port, endpoint) -> None:
        self.__endpoint = 'http://' + host + ':' + str(port) + endpoint

    def get_json_data_from_sensor_id(self, id):
        return requests.get(self.__endpoint + str(id))
    
    def get_data_from_file(self, filename, sensor_name):
        df = pd.read_csv(filename)
        date_time_col = ['Year','Month','Day','Hour','Minute','Second']
        df['DateTime'] = (pd.to_datetime(df[date_time_col], infer_datetime_format=False, format='%d/%m/%Y/%H/%M/%S'))
        df = df.drop(columns=date_time_col)
        df = df.drop(columns=['Altitude', 'Device', 'DeviceSt', ' SensorID'])
        df = df.rename(columns={'Value': 'measuring', 'Latitude': 'latitude', 'Longitude': 'longitude'})
        df = (df.where(df['DateTime'] > dt.datetime(2020, 1, 1, 0, 0, 0))
                .where(df['DateTime'] <= dt.datetime.now()).dropna())
        path = "data/input/"
        df.to_csv(path + sensor_name + 'web_dataframe.csv') 
        return df
    
    def get_samples_by_sensor(HTTP_REQUEST_MAIN,sensor_id):
        """
        
        Fernando,
        Essa função deveria escolher a data para coletar os dados e não todo 
        o conjunto. Se carregar tudo em response_dataframe, pode ficar pesado. 

        Parameters
        ----------
        HTTP_REQUEST_MAIN : TYPE
            DESCRIPTION.
        sensor_id : TYPE
            DESCRIPTION.

        Returns
        -------
        response_dataframe : TYPE
            DESCRIPTION.

        """
        response_json = requests.get(HTTP_REQUEST_MAIN + str(sensor_id))
        response_dict = json.loads(response_json.content)
        response_dataframe = pd.DataFrame.from_dict(response_dict)
        print(response_dataframe[["date","measuring"]])
        return response_dataframe


