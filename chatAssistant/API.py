# coding: utf-8
import _thread as thread
import base64
import datetime
import hashlib
import hmac
import json
from urllib.parse import urlparse
import ssl
from datetime import datetime
from time import mktime
from urllib.parse import urlencode
from wsgiref.handlers import format_date_time
import websocket
import sys


# --- 辅助类：收集结果 ---
class ResultCollector:
    def __init__(self):
        self.content = ""  # 存储完整内容用于返回
        self.error = None  # 存储错误
        self.is_finished = False


class Ws_Param(object):
    def __init__(self, APPID, APIKey, APISecret, gpt_url):
        self.APPID = APPID
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.host = urlparse(gpt_url).netloc
        self.path = urlparse(gpt_url).path
        self.gpt_url = gpt_url

    def create_url(self):
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        signature_origin = "host: " + self.host + "\n"
        signature_origin += "date: " + date + "\n"
        signature_origin += "GET " + self.path + " HTTP/1.1"

        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = f'api_key="{self.APIKey}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')

        v = {
            "authorization": authorization,
            "date": date,
            "host": self.host
        }
        url = self.gpt_url + '?' + urlencode(v)
        return url


# --- 回调函数修改版 ---

def on_error(ws, error, collector):
    collector.error = str(error)
    # 错误时打印换行，避免破坏输出格式
    print(f"\n### Error: {error}")
    ws.close()


def on_close(ws, close_status_code, close_msg, collector):
    collector.is_finished = True
    # 连接正常关闭时，打印一个换行符，结束流式输出行
    if not collector.error:
        print("")


def on_open(ws):
    thread.start_new_thread(run, (ws,))


def run(ws, *args):
    data = json.dumps(gen_params(appid=ws.appid, query=ws.query, domain=ws.domain))
    ws.send(data)


def on_message(ws, message, collector):
    try:
        data = json.loads(message)
        code = data['header']['code']

        if code != 0:
            collector.error = f"请求错误: {code}, {data}"
            ws.close()
        else:
            choices = data["payload"]["choices"]
            status = choices["status"]

            if "text" in choices and len(choices["text"]) > 0:
                content = choices["text"][0].get("content", "")

                # 【关键修改 1】累加内容，用于最后返回
                collector.content += content

                # 【关键修改 2】实时打印内容 (流式输出)
                # end='' 表示不换行，flush=True 表示立即输出而不等待缓冲区满
                print(content, end='', flush=True)

            if status == 2:
                collector.is_finished = True
                ws.close()
    except Exception as e:
        collector.error = f"解析消息失败: {str(e)}"
        ws.close()


def gen_params(appid, query, domain):
    data = {
        "header": {"app_id": appid, "uid": "1234"},
        "parameter": {
            "chat": {
                "domain": domain,
                "temperature": 0.5,
                "max_tokens": 4096,
                "auditing": "default",
            }
        },
        "payload": {
            "message": {"text": [{"role": "user", "content": query}]}
        }
    }
    return data


# --- 核心调用函数 ---
def get_spark_response(appid, api_secret, api_key, gpt_url, domain, query):
    """
    同步调用接口：
    1. 运行过程中会实时 print 输出答案（流式效果）。
    2. 运行结束后 return 完整的字符串。
    """
    wsParam = Ws_Param(appid, api_key, api_secret, gpt_url)
    websocket.enableTrace(False)
    wsUrl = wsParam.create_url()

    collector = ResultCollector()

    def _on_open(ws):
        thread.start_new_thread(run, (ws,))

    def _on_message(ws, message):
        on_message(ws, message, collector)

    def _on_error(ws, error):
        on_error(ws, error, collector)

    def _on_close(ws, close_status_code, close_msg):
        on_close(ws, close_status_code, close_msg, collector)

    ws = websocket.WebSocketApp(
        wsUrl,
        on_open=_on_open,
        on_message=_on_message,
        on_error=_on_error,
        on_close=_on_close
    )

    ws.appid = appid
    ws.query = query
    ws.domain = domain

    # 阻塞直到连接关闭
    ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    if collector.error:
        raise Exception(collector.error)

    # 【关键修改 3】返回完整内容
    return collector.content


# 兼容旧的 main 函数
def main(appid, api_secret, api_key, gpt_url, domain, query):
    try:
        print(">>> 开始回答：")
        full_text = get_spark_response(appid, api_secret, api_key, gpt_url, domain, query)
        print("<<< 回答结束")
        return full_text
    except Exception as e:
        print(f"\n发生异常: {e}")
        return None


