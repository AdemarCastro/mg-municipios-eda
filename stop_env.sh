#!/bin/bash

echo "Desativando ambiente virtual..."
deactivate

echo "Adicionando mudanças ao Git..."
git add .

echo "Digite a mensagem do commit: "
read commit_message

git commit -m "$commit_message"
git push origin main

echo "Mudanças enviadas para o repositório remoto!"