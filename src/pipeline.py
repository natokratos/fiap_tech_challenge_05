import datetime
import numpy as np
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_percentage_error
from sklearn.exceptions import NotFittedError
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
from tensorflow.keras.callbacks import TensorBoard
from tensorflow.keras.models import Sequential
from tensorflow.keras.metrics import Recall, F1Score, Precision
from tensorflow.keras.layers import LSTM, Dense, Dropout, Flatten, Input
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
#import yfinance as yf
import pandas as pd
import zipfile
import joblib
import json
import re
import nltk

from nltk.corpus import stopwords

class Pipeline:
    def __init__(self, retrain):
        df_prospects = self.read_json("prospects")
        df_prospects_exploded = df_prospects['prospects'].explode()
        df_res = pd.DataFrame()
        count = 0
        for dfp, v in zip(df_prospects_exploded.index, df_prospects_exploded):
            if type(v) is not float and dfp < len(df_prospects):
                v["index"] = dfp

                df_res = pd.concat([df_res, pd.DataFrame([{'cod_prospect': f"{dfp}{v['codigo']}", 'prospects': v}])], ignore_index=True)

        df_temp = df_res["prospects"].apply(pd.Series)
        df_prospects = pd.concat([df_res.drop('prospects', axis=1), df_temp], axis=1)
        #print(f"df_prospects [{df_prospects}] [{df_prospects.columns}] [{df_prospects.shape}]")
        print(f"df_prospects [{df_prospects.shape}]")

        df_vagas = self.read_json("vagas")
        df_vagas.reset_index(inplace=True)
        df_vagas = self.normalize_json(df_vagas, "informacoes_basicas")
        df_vagas = self.normalize_json(df_vagas, "perfil_vaga")
        df_vagas = self.normalize_json(df_vagas, "beneficios")
        df_vagas.rename(columns={'titulo_vaga': 'titulo'}, inplace=True)
        #print(f"df_vagas [{df_vagas}] [{df_vagas.columns}] [{df_vagas.shape}]")
        print(f"df_vagas [{df_vagas.shape}]")

        df_applicants = self.read_json("applicants")
        df_applicants.reset_index(inplace=True)
        df_applicants = self.normalize_json(df_applicants, "infos_basicas")
        df_applicants = self.normalize_json(df_applicants, "informacoes_pessoais")
        df_applicants = self.normalize_json(df_applicants, "informacoes_profissionais")
        df_applicants = self.normalize_json(df_applicants, "formacao_e_idiomas")
        #print(f"df_applicants [{df_applicants}] [{df_applicants.columns}] [{df_applicants.shape}]")
        print(f"df_applicants [{df_applicants.shape}]")
        #pd.set_option('display.max_columns', None)

        merged_df = pd.merge(df_prospects, df_vagas, on=['index'],  how="left", suffixes=['_df_prospects', '_df_vagas'])
        merged_df['codigo'] = merged_df['codigo'].astype(int)
        final_df = pd.merge(merged_df, df_applicants, left_on='codigo', right_on='index',  how="left", suffixes=['_merged_df', '_df_applicants'])
        final_df.fillna("", inplace=True)
        #print(f"final_df [{final_df}] [{final_df.columns}] [{final_df.shape}]")
        print(f"final_df [{final_df.shape}]")

        count = 0
        #word_count_vector = []
        nltk.download('stopwords')
        portuguese_stop_words = stopwords.words('portuguese')
        custom_stop_words = ['descrição', 'comentário', 'and', 'all', 'Descrição/Comentário:', 'Description)',
                                'including', 'provide', 'subida', 'durante', 'set', 'input', 'final', 'experiência',
                                'comprovada', 'responsabilidades']
        self.all_stop_words = ENGLISH_STOP_WORDS.union(portuguese_stop_words).union(custom_stop_words)
        self.all_stop_words = self.all_stop_words.union(custom_stop_words)
        #print(f"all_stop_words {all_stop_words}")
        prospects_categorized_words = []
        words = []
        cv = CountVectorizer(max_df=0.85, stop_words=list(self.all_stop_words))
        for df_pa, df_ctc, df_hcn, df_tc, df_np, df_na, df_aa in zip(final_df["principais_atividades"],
#         for df_pa, df_ctc, df_hcn, df_tc, df_np, df_na, df_aa, df_cv_en, df_cv_pt in zip(final_df["principais_atividades"],
                                            final_df["competencia_tecnicas_e_comportamentais"],
                                            final_df["habilidades_comportamentais_necessarias"],
                                            final_df["tipo_contratacao"],
                                            final_df["nivel_profissional"],
                                            final_df["nivel_academico_merged_df"],
                                            final_df["areas_atuacao"]):
