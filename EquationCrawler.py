import os
import re
import time
import random
import json
import asyncio
import aiohttp
import async_timeout
import requests
import multiprocessing
from bs4 import BeautifulSoup


class SuperCrawler:

    """
    This class download equations from Wiki
    Start form key word "Euler function"
    1.find and download all equations on current website
    2.get a url on current website and visit this url
    3.If there are quations on the new website, do step1, otherwise do step2
    4.repeat 1-3 until we have enough equations
    """

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q = 0.8',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://en.wikipedia.org/wiki/Bobby_Smith_(footballer,_born_1870)',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    parameters = {}


    def __init__(self, num):
        self.num = num
        self.equations = []
        self.session = requests.session()
        self.session.headers = self.headers

    def find_equation_and_url(self, url):
        """
        find and save all equations and possible urls, which link
        to other websites with equations
        """
        results_equ = []
        results_url = []
        time.sleep(1.5)
        response = self.session.get(url, params=self.parameters)
        html = response.content
        soup = BeautifulSoup(html, features='lxml')
        jsobj = list(map(soup.find_all, ['math', 'a']))
        for the_obj in jsobj[0]:
            if 'alttext' in the_obj.attrs.keys():
                results_equ.append(the_obj['alttext'])
        for the_obj in jsobj[1]:
            if 'href' in the_obj.attrs.keys():
                result = the_obj['href']
                if re.match('/wiki', result):
                    results_url.append('https://en.wikipedia.org' + the_obj['href'])
        results = {'equation': results_equ, 'url': results_url}
        return results

    def read_equations(self, unparsed_url, parsed_url, lock):
        all_equations = []
        with lock:
            url = unparsed_url.pop(0)
            print(url)
            parsed_url.append(url)
            parsed_url = list(set(parsed_url))
            dicts = self.find_equation_and_url(url)
            new_equs = dicts['equation']
            new_urls = dicts['url']
            all_equations.extend(new_equs)
            unparsed_url.extend(list(set(new_urls).difference(set(parsed_url))))
        return all_equations


    def add_to_equations(self, new_equations):
        print(len(new_equations))
        with open('equation1.txt', 'a+', encoding='UTF-8') as f:
            for equations in new_equations:
                result = equations[1:-1] + '\n'
                f.write(result)


    def run(self):
        manager = multiprocessing.Manager()
        lock = manager.Lock()
        pool = multiprocessing.Pool()
        parsed_url = manager.list()
        unparsed_url = manager.list(['https://en.wikipedia.org/wiki/Euler%27s_totient_function'])
        for i in range(100):
            if len(self.equations) < self.num:
                pool.apply_async(self.read_equations, (unparsed_url, parsed_url, lock,), callback=self.add_to_equations)
                print(len(self.equations))
            else:
                print("stop")
                pool.terminate()
                break
        pool.close()
        pool.join()
        print(len(self.equations))

        print("******************** Finished! ********************")


if __name__ == "__main__":
    myCrawler = SuperCrawler(1000)
    myCrawler.run()
