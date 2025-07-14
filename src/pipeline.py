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
#import yfinance as yf
import pandas as pd
import zipfile
import joblib
import json

class Pipeline:
    #df_prospects = None
    def add_index_field(self, index_dict):
        index_dict = self.df_prospects["index"] #[index_dict.append({ 'index', df_idx }) for df_idx in self.df_prospects["index"]]

        return index_dict

    def __init__(self, retrain):
        df_prospects = self.read_json("prospects")
        df_prospects_exploded = df_prospects['prospects'].explode()
        df_res = pd.DataFrame()
        count = 0
        for dfp, v in zip(df_prospects_exploded.index, df_prospects_exploded):
            if type(v) is not float and dfp < len(df_prospects):
                v["index"] = dfp

                df_res = pd.concat([df_res, pd.DataFrame([{'cod_prospect': f"{dfp}{v['codigo']}", 'prospects': v}])], ignore_index=True)
            if count < 4:
                count = count + 1
            else:
                break

        df_temp = df_res["prospects"].apply(pd.Series)
        df_prospects = pd.concat([df_res.drop('prospects', axis=1), df_temp], axis=1)
        print(f"df_prospects [{df_prospects}] [{df_prospects.columns}] [{df_prospects.shape}]")

        df_vagas = self.read_json("vagas")
        df_vagas.reset_index(inplace=True)
        df_vagas = self.normalize_json(df_vagas, "informacoes_basicas")
        df_vagas = self.normalize_json(df_vagas, "perfil_vaga")
        df_vagas = self.normalize_json(df_vagas, "beneficios")
        df_vagas.rename(columns={'titulo_vaga': 'titulo'}, inplace=True)
        print(f"df_vagas [{df_vagas}] [{df_vagas.columns}] [{df_vagas.shape}]")

        df_applicants = self.read_json("applicants")
        df_applicants.reset_index(inplace=True)
        df_applicants = self.normalize_json(df_applicants, "infos_basicas")
        df_applicants = self.normalize_json(df_applicants, "informacoes_pessoais")
        df_applicants = self.normalize_json(df_applicants, "informacoes_profissionais")
        df_applicants = self.normalize_json(df_applicants, "formacao_e_idiomas")
        print(f"df_applicants [{df_applicants}] [{df_applicants.columns}] [{df_applicants.shape}]")
        #pd.set_option('display.max_columns', None)
        #print(df_applicants[df_applicants['index'] == 25632])

        merged_df = pd.merge(df_prospects, df_vagas, on=['index'],  how="left", suffixes=['_df_prospects', '_df_vagas'])
        merged_df['codigo'] = merged_df['codigo'].astype(int)
        #print(f"merged_df [{merged_df}] [{merged_df.columns}] [{merged_df.shape}]")
        final_df = pd.merge(merged_df, df_applicants, left_on='codigo', right_on='index',  how="left", suffixes=['_merged_df', '_df_applicants'])
        final_df.fillna("", inplace=True)
        print(f"final_df [{final_df}] [{final_df.columns}] [{final_df.shape}]")
        #print(final_df[final_df['index_merged_df'] == 4530])

    def x__init__(self, retrain):
        # Path to your zip file
        zip_files = ['prospects', 'vagas', 'applicants']

        df_prospects = self.read_json("prospects")
        df_prospects.reset_index(inplace=True)
        pd.set_option('display.max_columns', None)
        df_prospects = self.normalize_json(df_prospects, "prospects", True)#, teste=["prospects", "codigo"])
        #df_prospects.rename(columns={'index': 'codigo'}, inplace=True)
        #df_prospects['index'] = df_prospects['index'].astype(object)
        ##df_prospects.sort_values(by='index', ascending=True, inplace=True)
        #df_prospects.fillna("", inplace=True)
        print(f"df_prospects {df_prospects.columns} {df_prospects.shape}")
        print(df_prospects)
        ##print("\ndf_prospects ===========")
        ##print(df_prospects[df_prospects['titulo'] == 'CONSULTOR CONTROL M'])
        print(df_prospects[df_prospects['index'] == 4530])

        df_vagas = self.read_json("vagas")
        #print("xxxxxxxxxxxxxxx")
        #print(df_vagas)
        #pd.set_option('display.max_columns', None)
        df_vagas.reset_index(inplace=True)
        ##dfx = pd.json_normalize(df_vagas["informacoes_basicas"])
        #print(f"------------------df1{df1} {df.columns} {df1.columns}")
        ##df_vagas = pd.concat([df_vagas, dfx], axis=1)
        df_vagas = self.normalize_json(df_vagas, "informacoes_basicas")
        df_vagas = self.normalize_json(df_vagas, "perfil_vaga")
        df_vagas = self.normalize_json(df_vagas, "beneficios")
        #df_vagas.fillna("", inplace=True)
        ##df_vagas.reset_index(inplace=True)
        ##print(f"-------DF2 {df_vagas.columns} {df_vagas.shape} {df_vagas[df_vagas['index'] == 4530]}")
        df_vagas.rename(columns={'titulo_vaga': 'titulo'}, inplace=True)
        #df_vagas['index'] = df_vagas['index'].astype(object)
        #df_vagas.sort_values(by='index', ascending=True, inplace=True)
        #print(f"-------DF3 {df_vagas.columns} {df_vagas.shape} {df_vagas[df_vagas['index'] == 4530]}")
        print(f"df_vagas {df_vagas.columns} {df_vagas.shape}")
        print(df_vagas)

        #print("\ndf_vagas ===========")
        #print(df_vagas[df_vagas['titulo'] == 'CONSULTOR CONTROL M'])
        print(df_vagas[df_vagas['index'] == 4530])
        #print("xxxxxxxxxxxxxxx")

        df_applicants = self.read_json("applicants")
        df_applicants.reset_index(inplace=True)
        df_applicants = self.normalize_json(df_applicants, "infos_basicas")
        df_applicants = self.normalize_json(df_applicants, "informacoes_pessoais")
        df_applicants = self.normalize_json(df_applicants, "informacoes_profissionais")
        df_applicants = self.normalize_json(df_applicants, "formacao_e_idiomas")
        #df2 = self.normalize_json(df2, "cv_pt", separator='\n')
        df_applicants.rename(columns={'index': 'codigo'}, inplace=True)
        df_applicants['codigo'] = df_applicants['codigo'].astype(object)
        #df_applicants.fillna("", inplace=True)
        print(f"df_applicants {df_applicants.columns} {df_applicants.shape}")
        print(df_applicants.head())

        # Merge df1 and df2, handling duplicate 'value' column
        #merged_df = pd.merge(df_vagas, df_prospects, on='id', how='outer', suffixes=('_df_vagas', '_df_prospects'))
        #merged_df = pd.merge(df_prospects, df_vagas, how="left", left_index=True, right_index=True, suffixes=['_df_prospects', '_df_vagas'])
        merged_df = pd.merge(df_prospects, df_vagas, on=['index','codigo'],  how="left", suffixes=['_df_prospects', '_df_vagas'])
        #merged_df = df_prospects.join(df_vagas, how="inner", lsuffix='_df_prospects', rsuffix='_df_vagas')
        #print(f"merged_df {merged_df.columns} {merged_df.shape}")
        #print(merged_df.head())

        # Merge the result with df3
        #final_df = merged_df.join(df_applicants, on='codigo', how="left", lsuffix='_df_prospects', rsuffix='_df_applicants')
        #final_df = pd.merge(df_prospects, df_applicants, on='codigo', how='left', suffixes=('_df_prospects', '_df_applicants'))
        final_df = merged_df
        final_df.fillna("", inplace=True)
        print(f"final_df {final_df.columns} {final_df.shape}")
        print(final_df.head())
        print(final_df[final_df['index'] == 4530])
        ##print("\ndf_vagas ===========")
        ##print(df_vagas.iloc[8194])
        ##print("\ndf_prospects ===========")
        ##print(df_prospects.iloc[8194])
        ##print("\nfinal_df ===========")
        ##print(final_df.iloc[0])
