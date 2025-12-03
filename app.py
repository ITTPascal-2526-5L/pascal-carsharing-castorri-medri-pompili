# Se flask non è riconosciuto, così come il venv, controlla dove sono allocati python e pip.
# se sono nella cartella sbagliata, cioè fuori progetto, disinstalla il venv e reinstallalo bene
# ricontrolla, se sono corrette le cartelle allora reinstalla flask.

# Questo file serve solo per lanciare l'istanza.
# L'istanza e le sue dipendenze (librerie) sono state settate all'interno del file __init__.py all'interno del package "app".

# Da dentro il pacchetto app prendi questa funzione
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)