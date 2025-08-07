from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ⬅️ Esto permite CORS para todas las rutas

@app.route('/youtube-info', methods=['POST'])
def receive_info():
    data = request.get_json()
    print("[YouTube] Información recibida:")
    for k, v in data.items():
        print(f"{k}: {v}")
    print("-" * 30)
    return '', 204

if __name__ == '__main__':
    app.run(port=5000)
