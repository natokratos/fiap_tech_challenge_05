import os
import glob
import shutil
import platform 
import time
import datetime
import psycopg2
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn import preprocessing
from sklearn import utils
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.utils.validation import check_is_fitted
from sklearn.exceptions import NotFittedError
import joblib

model = LinearRegression()

class Pipeline:

    def __init__(self):
        self.database = 'app'
        self.table = 'ml.raw_data'
        self.metric_date = ''
        self.model = LinearRegression()
        self.model_dump = bytes()
        self.x_train = {}
        self.x_test = {}
        self.y_train = {}
        self.y_test = {}

        try:
            connection = psycopg2.connect(database=self.database, user='postgres', password='postgres', host="172.30.0.2", port=5432)
            connection.autocommit = True
        except:
            print(f"Nao consegui conectar ao banco de dados ({self.database}, 172.30.0.2)")
            return

        # Read data into a Pandas DataFrame
        df = pd.read_sql(f'SELECT * FROM {self.table}', con=connection)

        le = preprocessing.LabelEncoder()
        df['codigo'] = le.fit_transform(df['codigo'])
        #df['acao'] = le.fit_transform(df['acao'])
        #df['tipo'] = le.fit_transform(df['tipo'])
        ##df['codigo'] = utils.multiclass.type_of_target(df['codigo'].astype('int'))
        self.metric_date = df['data'][0]
        remove_columns = ['data', 'acao', 'tipo']
        df = df.drop(remove_columns, axis=1)
        #rows, cols = df.shape
        #print(f'Linhas: {rows}. Colunas: {cols}')     
        # Prepare the data
        x = df.drop('qtdeteorica', axis = 1)
        #y = df['part']
        y = df['qtdeteorica']

        # normalização dos dados
        #min_max_scaler = StandardScaler()
        #x = min_max_scaler.fit_transform(x)        
        
        # Split the data into training and testing sets
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(x, y, test_size=0.2, random_state=23)

        # Create a logistic regression model
        #self.model = LinearRegression()

        # Close the connection
        connection.close()

    def train(self):
        print(f"Treinando o modelo")

        # Train the model
        self.model.fit(self.x_train, self.y_train)
        try:
            check_is_fitted(self.model)
            self.model_dump = joblib.dump(self.model, 'src/.model.dump')
        except NotFittedError as exc:
            print(f"Model is not fitted yet.")

    def predict(self):
        print(f"Predicao")

        try:
            self.model = joblib.load('src/.model.dump')
            check_is_fitted(self.model)
        except NotFittedError as exc:
            print(f"Model is not fitted yet.")
        y_pred = self.model.predict(self.x_test)

        r2score = r2_score(self.y_test, y_pred)
        # Evaluate the model
        mse = mean_squared_error(self.y_test,y_pred)
        rmse = np.sqrt(mse)
        mape = mean_absolute_percentage_error(self.y_test,y_pred)

        # try:
        #     connection = psycopg2.connect(database=self.database, user='postgres', password='postgres', host="localhost", port=5432)
        #     connection.autocommit = True
        # except:
        #     return "Nao consegui conectar ao banco de dados"
        
        # cursor = connection.cursor()

        # try:
        #     cursor.execute(f"INSERT INTO METRICS (data, mse, rmse, mape) VALUES ('{self.metric_date}', {mse}, {rmse}, {mape})")
        # except:
        #     return f"Nao consegui　inserir os dados referentes as metricas no banco de dados: DATE [INSERT INTO METRICS (date, mse, rmse, mape) VALUES ({self.metric_date}, {mse}, {rmse}, {mape})]"

        #return f"DATE: {self.metric_date} MSE: {mse} RMSE {rmse} MAPE {mape}"
        return self.metric_date, r2score, mse, rmse, mape, self.model.coef_, self.model.intercept_, self.x_test.astype('str'), self.y_test.astype('str'), y_pred, y_pred.astype('str')