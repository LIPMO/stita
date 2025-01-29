from flask import Flask, render_template
import gpsd
import time

app = Flask(__name__)

# Connecte-toi au service gpsd
gpsd.connect()

@app.route('/')
def index():
    # Récupère les données GPS
    packet = gpsd.get_current()
    
    # Vérifie si la vitesse est disponible
    if packet.speed is not None:
        speed = packet.speed * 3.6  # Vitesse en km/h
    else:
        speed = 0  # Si aucune vitesse n'est disponible
    
    inclinaison = 0  # Inclinaison fixe pour l'instant
    
    return render_template('index.html', vitesse=speed, inclinaison=inclinaison)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