#         df1 = None
#         with zipfile.ZipFile("vagas.zip", 'r') as z:
#             with z.open("vagas.json") as f:
#                 df1 = pd.read_json(f, orient="index")
#                 print("TESTE")
#         print(df1.columns)
#         print(df1.head())
#         print(f"df[column_name] {df1["informacoes_basicas"]}")
#
#         df2 = pd.json_normalize(df1["informacoes_basicas"], sep=',')
#         print(f"df2{df2}")
#         df3 = pd.concat([df1, df2], axis=1)
#         print(f"df3{df3}")
#         df3 = df3.drop("informacoes_basicas", axis=1).dropna()
#         print(f"df3{df3}")
#         print("TESTE1")



        #df1 = self.normalize_json(df1, "informacoes_basicas")
        #print(df1.columns)
        #print(df1.head())
        #df1 = self.normalize_json(df1, "perfil_vaga")
        #print(df1.columns)
        #print(df1.head())
        #df1 = self.normalize_json(df1, "beneficios")
        #print(df1.columns)
        #print(df1.head())
#         with zipfile.ZipFile("prospects.zip", 'r') as z:
#             with z.open("prospects.json") as f:
#                 df = pd.read_json(f, orient="index")
#                 print(df)
#                 #json_data = json.load(f)
#                 #print(f"json_data [{json_data}]")
#                 #df1 = df.prospects.str.split(" ", expand=True)
#                 print(df.columns)
#                 df1 = pd.json_normalize(df["prospects"].explode(), sep=',')
#                 print(df1)
#                 df2 = pd.concat([df, df1], axis=1)
#                 df2 = df2.drop("prospects", axis=1).dropna()
#                 print(df2.columns)
#                 print(df2.head())

#                 column_flat = pd.DataFrame([[i, c_flattened] for i, y in df["prospects"].apply(list).iteritems() for c_flattened in y], columns=['I', "prospects"])
#                 column_flat = column_flat.set_index('I')
#                 df.drop(column, 1).merge(column_flat, left_index=True, right_index=True)
#
                #df1 = pd.json_normalize(df["prospects"])#, record_path=[0],

