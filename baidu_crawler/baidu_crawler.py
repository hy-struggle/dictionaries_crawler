# post请求
import json
import execjs
import requests

"""
    1.cookie参数和token参数是对应的
    2.生成sign参数需要通过调用baidu.js程序
"""


class Baidu:

    def __init__(self, word):
        self.word = word
        self.sign = self.get_sign()
        self.url = 'https://fanyi.baidu.com/v2transapi'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',

            'cookie': 'BIDUPSID=EF5D2DCB95CD02713C504B965E680572; PSTM=1508391259; '
                      'BAIDUID=FE94A1C6870007735C0EA30CA092352A:FG=1; '
                      'BDUSS=HhpVTc3VjZrQ2ppRX5RcVFoQW9-WExTQ29zYWR-'
                      'TUluOUQxRGVaWHZrWGlOWmRkRVFBQUFBJCQAAAAAAAAAAAEAAAAUxiG2ZnJlZc31vNG'
                      '~pQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
                      'OKob13iqG9dW; locale=zh; __guid=37525047.783289347368707300.1568961749022.282; '
                      'REALTIME_TRANS_SWITCH=1; FANYI_WORD_SWITCH=1; HISTORY_SWITCH=1; SOUND_SPD_SWITCH=1; '
                      'SOUND_PREFER_SWITCH=1; to_lang_often=%5B%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u'
                      '4E2D%u6587%22%7D%2C%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%5D;'
                      ' from_lang_often=%5B%7B%22value%22%3A%22en%22%2C%22text%22%3A%22%u82F1%u8BED%22%7D%2C'
                      '%7B%22value%22%3A%22zh%22%2C%22text%22%3A%22%u4E2D%u6587%22%7D%5D; yjs_js_security_pass'
                      'port=67080cbdf7d8d4ad0eb8f1513b5feb52c128c29b_1569324592_js; monitor_count=3; Hm_lvt_'
                      '64ecd82404c51e03dc91cb9e8c025574=1568961749,1569324577,1569324592,1569324674; Hm_lpvt_'
                      '64ecd82404c51e03dc91cb9e8c025574=1569324674; __yjsv5_shitong=1.0_7_9055159b9a5e975fcd2c2'
                      'c48931b3bc7b406_300_1569324677995_117.32.216.70_70981334'
        }

        # 构造post请求的参数
        self.post_data = {
            'from': 'en',
            'to': 'zh',
            'query': self.word,
            'simple_means_flag': '3',
            'sign': self.sign,
            'token': '8d588b57816e1213f2bcfaf52bddbbe2'
        }

    # 获取sign
    def get_sign(self):
        query = self.word  # 是要翻译的内容
        with open('baidu.js', 'r', encoding='utf-8') as f:
            ctx = execjs.compile(f.read())
        sign = ctx.call('e', query)
        # print(sign)
        return sign

    # 发送请求
    def request_post(self):
        res = requests.post(url=self.url, headers=self.headers, data=self.post_data)
        # print(res.content.decode())
        json_data = json.loads(res.content.decode())
        return json_data

    # 判断post参数
    def judge_post(self):
        if self.is_chinese(self.word):
            self.post_data['from'] = 'zh'
            self.post_data['to'] = 'en'
            # print(self.word.encode().isalpha())

    # 判断是否为汉字
    @staticmethod
    def is_chinese(uchar):
        if u'\u4e00' <= uchar <= u'\u9fa5':
            return True
        else:
            return False

    # 解析数据
    @staticmethod
    def parse_data(data):
        # dict_data = json.loads(data)
        print(data['trans_result']['data'][0]['dst'])

    def run(self):
        self.judge_post()
        json_data = self.request_post()
        self.parse_data(json_data)
        # print(data)


if __name__ == '__main__':
    word = input("翻译：")
    baidu = Baidu(word)
    baidu.run()
