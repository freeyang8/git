from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


# 1. 首页路由 (现在只需要渲染模板，不需要传变量)
@app.route('/')
def home():
    return render_template('index.html')


# 2. 处理表单提交的路由
@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form.get('username_input')

    if user_input:
        # 重定向到结果页面
        return redirect(url_for('hello', name=user_input))
    else:
        # 如果为空，返回首页
        return redirect(url_for('home'))


# 3. 展示结果的动态路由
@app.route('/hello/<name>')
def hello(name):
    # 结果页面的 HTML
    html_response = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>你好 {name}</title>
        <style>
            body {{ font-family: Arial, sans-serif; text-align: center; padding: 50px; background-color: #e8f6f3; }}
            h1 {{ color: #27ae60; font-size: 3em; margin-bottom: 10px; }}
            p {{ font-size: 1.2em; color: #555; }}
            a {{ color: #3498db; text-decoration: none; font-size: 1.2em; display: inline-block; margin-top: 20px; }}
            a:hover {{ text-decoration: underline; }}
        </style>
    </head>
    <body>
        <a href="/">⬅️ 再问一个问题</a>
    </body>
    </html>
    """
    return html_response


if __name__ == '__main__':
    app.run(debug=True, port=5000)