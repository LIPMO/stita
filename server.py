from flask import Flask, request, render_template

app = Flask(__name__)

# Variables globales pour stocker les données GPS
current_speed = 0
current_latitude = 0
current_longitude = 0

@app.route('/')
def index():
    return render_template('index.html', vitesse=current_speed, latitude=current_latitude, longitude=current_longitude)

@app.route('/update_gps', methods=['POST'])
def update_gps():
    global current_speed, current_latitude, current_longitude
    # Récupérer les données envoyées par GPS Logger
    data = request.json
    current_speed = data.get('speed', 0)  # Vitesse en km/h
    current_latitude = data.get('latitude', 0)
    current_longitude = data.get('longitude', 0)
    return "Données GPS mises à jour", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
