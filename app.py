from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Сервис для получения погоды
@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', default='London')
    api_key = '9a41869dc1f75ba7dc852c1ce508b17e'  # Пример API для получения погоды
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        return jsonify({
            'city': city,
            'temperature': data['main']['temp'],
            'weather': data['weather'][0]['description']
        })
    else:
        return jsonify({'error': 'City not found'}), 404

# Сервис для рекомендаций
@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    weather = request.args.get('weather')

    if weather:
        if 'rain' in weather:
            return jsonify({"recommendation": "Take an umbrella!"})
        elif 'clear' in weather:
            return jsonify({"recommendation": "It’s a great day to go outside!"})
        else:
            return jsonify({"recommendation": "Stay indoors and stay warm."})
    return jsonify({"recommendation": "Please provide weather data."})

# Сервис для истории запросов
history = []

@app.route('/history', methods=['GET'])
def get_history():
    return jsonify({'history': history})

@app.route('/add_history', methods=['POST'])
def add_history():
    city = request.json.get('city')
    history.append({'city': city})
    return jsonify({'message': 'City added to history'})

if __name__ == "__main__":
    print("Starting Flask application...")  # для проверки запуска
    app.run(debug=True, host='0.0.0.0', port=5000)
