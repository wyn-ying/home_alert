# -*- coding:utf-8 -*-
'''
钉钉官方文档，可以有更多格式，@人，发链接等功能
https://open-doc.dingtalk.com/docs/doc.htm?spm=a219a.7629140.0.0.karFPe&treeId=257&articleId=105735&docType=1
'''
import requests
import ConfigParser

#增加群机器人，复制url
Config = ConfigParser.ConfigParser()
Config.read('settings.conf')
url = Config.get('dingtalk','url')
class DingtalkMsg:
    def __init__(self):
        pass

    def send(self, msg):
        a = {
            "msgtype": "text", 
            "text": {"content": msg}
        }
        r = requests.post(url, json=a)
        print(r)
        print(r.text)

if __name__ == '__main__':
    dm = DingtalkMsg()
    dm.send("its a test message")
