# post请求
import json

import requests


class Biying:
    def __init__(self, word):
        self.word = word
        self.url = 'https://cn.bing.com/ttranslatev3?'
        # self.url = 'https://cn.bing.com/ttranslatev3?isVertical=1&&IG=E3F2E74779804936A4B134F621FE89FB&IID=translator.5028.12'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
        # 构造post请求的参数
        self.post_data = {
            'fromLang': 'auto-detect',
            'to': 'zh-Hans',
            'text': self.word
        }

    # 判断post参数
    def judge_post(self):
        if self.is_chinese(self.word):
            self.post_data['to'] = 'en'
            # print(self.word.encode().isalpha())

    # 判断是否为汉字
    @staticmethod
    def is_chinese(uchar):
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    # 发送请求
    def request_post(self):
        res = requests.post(url=self.url, headers=self.headers, data=self.post_data)
        # print(res.content.decode())
        return res.content.decode()

    # 解析数据
    @staticmethod
    def parse_data(data):
        dict_data = json.loads(data)
        print(dict_data[0]['translations'][0]['text'])

    def run(self):
        self.judge_post()
        data = self.request_post()
        self.parse_data(data)
        # dict_data = json.loads(data)
        # print(dict_data)


if __name__ == '__main__':
    word = input("翻译：")
    by = Biying(word)
    by.run()
