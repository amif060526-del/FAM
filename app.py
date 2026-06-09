from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# 首頁
@app.route('/')
def home():
    return render_template('index.html')


# 天氣查詢
@app.route('/weather', methods=['GET', 'POST'])
def weather():

    weather_data = None

    if request.method == 'POST':

        city = request.form['city']

        api_key = "你的OpenWeatherAPI"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=zh_tw&units=metric"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            weather_data = {
                'city': city,
                'temp': data['main']['temp'],
                'description': data['weather'][0]['description']
            }

    return render_template('weather.html', weather=weather_data)


# 電影推薦
@app.route('/movie')
def movie():

    movies = [
        "復仇者聯盟",
        "蜘蛛人：無家日",
        "玩命關頭",
        "阿凡達",
        "奧本海默",
        "全面啟動",
        "星際效應"
    ]

    return render_template('movie.html', movies=movies)


# 聊天室
@app.route('/chat', methods=['GET', 'POST'])
def chat():

    reply = ""

    if request.method == 'POST':

        message = request.form['message']

        if "你好" in message:
            reply = "你好，很高興認識你"

        elif "電影" in message:
            reply = "推薦你看奧本海默"

        elif "天氣" in message:
            reply = "可以到天氣查詢頁面查看"

        else:
            reply = "我還在學習中"

    return render_template('chat.html', reply=reply)


if __name__ == '__main__':
    app.run(debug=True)
