#!/bin/bash

mkdir ParcialIDS
cd ParcialIDS || exit
mkdir .venv
mkdir static
mkdir templates
cd static
mkdir css
mkdir images
cd ..
touch app.py
pipenv install flask
pipenv shell
export FLASK_DEBUG=1