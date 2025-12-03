# Settare il server Flask e il db che andremo ad utilizzare.

# In  questo file, come indicato nell'app.py devo settare le dipendenze della mia istanza che lancerò in app.py.
# Molto spesso è necessario lanciare più istanze diverse, quindi è meglio creare diverse aree di sviluppo diverse per programmatore/cliente

from flask import Flask
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config) # Config: è una clsse "nostra", per indicare in quale ambiente stiamo lavorando (sviluppo interno azienda)
    app.secret_key = 'SOME KEY'

    # Ho importato tutti i blueprints che ho registrato all'interno del /routes/__init__.py
    # ogni blueprints, ovvero progetto, corrisponde ad una relazione simili 1 a 1 con le funzionalità del software che sto realizzando
    from .routes import blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