#                                             final_df["cv_en"],
#                                             final_df["cv_pt"]):
            try:
                if type(df_pa) is not float:
                    words = words + df_pa.split()
                if type(df_ctc) is not float:
                    words = words + df_ctc.split()
                if type(df_hcn) is not float:
                    words = words + df_hcn.split()
                if type(df_tc) is not float:
                    words.append(df_tc)
                if type(df_np) is not float:
                    words.append(df_np)
                if type(df_na) is not float:
                    words.append(df_na)
                if type(df_aa) is not float:
                    words.append(df_aa)
#                 if type(df_cv_en) is not float:
#                     tmp = df_cv_en.split('\n')
#                     for t in tmp:
#                         for w in t.split(' '):
#                             words.append(w)
#                 if type(df_cv_pt) is not float:
#                     tmp = df_cv_pt.split('\n')
#                     for t in tmp:
#                         for w in t.split(' '):
#                             words.append(w)
            except ValueError as e:
                True
            if count > 1000:
                break
            else:
                count = count + 1

        word_count = cv.fit_transform(words)
        prospects_categorized_words = list(cv.vocabulary_.items())[:10000]

        df_train = pd.DataFrame.from_dict(prospects_categorized_words)#, columns=['words', 'count'])

        self.encoder = LabelEncoder()
        df_train['encoded_features'] = self.encoder.fit_transform(df_train[[0]])
        df_train = df_train.drop(0, axis=1)
        print(f"df_train {df_train} {df_train.shape}")

        # Input/Output Split (for next word prediction)
        X = df_train[:-1]
        y = df_train[1:]

        # Split the data into training and test sets
        train_size = int(0.8 * X.shape[0])
        self.X_train, self.X_test = X[:train_size], X[train_size:]
        self.y_train, self.y_test = y[:train_size], y[train_size:]

        # Reshape the input data to 3D for LSTM
        self.X_train1 = np.reshape(self.X_train, (-1, 1, self.X_train.shape[0]))

        self.model = Sequential([
            Input((self.X_train1.shape[0], self.X_train1.shape[1])),
            LSTM(units=30, activation='relu', return_sequences=True),
            Dropout(0.3),
            Dense(1),
        ])

        self.model.compile(optimizer='adam', loss=['mean_squared_error'], metrics=['precision'])

        print(f"self.model.summary() {self.model.summary()}")

        log_dir = "logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        tensorboard_callback = TensorBoard(log_dir=log_dir, histogram_freq=1)

        #retrain = True
        print(f"self.X_test {self.X_test}")
        print(f"self.y_test {self.y_test}")
        if retrain:
            self.model.fit(self.X_train, self.y_train, epochs=10, batch_size=32, verbose=0, callbacks=[tensorboard_callback])

            self.loss = self.model.evaluate(self.X_test, self.y_test)
            print(f'Test loss: {self.loss}')

        try:
            joblib.dump(self.model, 'src/.model.dump')
        except NotFittedError as exc:
            print(f"Model is not fitted yet.")

    def predict(self, applicants):
        print(f"Predicao")

        try:
            self.model = joblib.load('src/.model.dump')
        except NotFittedError as exc:
            print(f"Model is not fitted yet.")

        df_applicants = self.read_json(applicants)
        df_applicants.reset_index(inplace=True)
        df_applicants = self.normalize_json(df_applicants, "infos_basicas")
        df_applicants = self.normalize_json(df_applicants, "informacoes_pessoais")
        df_applicants = self.normalize_json(df_applicants, "informacoes_profissionais")
        df_applicants = self.normalize_json(df_applicants, "formacao_e_idiomas")
        print(f"df_applicants [{df_applicants}] [{df_applicants.columns}] [{df_applicants.shape}]")

        count = 0
        categorized_words = []
        words = []
        cv = CountVectorizer(max_df=0.85, stop_words=list(self.all_stop_words))
        for df_cv_en, df_cv_pt in zip(df_applicants["cv_en"],
                                        df_applicants["cv_pt"]):
            try:
                print(f"df_cv_en {df_cv_en}")
                if type(df_cv_en) is not float:
                    tmp = df_cv_en.split('\n')
                    print(f"tmp_cv_en {tmp}")
                    for t in tmp:
                        print(f"t.split(' ') {t.split(' ')}")
                        for w in t.split(' '):
                            words.append(w)
                print(f"df_cv_pt {df_cv_pt}")
                if type(df_cv_pt) is not float:
                    tmp = df_cv_pt.split('\n')
                    for t in tmp:
                        for w in t.split(' '):
                            words.append(w)
            except ValueError as e:
                True
            if count > 1000:
                break
            else:
                count = count + 1

        #print(f"words {words}")
        word_count = cv.fit_transform(words)
        categorized_words = list(cv.vocabulary_.items())[:10000]

        df_predict = pd.DataFrame.from_dict(categorized_words)

        #encoder = LabelEncoder()
        df_predict['encoded_features'] = self.encoder.fit_transform(df_predict[[0]])
        df_predict = df_predict.drop(0, axis=1)
        print(f"df_predict {df_predict} {df_predict.shape}")
        #h_prices1 = np.reshape(h_prices, (h_prices.shape[0], 1, 1))
        y_pred = self.model.predict(df_predict)
        print(f"y_pred {y_pred} {y_pred.shape}")

        y_pred1 = np.reshape(y_pred, (y_pred.shape[0], -1)).flatten()
