from flask import Flask

app = Flask(__name__)

print("✅ Flask app créée")

# Importer les routes *après* la création de `app`
from . import main

application = app
print("✅ Fin de main.py atteinte")