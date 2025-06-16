import uvicorn

from api import ApiEndpoints

def run():

    '''
    Execução do scrapper para extracao dos dados
    '''
    uvicorn.run("api:app", host="0.0.0.0", port=8080, reload=True)

if __name__ == '__main__':

    run()
