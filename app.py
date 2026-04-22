
@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'POST':
        # 2. 讀取使用者輸入的股票號碼
        question = request.form.get('question', '').strip()
        # 3. 查詢股票號碼的收盤價
        answer = zh_ko_dict.get(question, "抱歉，我目前沒有這個股票號碼。")
        # 4. 回傳答案給使用者
        return render_template('stock.html', question=question, answer=answer)
    # GET 時給空白欄位
    return render_template('stock.html', question="", answer="")
