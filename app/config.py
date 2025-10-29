# Contiene le varie configurazioni
# Dentro il file .env vanno inserite tutte le chiavi necessarie all'applicativo per funzionare.

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    # Secret_key_db = ....