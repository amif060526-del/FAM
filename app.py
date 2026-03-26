
from flask import Flask, request, render_template

app = Flask(__name__)

# 建立題庫
zh_ko_dict = {
    "你好": "안녕하세요",
    "안녕하세요" : "你好",
    "謝謝": "감사합니다",
    "對不起": "죄송합니다",
    "早安": "좋은 아침",
    "晚安": "안녕히 주무세요",
    "老師": "선생님",
    "學生": "학생",
    "朋友": "친구",
    "家人": "가족",
    "愛": "사랑"
}

zh_en_dict = {
    "你好": "Hello",
    "謝謝": "Thank",
    "對不起": "Sorry",
    "早安": "Goodmorning",
    "晚安": "Goodnight",
    "老師": "Teacher",
    "學生": "Student",
    "朋友": "friend",
    "家人": "family",
    "愛": "love"
}




# homepage process
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/ask', methods=['GET', 'POST'])
def ask():
    answer = None
    question = ""
    source = ""
    dict_type = request.form.get('dict_type', 'en')  # 使用者選擇的字典

    if request.method == 'POST':
        question = request.form.get('question', '').strip()

        # 根据使用者选择切换字典
        if dict_type == 'ko':
            current_dict = zh_ko_dict
        else:
            current_dict = zh_en_dict

        # 查本地题库
        answer = current_dict.get(question)

        # 如果找不到
        if not answer and question:
            answer = "题库中没有这个字"
            source = "未找到"
        else:
            source = "本地题库"

    return render_template(
        'ask.html',
        question=question,
        answer=answer,
        source=source,
        dict_type=dict_type
    )
 
    return render_template('ask.html', question=question, answer=answer, source=source, dict_type=dict_type)



if __name__ == '__main__':
    # 開發用；部署用 gunicorn（見下方）
    app.run(host='0.0.0.0', debug=False)

