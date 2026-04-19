from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from etf_data import ETF_DATA
import time

app = Flask(__name__)
app.secret_key = "etfforai_2024_secret"

# 登录页
@app.route('/')
def index():
    if 'logged' in session:
        etf_list = list(ETF_DATA.keys())
        return render_template('index.html', etf_list=etf_list)
    return render_template('login.html')

# 登录接口
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username == '123' and password == 'l123@':
        session['logged'] = True
        return jsonify({"code":200})
    return jsonify({"code":403,"msg":"账号或密码错误"})

# 退出登录
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# AI分析接口
@app.route('/get_advice', methods=['POST'])
def get_advice():
    if 'logged' not in session:
        return jsonify({"code":403,"msg":"请先登录"})
    
    etf_key = request.json.get('etf_key', '').strip()
    data = ETF_DATA.get(etf_key)
    
    if not data:
        return jsonify({"code":404,"msg":"未找到数据"})
    
    # 固定延迟20秒，模拟AI思考
    time.sleep(20)

    return jsonify({
        "code":200,
        "data":{
            "code": data['code'],
            "name": data['name'],
            "suggest": data['suggest'],
            "confidence": data['confidence'],
            "reason": data['reason'],
            "date": "2026年4月21日"  # 固定日期
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)