#                 for p in df["prospects"]:
#                     df = df + pd.json_normalize(p #record_path="prospects",
                        #meta=["titulo", "modalidade", ["prospects", "nome"]
#                     meta = [["prospects", "codigo"]
#                     ["prospects", "situacao_candidado"],
#                     ["prospects", "data_candidatura"],
#                     ["prospects", "ultima_atualizacao"],
#                     ["prospects", "comentario"],
#                     ["prospects", "recrutador"]
#                ])

                #print(f"df1 [{df1}]")

#         self.symbol = 'DIS'
#         self.start_date = '2020-01-01'
#         self.end_date = '2025-05-01'
#
#         print(f"Baixando os dados do Yahoo Finance ...\n")
#         #data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
#         data = yf.download(self.symbol, period='max')
#         print(f"data {data}")
#
#         data = data.dropna()
#
#         # Remove rows with '.' and convert the column to float
#         #data = data[data,WEX != '.']
#         #data['WEX'] = data['WEX'].astype(float)
#
#         # Scale the data
#         closing_prices = data['Close'].values.reshape(-1, 1)
#         self.scaler = MinMaxScaler(feature_range=(0, 1))
#         data_scaled = self.scaler.fit_transform(closing_prices)
#         print(f"data_scaled {data_scaled}")
#
#         # Create lagged features
#         X = data_scaled[:-1]
#         y = data_scaled[1:]
#
#         # Split the data into training and test sets
#         train_size = int(0.8 * len(X))
#         self.X_train, self.X_test = X[:train_size], X[train_size:]
#         self.y_train, self.y_test = y[:train_size], y[train_size:]
#
#         # Reshape the input data to 3D for LSTM
#         self.X_train1 = np.reshape(self.X_train, (self.X_train.shape[0], self.X_train.shape[1], 1))
#         #self.X_test1 = np.reshape(self.X_test, (self.X_test.shape[0], 1, self.X_test.shape[1]))
#         #self.y_train1 = np.reshape(self.y_train, (self.y_train.shape[0], 1, self.y_train.shape[1]))
#         #self.y_test1 = np.reshape(self.y_test, (self.y_test.shape[0], 1, self.y_test.shape[1]))
#
#         #print(f"X_train.shape {self.X_train.shape}")
#         self.model = Sequential([
#             Input((self.X_train1.shape[1], 1)),
#             LSTM(units=50, return_sequences=True),
#             #Dropout(0.3),
#             #LSTM(300, activation='relu', return_sequences=True, input_shape=(self.X_train1.shape[1], self.X_train1.shape[2])),
#             #Dropout(0.3),
#             LSTM(units=50),
#             #Dropout(0.3),
#             #Flatten(),
#             #LSTM(100),
#             #Dense(256),
#             Dense(units=1),
#         ])
#
#         #self.model.compile(optimizer='adam', loss=['mse', 'mae', 'mape'], metrics=['accuracy'])
#         self.model.compile(optimizer='adam', loss=['mean_squared_error'], metrics=['precision'])
#
#         log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
#         tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)
#
#         if retrain:
#             self.model.fit(self.X_train1, self.y_train, epochs=10, batch_size=32, verbose=0, callbacks=[tensorboard_callback])#, validation_split=0.3, verbose=0, callbacks=[tensorboard_callback])
#
#             self.loss = self.model.evaluate(self.X_test, self.y_test)
#             print(f'Test loss: {self.loss}')
#
#         try:
#             joblib.dump(self.model, 'src/.model.dump')
#         except NotFittedError as exc:
#             print(f"Model is not fitted yet.")

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

    def read_json(self, file_name, orient='index'):
        df = None
        with zipfile.ZipFile(f"{file_name}.zip", 'r') as z:
            with z.open(f"{file_name}.json") as f:
                df = pd.read_json(f, orient=orient)

        return df

    def normalize_json(self, df, column_name, explode=False, separator=','):#, teste=[]):
        #print(f"df[{column_name}] {df[column_name]} explode {explode}")
        if explode:
            #dfx1 = df.reset_index()
            #print(f"EXPLODE1 {dfx1} {dfx1.columns} {dfx1.shape}")
            dfx = df[column_name].explode()#.reset_index()
            print(f"EXPLODE {dfx}")# {dfx.columns}")
            df1 = pd.json_normalize(dfx)#, record_path='prospects', meta=['titulo', 'modalidade'])
            dfx_reset = dfx.reset_index()#drop=True)
            df2 = pd.concat([dfx_reset.drop('prospects', axis=1), df1], axis=1)
            print(f"------------------df1{df2} {df2.columns} {df2.columns}")
            #merged_df = pd.merge(df_prospects, df_vagas, on=['index','codigo'],  how="left", suffixes=['_df_prospects', '_df_vagas'])

        else:
            df1 = pd.json_normalize(df[column_name], sep=separator)
            df2 = pd.concat([df, df1], axis=1)
            #print(f"------------------df2{df2}")
            ##df2 = df2.drop(column_name, axis=1)
            df2.drop(column_name, axis=1, inplace=True)
            #print(f"df2{df2}")

        return df2
