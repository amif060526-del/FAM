from flask import Flask, render_template
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

html_doc = """
<div class="result-item">
  <div class="period-title">第115000049期</div>
  <div class="period-date">開獎日期 115/05/01</div>
  <div class="balls">
    <span class="ball ball-orange">07</span>
    <span class="ball ball-orange">22</span>
    <span class="ball ball-orange">27</span>
    <span class="ball ball-orange">35</span>
    <span class="ball ball-orange">43</span>
    <span class="ball ball-orange">48</span>
  </div>
  <span class="ball ball-red">45</span>
</div>
"""

@app.route("/")
def index():
    soup = BeautifulSoup(html_doc, "html.parser")

    period = soup.find("div", class_="period-title").text
    date = soup.find("div", class_="period-date").text

    orange_balls = soup.find_all("span", class_="ball ball-orange")
    numbers = [ball.text for ball in orange_balls]

    special_ball = soup.find("span", class_="ball ball-red").text

    return render_template(
        "index.html",
        period=period,
        date=date,
        numbers=numbers,
        special_ball=special_ball
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
