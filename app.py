from flask import Flask, render_template, request
import requests
import openai

app = Flask(__name__)

# 天氣API
WEATHER_API_KEY = "你的OpenWeatherAPI"

# OpenAI API
OPENAI_API_KEY = "你的OpenAI_API"

# TMDB API
TMDB_API_KEY = "你的TMDB_API"

@app.route('/')
def home():
    return render_template('index.html')


# ==================
# 天氣查詢
# ==================
@app.route('/weather', methods=['GET', 'POST'])
def weather():

    weather_data = None

    if request.method == 'POST':

        city = request.form['city']

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"

        response = requests.get(url).json()

        if response.get("main"):

            weather_data = {
                "city": city,
                "temp": response["main"]["temp"],
                "desc": response["weather"][0]["description"]
            }

    return render_template(
        "weather.html",
        weather=weather_data
    )


# ==================
# 電影推薦
# ==================
@app.route('/movie', methods=['GET', 'POST'])
def movie():

    movies = []

    if request.method == 'POST':

        keyword = request.form['keyword']

        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={keyword}"

        response = requests.get(url).json()

        for item in response['results'][:5]:

            movies.append({
                "title": item["title"],
                "overview": item["overview"]
            })

    return render_template(
        "movie.html",
        movies=movies
    )


# ==================
# AI聊天
# ==================
@app.route('/chat', methods=['GET','POST'])
def chat():

    answer = ""

    if request.method == 'POST':

        user_message = request.form['message']

        client = openai.OpenAI(
            api_key=OPENAI_API_KEY
        )

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role":"user",
                    "content":user_message
                }
            ]
        )

        answer = response.choices[0].message.content

    return render_template(
        "chat.html",
        answer=answer
    )


if __name__ == '__main__':
    app.run(debug=True)
