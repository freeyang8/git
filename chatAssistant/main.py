# main.py
from flask import Flask, render_template, request, jsonify
import API

app = Flask(__name__)

# 配置你的讯飞星火参数
CONFIG = {
    "appid": "你的",
    "api_secret": "你的",
    "api_key": "你的",
    "gpt_url": "你的",
    "domain": "你的"
}


@app.route('/')
def index():
    """显示首页表单"""
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    """处理表单提交，调用 AI 并返回结果"""
    # 1. 获取网页输入框的内容
    user_query = request.form.get('username_input')

    if not user_query:
        return jsonify({"error": "请输入内容"}), 400

    print(f"--- 收到用户问题: {user_query} ---")

    try:
        # 2. 准备调用参数
        config = CONFIG.copy()
        config['query'] = user_query

        print("--- 思考中 (AI 正在生成)... ---")

        # 3. 调用 API.py 中的函数
        # 注意：因为 API.py 里有 print 输出，这些内容会显示在运行 main.py 的黑色控制台窗口中
        result_text = API.get_spark_response(**config)

        print("--- 回答生成完毕 ---")

        # 4. 将结果以 JSON 格式返回给网页
        return jsonify({
            "success": True,
            "query": user_query,
            "answer": result_text
        })

    except Exception as e:
        print(f"❌ 发生错误: {e}")
        return jsonify({"success": False, "error": str(e)}), 500


if __name__ == "__main__":
    # 启动 Web 服务器
    # debug=True 表示如果代码修改，服务器会自动重启
    print("🚀 服务器已启动！请在浏览器访问: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)