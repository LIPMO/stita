import json
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

# Variables globales pour stocker les données GPS
current_speed = 0
current_latitude = 0
current_longitude = 0

# Classe pour gérer les requêtes HTTP
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == "/":
            # Affiche la page HTML avec les données actuelles
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html_content = f"""
            <!DOCTYPE html>
            <html lang="fr">
            <head>
                <meta charset="UTF-8">
                <title>Dashboard Moto/Trottinette</title>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
                <h1>Dashboard Moto/Trottinette</h1>
                <p><strong>Vitesse :</strong> {current_speed} km/h</p>
                <p><strong>Latitude :</strong> {current_latitude}</p>
                <p><strong>Longitude :</strong> {current_longitude}</p>

                <canvas id="myChart" width="400" height="200"></canvas>
                <script>
                    var ctx = document.getElementById('myChart').getContext('2d');
                    var myChart = new Chart(ctx, {
                        type: 'line',
                        data: {
                            labels: ['Vitesse'],
                            datasets: [{
                                label: 'Vitesse (km/h)',
                                data: [{current_speed}],
                                borderColor: 'rgb(75, 192, 192)',
                                fill: false
                            }]
                        }
                    });
                </script>
            </body>
            </html>
            """
            self.wfile.write(html_content.encode('utf-8'))
        
    def do_POST(self):
        if self.path == "/update_gps":
            # Récupère les données JSON envoyées par GPS Logger
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))

            global current_speed, current_latitude, current_longitude
            current_speed = data.get('speed', 0)
            current_latitude = data.get('latitude', 0)
            current_longitude = data.get('longitude', 0)

            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Données GPS mises à jour")

# Démarre le serveur
def run(server_class=HTTPServer, handler_class=SimpleHTTPRequestHandler, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Serving on port {port}...')
    httpd.serve_forever()

if __name__ == "__main__":
    run()
