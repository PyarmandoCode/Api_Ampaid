from flask import Flask
from flask_cors import CORS
#todo Creando la aplicacion
app=Flask(__name__)
CORS(app)

from app import rutas
