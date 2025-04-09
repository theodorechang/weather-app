from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

# 這裡需要從 OpenWeatherMap 獲取 API key
# 為了演示，我們使用一個預設值，實際使用時應該放在 .env 文件中
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'your_api_key_here')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error = None

    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            try:
                # 調用 OpenWeatherMap API
                url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=zh_tw'
                print(f'正在請求 URL: {url}')
                response = requests.get(url)
                data = response.json()
                print(f'API 回應: {data}')

                if response.status_code == 200:
                    weather_data = {
                        'city': data['name'],
                        'temperature': round(data['main']['temp']),
                        'description': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                        'humidity': data['main']['humidity'],
                        'wind_speed': data['wind']['speed']
                    }
                else:
                    error = f'錯誤: {response.status_code}, 訊息: {data.get("message", "未知錯誤")}'

            except Exception as e:
                error = '獲取天氣資訊時發生錯誤'

    return render_template('index.html', weather=weather_data, error=error)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
