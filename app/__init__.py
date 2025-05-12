from flask import Flask

app = Flask(__name__)

# On importe les routes (dans main.py)
from . import main
