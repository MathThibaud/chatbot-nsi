from flask import Flask

app = Flask(__name__)

# Importer les routes *après* la création de `app`
from . import main
