import re
import random
import os
import time
import json
import requests



class ImgCrawler:
    """
    This class download normal images from Baidu.com
    """
    header = {
        'Accept-Encoding': 'gzip, deflate, br',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }
    param = {
        'tn': 'resultjson_com',
        'ipn': 'rj',
        'ct': '201326592',
        'fp': 'result',
        'queryWord': 'deep learning',
        'cl': '2',
        'lm': '-1',
        'ie': 'utf-8',
        'oe': 'utf-8',
        'st': '-1',
        'word': 'deep learning',
        'face': '0',
        'istype': '2',
        'nc': '1',
        'pn': '0',
        'rn': '50',
        'gsm': '12c',
    }

    def __init__(self, total_amount, key):
        self.url = "https://image.baidu.com/search/acjson"
        self.total_amount = total_amount
        self.param['word'] = key
        self.param['queryWord'] = key

    def get_imgs_batch(self, start_num):
        urls = []
        self.param['pn'] = str(start_num)
        r = requests.get(self.url, params=self.param, headers=self.header)
        try:
            jsobj = json.loads(r.text)
            for x in jsobj['data']:
                if 'thumbURL' in x:
                    urls.append(x['thumbURL'])
        except json.decoder.JSONDecodeError:
            print("OOOps~ An Error occurred")
        return urls

    def get_imgs(self):
        itr = self.total_amount//50
        img_id = 0
        for i in range(itr):
            for img in self.get_imgs_batch(i*50):
                img_name = str(img_id) + ".png"
                time.sleep(random.randint(1, 2))
                img_url = requests.get(img, stream=True)
                with open('./Images/%s' % img_name, 'wb') as f:
                    for chunk in img_url.iter_content(chunk_size=256):
                        f.write(chunk)
                img_id += 1
                print('Image %s is already saved' % img_name)


if __name__ == "__main__":
    crawler = ImgCrawler(100, 'deep learning')
    crawler.get_imgs()