import datetime
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Flatten, Input
import yfinance as yf
import joblib

class Pipeline:

    def __init__(self, retrain):
        self.symbol = 'DIS'
        self.start_date = '2020-01-01'
        self.end_date = '2025-05-01'
    
        print(f"Baixando os dados do Yahoo Finance ...\n")
        #data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        data = yf.download(self.symbol, period='max')
        print(f"data {data}")

        data = data.dropna()

        # Remove rows with '.' and convert the column to float
        #data = data[data,WEX != '.']
        #data['WEX'] = data['WEX'].astype(float)

        # Scale the data
        closing_prices = data['Close'].values.reshape(-1, 1)
        self.scaler = MinMaxScaler(feature_range=(0, 1))
        data_scaled = self.scaler.fit_transform(closing_prices)
        print(f"data_scaled {data_scaled}")

        # Create lagged features
        X = data_scaled[:-1]
        y = data_scaled[1:]

        # Split the data into training and test sets
        train_size = int(0.8 * len(X))
        self.X_train, self.X_test = X[:train_size], X[train_size:]
        self.y_train, self.y_test = y[:train_size], y[train_size:]

        # Reshape the input data to 3D for LSTM
        self.X_train1 = np.reshape(self.X_train, (self.X_train.shape[0], self.X_train.shape[1], 1))
        #self.X_test1 = np.reshape(self.X_test, (self.X_test.shape[0], 1, self.X_test.shape[1]))
        #self.y_train1 = np.reshape(self.y_train, (self.y_train.shape[0], 1, self.y_train.shape[1]))
        #self.y_test1 = np.reshape(self.y_test, (self.y_test.shape[0], 1, self.y_test.shape[1]))

        #print(f"X_train.shape {self.X_train.shape}")
        self.model = Sequential([
            Input((self.X_train1.shape[1], 1)),
            LSTM(units=50, return_sequences=True),
            #Dropout(0.3),
            #LSTM(300, activation='relu', return_sequences=True, input_shape=(self.X_train1.shape[1], self.X_train1.shape[2])),
            #Dropout(0.3),
            LSTM(units=50),
            #Dropout(0.3),
            #Flatten(),
            #LSTM(100),
            #Dense(256),
            Dense(units=1),
        ])

        #self.model.compile(optimizer='adam', loss=['mse', 'mae', 'mape'], metrics=['accuracy'])
        self.model.compile(optimizer='adam', loss=['mean_squared_error'], metrics=['precision'])

        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

        if retrain:
            self.model.fit(self.X_train1, self.y_train, epochs=10, batch_size=32, verbose=0, callbacks=[tensorboard_callback])#, validation_split=0.3, verbose=0, callbacks=[tensorboard_callback])

            self.loss = self.model.evaluate(self.X_test, self.y_test)
            print(f'Test loss: {self.loss}')

        try:
            joblib.dump(self.model, 'src/.model.dump')
        except NotFittedError as exc:
            print(f"Model is not fitted yet.")

    def predict(self, prices):
        print(f"Predicao")

        try:
            self.model = joblib.load('src/.model.dump')
        except NotFittedError as exc:
            print(f"Model is not fitted yet.")

        h_prices = np.loadtxt(prices)
        h_prices1 = np.reshape(h_prices, (h_prices.shape[0], 1, 1))
        y_pred = self.model.predict(h_prices1)
        
        y_pred_inv = self.scaler.inverse_transform(y_pred)
        # print(f"self.y_pred_inv {y_pred_inv}")
        # print(f"self.y_pred_inv.shape {y_pred_inv.shape}")
        y_test_inv = self.scaler.inverse_transform(self.y_test)
        # print(f"self.y_test_inv {y_test_inv}")
        # print(f"self.y_test_inv.shape {y_test_inv.shape}")

        mae = mean_absolute_error(y_test_inv,y_pred_inv)
        mse = mean_squared_error(y_test_inv,y_pred_inv)
        rmse = np.sqrt(mse)
        mape = mean_absolute_percentage_error(y_test_inv,y_pred_inv)

        return mae,mse, rmse, mape