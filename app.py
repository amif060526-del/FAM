
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
    dict_type = request.form.get('dict_type', 'en') # 取得使用者选的字典
 
    if request.method == 'POST':
        question = request.form.get('question', '').strip()
        # A. 根据选择的字典类型，设定查询对象
        if dict_type == 'ko':
            current_dict = zh_ko_dict
            lang_name = "韩文"
        else:
            current_dict = en_zh_dict
            lang_name = "英文"
 
        # B. 逻辑切换点
        # 1. 先查本地字典
        answer = current_dict.get(question)
 
        # 2. 如果字典里没有这个字，就切换到AI if
        not answer and question:
            try:
                # 这里就是伺服器自动切换AI 的地方
                prompt = f"你是一个专业的{lang_name}老师。请翻译并解释这个字：{question}"
                response = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = response.choices[0].message.content
                source = "AI 即时生成" # 标注来源让使用者知道这是AI 算的
            except Exception as e:
                answer = "抱歉，目前题库找不到这个字，且AI 服务暂时无法连线。"
                source = "错误提示"
        else:
            source = "本地题库"
 
    return render_template('ask.html', question=question, answer=answer, source=source, dict_type=dict_type)



if __name__ == '__main__':
    # 開發用；部署用 gunicorn（見下方）
    app.run(host='0.0.0.0', debug=False)

