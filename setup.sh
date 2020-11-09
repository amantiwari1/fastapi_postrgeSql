#! /bin/bash

sudo su

apt update

apt install python3-pip

python3 -m venv env
source ./env/bin/activate

pip3 install -r requirements.txt

echo 'Make Env'

echo 'Please run uvicorn --port 8000 --host 127.0.0.1 main:app --reload '