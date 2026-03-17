import requests
import json

url = "https://spark-api-open.xf-yun.com/x2/chat/completions" # 假设是这个地址，请根据你的文档确认
headers = {
    "Authorization": "Bearer 你的API密码",
    "Content-Type": "application/json"
}

data = {
    "model": "spark-x", # 或者你用的 spark-x
    "user": "user_123",
    "messages": [
        {"role": "user", "content": "推荐两个国内适合自驾的景点"}
    ],
    "stream": False, # 代码里先关掉流式，方便处理
    "tools": [
        {
            "type": "web_search",
            "web_search": {"enable": True, "search_mode": "deep"}
        }
    ]
}

response = requests.post(url, headers=headers, json=data)
result = response.json()

# 提取并打印最终回答
answer = result['choices'][0]['message']['content']
print("🤖 AI 的回答：")
print(answer)