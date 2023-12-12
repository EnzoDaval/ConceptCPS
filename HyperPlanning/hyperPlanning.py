import http.server
import socketserver
import json

PORT = 8000

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Gérer la requête pour obtenir tous les cours
        if self.path == '/get-json':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()

            with open('data/data.json', 'r') as file:
                data = json.load(file)
                self.wfile.write(json.dumps(data).encode())

        # Gérer la requête pour obtenir un cours spécifique
        elif self.path.startswith('/get-json/'):
            course_id = self.path.split('/')[-1]  # Extraire l'ID du cours de l'URL

            with open('data/data.json', 'r') as file:
                data = json.load(file)

            # Trouver le cours correspondant à l'ID
            course_data = next((course for course in data["courses"] if course["courseID"] == course_id), None)

            if course_data:
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(course_data).encode())
            else:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"Course not found")

        # Si la requête ne correspond à aucune des routes précédentes
        else:
            self.send_response(404)
            self.end_headers()

Handler = MyHttpRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("Serving at port", PORT)
    httpd.serve_forever()
