①如何获取token调用讯飞大模型API，参考操作：
https://blog.csdn.net/weixin_56649281/article/details/136569427
②在 控制台-讯飞开放平台获取（点击“更多服务信息查询”查看）
    "gpt_url"和"domain"查看方式：右下角的“服务信息”->"文档"
    "gpt_url"为请求地址
    并且在main.py中CONFIG列表中添加配置自己的参数（将引号内的‘你的’替换掉）
    "appid": "你的",
    "api_secret": "你的",
    "api_key": "你的",
    "gpt_url": "你的",
    "domain": "你的"
③点击启动，终端会生成地址，在浏览器输入地址，即可使用
注：终端会接收回复，接收完毕后会直接粘贴到网页内
