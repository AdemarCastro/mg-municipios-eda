#!/bin/bash

echo "Atualizando repositório..."
git pull origin main

echo "Criando e ativando ambiente virtual..."
python3 -m venv venv
source venv/bin/activate

echo "Instalando dependências..."
pip install -r requirements.txt

echo "Ambiente configurado!"
