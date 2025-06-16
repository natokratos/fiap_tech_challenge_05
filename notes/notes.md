# fiap_tech_challenge_03

WSL

https://docs.localstack.cloud/user-guide/integrations/devcontainers/#vscode

https://www.omgubuntu.co.uk/2022/04/how-to-install-firefox-deb-apt-ubuntu-22-04
sudo apt-get install firefox
sudo apt install libffi-dev
sudo ldconfig

https://gist.github.com/trongnghia203/9cc8157acb1a9faad2de95c3175aa875

git clone https://github.com/yyuu/pyenv-virtualenv.git $HOME/.pyenv/plugins/pyenv-virtualenv

pyenv install -l

pyenv install 3.13.0

pyenv virtualenv 3.13.0 venv_3.13.0
--
source venv_3.13.0/bin/activate
pyenv virtualenvs           
pip3.13 install poetry 

pyenv global 3.13.0

pip install --upgrade pip

pip3 install selenium
pip3 install bs4
pip3 install requests
pip3 install pandas
pip3 install lxml
pip3 install boto3
pip3 install awscli
pip3 install fastparquet

https://stackoverflow.com/questions/64086810/navigate-pagination-with-selenium-webdriver
https://stackoverflow.com/questions/63881801/element-is-not-clickable-at-point-because-another-element-obscures-it
https://stackoverflow.com/questions/75688714/python-selenium-how-to-click-element-in-pagination-that-is-not-a-button-a-hr
https://stackoverflow.com/questions/30002313/finding-elements-by-class-name-with-selenium-in-python

aws s3api create-bucket --bucket dados-brutos --endpoint=http://localhost:4566
aws s3 ls --endpoint=http://localhost:4566

aws configure
local | local
us-east-1
json

docker logs -f localstack-main

pip freeze > requirements.txt

poetry install
poetry lock
poetry run python3.13 src/main.py
aws lambda create-function --function-name lambda-scrapper1 --runtime python3.9 --role arn:aws:iam::000000000000:role/lambda-exec --zip-file fileb://app_package.zip --endpoint=http://localhost:4566
aws lambda list-functions --endpoint=http://localhost:4566 | grep lambda-scrapper
aws lambda get-function --function-name lambda-scrapper --endpoint=http://localhost:4566
aws iam put-role-policy --role-name lambda-exec --policy-name AssumeRolePolicyDocument --policy-document '{ "Version": "2012-10-17", "Statement": [ { "Effect": "Allow", "Action": "*", "Resource": "*" }] }' --endpoint=http://localhost:4566
aws iam list-role-policies --role-name lambda-exec

SELECT schema_name FROM information_schema.schemata
SELECT table_schema, table_name FROM information_schema.tables

docker rm db04 && docker rm db04
docker volume rm fiap_tech_challenge_04_pgdata


* * * * * curl -v http://172.30.0.4:8080 >> /var/log/cron.log 2>&1

https://medium.com/@techwithjulles/recurrent-neural-networks-rnns-and-long-short-term-memory-lstm-creating-an-lstm-model-in-13c88b7736e2

curl -v http://172.30.0.4:8080/predict?prices="./predict_input"

50
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 90ms/step - accuracy: 0.1250 - loss: 0.0484 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 183ms/step - accuracy: 0.1250 - loss: 0.0484 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_loss: 0.0000e+00
Test loss: [0.04843377321958542, 0.125, 0.0, 0.0, 0.0]

70
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 94ms/step - accuracy: 0.1875 - loss: 0.0505 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 186ms/step - accuracy: 0.1875 - loss: 0.0505 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_loss: 0.0000e+00
Test loss: [0.050489068031311035, 0.1875, 0.0, 0.0, 0.0]

100
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 87ms/step - accuracy: 0.2500 - loss: 0.0510 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 169ms/step - accuracy: 0.2500 - loss: 0.0510 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_loss: 0.0000e+00
Test loss: [0.05101064220070839, 0.25, 0.0, 0.0, 0.0]

300
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 94ms/step - accuracy: 0.2500 - loss: 0.0583 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 171ms/step - accuracy: 0.2500 - loss: 0.0583 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_loss: 0.0000e+00
Test loss: [0.05831832066178322, 0.25, 0.0, 0.0, 0.0]

500
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 93ms/step - accuracy: 0.2500 - loss: 0.0610 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 175ms/step - accuracy: 0.2500 - loss: 0.0610 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_loss: 0.0000e+00
Test loss: [0.06102947145700455, 0.25, 0.0, 0.0, 0.0]

800
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 91ms/step - accuracy: 0.2500 - loss: 0.0675 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 170ms/step - accuracy: 0.2500 - loss: 0.0675 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_loss: 0.0000e+00
Test loss: [0.0675036609172821, 0.25, 0.0, 0.0, 0.0]

Data 2023 - 2025
2 LSTM 300
Epochs 300
4/4 ━━━━━━━━━━━━━━━━━━━━ 0s 15ms/step - accuracy: 0.3536 - loss: 0.1015 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_loss: 0.0000e+00
Test loss: [0.0830649733543396, 0.3760683834552765, 0.0, 0.0, 0.0]

Data 2020 - 2025
3 LSTM 300
Epochs 300
9/9 ━━━━━━━━━━━━━━━━━━━━ 0s 10ms/step - accuracy: 0.6177 - loss: 0.0764 - mae_loss: 0.0000e+00 - mape_loss: 0.0000e+00 - mse_loss: 0.0000e+00
Test loss: [0.07991201430559158, 0.5522388219833374, 0.0, 0.0, 0.0]
