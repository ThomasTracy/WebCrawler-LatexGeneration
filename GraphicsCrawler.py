import os
import time
import json
import asyncio
import aiohttp
import async_timeout
import requests
import multiprocessing
from bs4 import BeautifulSoup


class GraphicsCrawler:
    """
    This class locates and downloads Graphics from mathworks.com
    """

    __headers = {
        'Referer': 'https://de.mathworks.com/help/matlab/examples.html?category=graphics',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

    __params = {
        'category': 'graphics',
        'product': 'matlab',
        'docroot': 'https://de.mathworks.com/help'
    }

    __urls = []

    __imgUrls = []


    def __init__(self, urls='https://de.mathworks.com/help/search/examplelist/doccenter/en/R2018b'):
        self.url = urls
        self.session = requests.session()
        self.session.headers = self.__headers
        # self.pool = Pool()

    # extract all the websites, that include Graphics with recursion
    def __recursionUrl(self, js):

        '''
        Use recursion to parse the respone of a website
        and get all of the wanted elements( here is URL) in this wersite
        :param js:
        :return:
        '''

        key = 'url'
        for value in js.values():
            if isinstance(value, dict):
                self.__recursionUrl(value)
            elif isinstance(value, list):
                for the_value in value:
                    self.__recursionUrl(the_value)
        if key in js:
            self.__urls.append(js[key])

    def __getUrls(self):

        '''
        Extract all the possible websites,
        in which the wanted graphics exist
        :return:
        '''

        response = self.session.get(self.url,params=self.__params)
        jsobj = json.loads(response.text)
        self.__recursionUrl(jsobj)
        urlset = list(set(self.__urls))
        urlset.sort(key=self.__urls.index)
        self.__urls = []
        self.__urls = urlset

    def getGraphicUrls(self, url, list):

        '''
        Parse a website, which contains Graphics.
        Then extract all urls of Graphic from this website
        :param url:
        :param list:
        :return:
        '''

        # print("Pid:", os.getpid(), " | ", "Time:", time.ctime())
        time.sleep(1.5)
        response = self.session.get(url)
        soup = BeautifulSoup(response.text, features='lxml')
        graphics = soup.find_all('div', {'class': 'mediaobject'})
        for graphic in graphics:
            x = graphic.find('img')
            graphic_url = 'https://de.mathworks.com/help' + x['src'][5:]
            if graphic_url not in list:
                list.append(graphic_url)

    def download(self, name, url):
        img_name = 'Graphic' + str(name) + '.png'
        time.sleep(1.5)
        theGraphic = self.session.get(url, stream=True)
        with open('./graphics/%s' % img_name, 'wb') as f:
            for chunk in theGraphic.iter_content(chunk_size=256):
                f.write(chunk)
        print("Download ",name, "seccessed!")

    async def asy_download(self, session, name, url):

        '''
        Problem is how to restrict the visiting speed.
        'asybcio.sleep()' will not delay a continous visiting
        of the aimed website
        :param session: aiohttp.ClientSession()
        :param name: name of Graphic
        :param url: url of Graphic
        '''

        img_name = 'Graphic' + str(name) + '.png'
        print("Start downloading ", img_name)
        time.sleep(1.5)
        async with session.get(url, headers=self.__headers) as r:
            with open('./graphics/%s' % img_name, 'wb') as f:
                while True:
                    chunk = await r.content.read(256)
                    if chunk:
                        f.write(chunk)
                    else:
                        break
        print("Download ",name, "seccessed!")

    async def asy_run(self, loop):
        async with aiohttp.ClientSession() as session:
            tasks = [loop.create_task(self.asy_download(session, i, self.__imgUrls[i])) for i in range(len(self.__imgUrls))]
            await asyncio.wait(tasks)


    def start(self):

        '''
        Use multiprocessing parse all pages and get urls of all graphics.
        because parsing is compute-intensive
        Save all urls of graphics in global list.
        Then down load all graphics with asyncio&aiohttp.
        because downloading is io-intensive
        '''
        print("******************** Now Start Parsing Websites ********************")

        pool = multiprocessing.Pool()
        manager = multiprocessing.Manager()
        temp_list = manager.list()
        self.__getUrls()
        for url in self.__urls:
            pool.apply_async(self.getGraphicUrls, (url, temp_list,))
        pool.close()
        pool.join()
        self.__imgUrls = temp_list[:]

        print("******************** Now Start Downloading Graphics ********************")
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.asy_run(loop))
        loop.close()
        #     pool2.apply_async(self.download, (name, url, ))
        # pool2.close()
        # pool2.join()

if __name__ == "__main__":
    graphicsCrawler = GraphicsCrawler()
    start = time.time()
    print("Start: ", time.ctime())
    graphicsCrawler.start()
    end = time.time()
    print("End: ", time.ctime())
    print("Use Time: ", end-start)