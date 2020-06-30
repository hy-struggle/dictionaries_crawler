# post请求
import json
import execjs
import requests


class Google:
    def __init__(self, word):
        self.word = word
        self.tk = self.get_tk()
        self.sl = 'en'
        self.tl = 'zh-CN'
        self.url = "http://translate.google.cn/translate_a/single?client=t" \
                   "&sl=%s&tl=%s&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
                   "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
                   "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (self.sl, self.tl, self.tk, self.word)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }

    # 判断是否为汉字
    @staticmethod
    def is_chinese(uchar):
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    # 判断url参数
    def judge_url(self):
        if self.is_chinese(self.word):
            self.sl = 'zh-CN'
            self.tl = 'en'
            self.url = "http://translate.google.cn/translate_a/single?client=t" \
                       "&sl=%s&tl=%s&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
                       "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
                       "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (self.sl, self.tl, self.tk, self.word)
            # print(self.word.encode().isalpha())

    # 调用google.js获取tk
    def get_tk(self):
        query = self.word
        with open('google.js', 'r', encoding='utf-8') as f:
            ctx = execjs.compile(f.read())
        tk = ctx.call('TL', query)
        # print(sign)
        return tk

    # 发送请求
    def request_get(self):
        res = requests.get(url=self.url, headers=self.headers)
        # print(res.content.decode())
        json_data = json.loads(res.content.decode())
        return json_data

    # 解析数据
    @staticmethod
    def parse_data(data):
        print(data[0][0][0])

    def run(self):
        self.judge_url()
        # print(self.url)
        # print('sl:%s' % self.sl)
        # print('tl:%s' % self.tl)
        json_data = self.request_get()
        self.parse_data(json_data)
        # print(json_data)
        # self.parse_data(data)


if __name__ == '__main__':
    word = input("翻译：")
    google = Google(word)
    google.run()
