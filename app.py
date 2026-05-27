from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

@app.route('/')
def index():
    # 讀取 CSV
    df = pd.read_csv('big_mart_sales.csv')

    # 取得欄位名稱與資料型別
    column_info = pd.DataFrame({
        'Column': df.columns,
        'Data Type': df.dtypes.astype(str)
    })

    # Outlet_Size 缺失值補值
   most_common = df['Outlet_Size'].mode()[0]
    df['Outlet_Size'].fillna(most_common, inplace=True)

    # Outlet_Type 統計
    outlet_counts = df['Outlet_Type'].value_counts()

    # 建立 static 資料夾
    if not os.path.exists('static'):
        os.makedirs('static')

    # 畫圖
    plt.figure(figsize=(8, 5))
    outlet_counts.plot(kind='bar')
    plt.title('Outlet Type Histogram')
    plt.xlabel('Outlet Type')
    plt.ylabel('Count')
    plt.xticks(rotation=30)
    plt.tight_layout()

    chart_path = 'static/outlet_type_hist.png'
    plt.savefig(chart_path)
    plt.close()

    return render_template(
        'index.html',
        tables=[column_info.to_html(classes='table table-striped', index=False)],
        chart=chart_path,
        missing_fixed=most_common
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
