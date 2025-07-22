# fiap_tech_challenge_05

## Pre-requisitos
- O Docker deve estar instalado na maquina em que o projeto sera executado.
- Ter um browser instalado na máquina ou ferramenta para acessar a API (curl, por exemplo)

## Objetivo
Este projeto tem como objetivo criar um LSTM para fazer a predição da probabilidade de contratacao de certos grupos de pessoas, baseado no historico de contratacoes anterioes.

## Operação
A aplicação engloba 3 containers:
- Tech05: aquele que tem a API para realizar as predicoes. Ela roda em Python3.12;
- Tensorboard05: ferramenta de monitoração do modelode LSTM;
- Portainer05: ferramenta de monitoração dos containers, tanto recursos de infra quanto dos logs e saúde destes.

Para executá-los, basta digitar a seguinte linha de comando:

docker compose -f docker-compose.yml up -d

Basta esperar que ele baixe as imagens e as coloque no ar. Para verificar se a aplicação subiu corretamente, basta olhar o log do container tech05:

docker logs tech05 -f

Ela estará no ar quando aparecerem a seguintes mensagens:

INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

A API já faz a cargs dos dados e o treinamento do modelo ao iniciar, caso não tenha sido feito, verificando se o arquivo **src/.model.dump** existe e se a variável de ambiente **RETRAIN** do docker-compose existe e está como **true**.

Fica disponível um endpoint chamado **predict**, que recebe um arquivo de entrada com valores para serem usados na predição. Já existe na raiz do projeto um arquivo pronto chamado **predict_input**, para ser usado como teste. A chamada do endpoint fica desta forma, a partir da raiz do projeto:

curl -v http://172.30.0.4:8080/predict?prices="./predict_input"
curl -v http://localhost:8080/predict?prices="./predict_input"

## Monitoração
A monitoração pode ser feita nestes 2 endpoints, acessando-os pelo browser:
- Portainer: ferramenta de monitoração dos containers, tanto recursos de infra quanto dos logs e saúde destes.

http://172.30.0.6:9000
http://localhost:9000

Usuario: admin
Senha: adminportainer

- Tensorboard: ferramenta de monitoração do modelode LSTM.

http://172.30.0.5:6006/#timeseries&run=fit%2F20250605-154514%2Ftrain
http://localhost:6006/#timeseries&run=fit%2F20250605-154514%2Ftrain


## Qualidade do Modelo
Nao foi possivel calcular a qualidade do modelo corretamente, a precisao do modelo ficou em 100%, demonstando que exste overfitting. Isto pode ter sido causad por alguns fatores:
- Baixa quantidade de dados disponíveis para treinar o modelo;
- Problemas ao calcular as metricas MAE, MSE, MRSE e MAPE. O modelo realiza a predição mas não faz o cálculo das métricas, talvez devido a problemas nos dados de entrada
