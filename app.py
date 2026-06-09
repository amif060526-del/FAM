import os
from flask import Flask, render_template, request
import requests
import openai

app = Flask(__name__)

# 從環境變數讀取 API 金鑰（安全作法）
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route('/')
def home():
    return render_template('index.html')

# ==========================================
# 1. 天氣查詢功能
# ==========================================
@app.route('/weather', methods=['GET', 'POST'])
def weather():
    weather_data = None
    error_msg = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            # 使用 OpenWeatherMap API (預設用 metric 攝氏單位, lang=zh_tw 中文)
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=zh_tw"
            try:
                response = requests.get(url).json()
                if response.get("cod") == 200:
                    weather_data = {
                        "city": response.get("name"),
                        "temp": response["main"]["temp"],
                        "humidity": response["main"]["humidity"],
                        "desc": response["weather"][0]["description"],
                        "icon": response["weather"][0]["icon"]
                    }
                else:
                    error_msg = "找不到該城市，請檢查拼字（例如：Taipei）。"
            except Exception as e:
                error_msg = "天氣服務連線失敗。"
                
    return render_template("weather.html", weather=weather_data, error=error_msg)

# ==========================================
# 2. 電影推薦功能
# ==========================================
@app.route('/movie', methods=['GET', 'POST'])
def movie():
    movies = []
    error_msg = None
    
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword:
            # 使用 TMDB API 搜尋電影 (中文語系)
            url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={keyword}&language=zh-TW"
            try:
                response = requests.get(url).json()
                results = response.get('results', [])
                
                for item in results[:6]:  # 取前 6 筆結果
                    movies.append({
                        "title": item.get("title"),
                        "overview": item.get("overview", "暫無劇情簡介。"),
                        "release_date": item.get("release_date", "未知"),
                        "poster": f"https://image.tmdb.org/t/p/w500{item.get('poster_path')}" if item.get('poster_path') else None
                    })
                if not movies:
                    error_msg = "沒有找到相關電影。"
            except Exception as e:
                error_msg = "電影服務連線失敗。"
                
    return render_template("movie.html", movies=movies, error=error_msg)

# ==========================================
# 3. AI 聊天網站功能
# ==========================================
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    answer = ""
    user_message = ""
    
    if request.method == 'POST':
        user_message = request.form.get('message')
        if user_message:
            try:
                # 呼叫新版 OpenAI API
                client = openai.OpenAI(api_key=OPENAI_API_KEY)
                response = client.chat.completions.create(
                    model="gpt-4o-mini",  # 運用最新、CP值最高的模型
                    messages=[
                        {"role": "system", "content": "你是一個幽默且樂於助人的期末報告專題助理。"},
                        {"role": "user", "content": user_message}
                    ]
                )
                answer = response.choices[0].message.content
            except Exception as e:
                answer = f"AI 暫時離線中... 錯誤訊息: {str(e)}"
                
    return render_template("chat.html", answer=answer, user_message=user_message)

if __name__ == '__main__':
    app.run(debug=True)
