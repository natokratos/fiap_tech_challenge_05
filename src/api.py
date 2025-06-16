import os

from fastapi import FastAPI
from pipeline import Pipeline

app = FastAPI()

class ApiEndpoints:
    def __init__(self, retrain : bool):
        pipeline = Pipeline(retrain)
        
        @app.get("/")
        async def read_root():
            return {"API": "V1"}

        @app.get("/predict")
        def predict(prices:str):
            #pipeline = Pipeline()

            mae, mse, rmse, mape = pipeline.predict(prices)
            return { "message" : f"mae: {mae}|mse: {mse}|rmse: {rmse}|mape: {mape}"}
            #29508039744.178253|5.796406865801174e+21|76134137322.23656|6090.248222127322
            #87940498790.81458|5.059217249030164e+22|224927038148.59973|17566.530693037814

retrain = False
path = "./src/.model_dump"
if not os.path.exists(path):
    retrain = True

if "RETRAIN" in os.environ and not os.path.exists(path):
    retrain = (os.environ["RETRAIN"].lower() is "true")

print(f"RETRAIN [{retrain}]")
server = ApiEndpoints(retrain)