#         print(f"y_pred_inv {y_pred_inv} {y_pred_inv.shape}")
        y_pred_inv = self.encoder.inverse_transform(y_pred1)
        # print(f"self.y_pred_inv {y_pred_inv}")
        # print(f"self.y_pred_inv.shape {y_pred_inv.shape}")
        y_test_inv = self.encoder.inverse_transform(self.y_test)
        # print(f"self.y_test_inv {y_test_inv}")
        # print(f"self.y_test_inv.shape {y_test_inv.shape}")

#         df_predict1 = np.reshape(df_predict, (df_predict.shape[1], -1))
#         print(f"df_predict1 {df_predict1} {df_predict.shape}")
#         y_pred_inv = np.reshape(y_pred, (y_pred.shape[0], -1))
#         print(f"y_pred_inv {y_pred_inv} {y_pred_inv.shape}")
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

    def normalize_json(self, df, column_name, explode=False, separator=','):
        df1 = pd.json_normalize(df[column_name], sep=separator)
        df2 = pd.concat([df, df1], axis=1)
        df2.drop(column_name, axis=1, inplace=True)

        return df2

#     def normalize_json(self, df, column_name, explode=False, separator=','):#, teste=[]):
#         #print(f"df[{column_name}] {df[column_name]} explode {explode}")
#         if explode:
#             #dfx1 = df.reset_index()
#             #print(f"EXPLODE1 {dfx1} {dfx1.columns} {dfx1.shape}")
#             dfx = df[column_name].explode()#.reset_index()
#             print(f"EXPLODE {dfx}")# {dfx.columns}")
#             df1 = pd.json_normalize(dfx)#, record_path='prospects', meta=['titulo', 'modalidade'])
#             dfx_reset = dfx.reset_index()#drop=True)
#             df2 = pd.concat([dfx_reset.drop('prospects', axis=1), df1], axis=1)
#             print(f"------------------df1{df2} {df2.columns} {df2.columns}")
#         else:
#             df1 = pd.json_normalize(df[column_name], sep=separator)
#             df2 = pd.concat([df, df1], axis=1)
#             df2.drop(column_name, axis=1, inplace=True)
#
#         return df2
