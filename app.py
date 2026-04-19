from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from etf_data import ETF_DATA
import time

app = Flask(__name__)
# 配置Session密钥（生产环境请替换为随机强密钥）
app.secret_key = 'ETFforAI_2026_Secret_Key'

# 预设的登录账号密码
VALID_USER = {
    "username": "123",
    "password": "l123@"
}

# 登录页路由
@app.route('/')
def login_page():
    # 如果已登录，直接跳转至ETF分析页
    if session.get('is_login'):
        return redirect(url_for('index'))
    return render_template('login.html')

# 登录接口
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', '').strip()
    password = request.json.get('password', '').strip()
    
    if not username or not password:
        return jsonify({"code": 400, "msg": "账号和密码不能为空"})
    
    if username == VALID_USER['username'] and password == VALID_USER['password']:
        # 标记登录状态
        session['is_login'] = True
        session['username'] = username
        return jsonify({"code": 200, "msg": "登录成功"})
    else:
        return jsonify({"code": 401, "msg": "账号或密码错误"})

# ETF分析页（需登录才能访问）
@app.route('/index')
def index():
    # 未登录则跳转至登录页
    if not session.get('is_login'):
        return redirect(url_for('login_page'))
    etf_list = list(ETF_DATA.keys())
    return render_template('index.html', etf_list=etf_list)

# 原有ETF分析接口（增加登录校验）
@app.route('/get_advice', methods=['POST'])
def get_advice():
    # 未登录则返回未授权
    if not session.get('is_login'):
        return jsonify({"code": 401, "msg": "请先登录", "data": {}})
    
    etf_key = request.json.get('etf_key', '').strip()
    data = ETF_DATA.get(etf_key)
    
    if not data:
        return jsonify({"code":404,"msg":"未找到数据","data":{}})
    
    time.sleep(1.2)

    return jsonify({
        "code":200,
        "msg":"success",
        "data":{
            "code": data['code'],
            "name": data['name'],
            "suggest": data['suggest'],
            "confidence": data['confidence'],
            "reason": data['reason'],
            "date": "2026-04-19"
        }
    })

# 退出登录接口（可选，可根据需要添加）
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)