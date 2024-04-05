# AtvPonderadaSem7

## Autor: Lucas de Luccas

## Descrição do Projeto
Este projeto é uma aplicação web projetada para controlar o braço robótico Dobot Magician Lite. Utiliza a biblioteca `pydobot` para o controle do braço, e a biblioteca `htmx` para comunicação entre o frontend e o backend. O backend foi desenvolvido em Python com o uso do framework Flask, enquanto o armazenamento de dados é gerido pela biblioteca TinyDB, um banco de dados no formato JSON.

## Como rodar o projeto
Siga os passos abaixo para configurar o ambiente e executar o projeto localmente:

1. Clone o repositório para a sua máquina local.
2. Navegue até a pasta do projeto e instale as dependências:

    ```shell
    cd src
    python -m venv venv
    venv/Scripts/activate
    pip install -r requirements.txt
    ```

3. Inicie a aplicação:

    ```shell
    python app.py
    ```

## Estrutura do Projeto
│ README.md
│ requirements.txt
│
├─── Banco de Dados
│ │ banco.json
│
├─── backend
│ │ app.py
│ │ modals.py
│
├─── frontend
│ ├─── templates
│ │ index.html
│ │ log.html
│ │ control.html
│
└─── static
│
└─── venv

## Vídeo de Demonstração

https://drive.google.com/file/d/1IdVlyoO4fPsXBiDc4X0PfkXvtrumQh5R/view?usp=sharing



---
