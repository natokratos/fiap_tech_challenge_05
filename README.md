# fiap_tech_challenge_04

## Pre-requisitos
- O Docker deve estar instalado na maquina em que o projeto sera executado.
- Ter um browser instalado na máquina ou ferramenta para acessar a API (curl, por exemplo)

## Objetivo
Este projeto tem como objetivo criar um LSTM para fazer a predição de valores do fechamento da bolsa de valores da empresa The Walt Disney Company (DIS). Ele utiliza os valores do Yahoo Finance e cria toda a pipeline de desenvolvimento, desde a criação do modelo preditivo até o deploy em uma API que permite a previsão de preço de ações.

## Operação
A aplicação engloba 3 containers:
- Tech04: aquele que tem a API para realizar as predicoes. Ela roda em Python3.12;
- Tensorboard04: ferramenta de monitoração do modelode LSTM;
- Portainer04: ferramenta de monitoração dos containers, tanto recursos de infra quanto dos logs e saúde destes.

Para executá-los, basta digitar a seguinte linha de comando:

docker compose -f docker-compose.yml up -d

Basta esperar que ele baixe as imagens e as coloque no ar. Para verificar se a aplicação subiu corretamente, basta olhar o log do container tech04:

docker logs tech04 -f

Ela estará no ar quando aparecerem a seguintes mensagens:

INFO:     Started server process [XXXXX]
INFO:     Waiting for application startup.
INFO:     Application startup complete.

A API já faz a cargs dos dados e o treinamento do modelo ao iniciar, caso não tenha sido feito, verificando se o arquivo **src/.model.dump** existe e se a variável de ambiente **RETRAIN** do docker-compose existe e está como **true**.

Fica disponível um endpoint chamado **predict**, que recebe um arquivo de entrada com valores para serem usados na predição. Já existe na raiz do projeto um arquivo pronto chamado **predict_input**, para ser usado como teste. A chamada do endpoint fica desta forma, a partir da raiz do projeto:

curl -v http://172.30.0.4:8080/predict?prices="./predict_input"

## Monitoração
A monitoração pode ser feita nestes 2 endpoints, acessando-os pelo browser:
- Portainer: ferramenta de monitoração dos containers, tanto recursos de infra quanto dos logs e saúde destes.

http://172.30.0.6:9000

Usuario: admin
Senha: adminportainer

- Tensorboard: ferramenta de monitoração do modelode LSTM.

http://172.30.0.5:6006/#timeseries&run=fit%2F20250605-154514%2Ftrain


## Qualidade do Modelo
Foram medidas a precision e a loss do modelo (mean_squared_error), que ficaram em torno de 80,2% e 1,21% respectivamente.

Nas predicoes usando o arquivo predic_inout na raiz deste projeto, as medições foram estas e ficaram em torno destes valores:

MAE: 109.59985727372306
MSE: 12931.893355177934
RMSE: 113.71848290923482
MAPE: 1.060040553927951

O MAPE ficou em torno de 2,5% , sendo assim considero que o modelo ficou com uma precisão e erros aceitáveis. Pode melhorar mais, trabalhando no treinamento e talvez na preparação dos dados.
