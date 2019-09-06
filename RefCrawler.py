import re
import random
import os
import time
import json
import requests
import multiprocessing
from bs4 import BeautifulSoup


class RefCrawler:
    """
    This class find and download references from IEEE
    and save the results in a txt
    """
    header = {
        'Accept': 'application/json,text/plain,*/*',
        'Accept-Encoding': 'gzip,deflate,br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '108',
        'Content-Type': 'application/json',
        'Cookie': '__guid=200672182.4351965091994103300.1524725436584.2788;fp=3d6a45b88193c6c2c1954dd9aa6bfb1b;unicaID=s9Wvyfe52eM-a1Giear;__utma=98802054.1270575453.1525458044.1525458044.1525458044.1;_ga=GA1.2.1270575453.1525458044;s_vi=[CS]v1|2D70CA6885312F1D-40000103E0001E2D[CE];s_fid=16D44643B96DB2F2-21E70A5644ED5271;cookieconsent_status=dismiss;_parsely_visitor={%22id%22:%22256738f5-0943-4c80-9c61-a9da0d6cf01a%22%2C%22session_count%22:1%2C%22last_session_ts%22:1542361495605};_4c_=jVJdi9swEPwrReX60mDr88OBcBxtOO6pUCh9PGxp%2FUEdy5V8zZWQ%2F34rX9IWCqV5sFY7s%2BP1TE7k2MNEtkxJLjQzgmlTbcg3%2BJnI9kTi4PPxg2xJKxqhtPBM1ZVVwFvGoPWuorZxSlJNNuQ56yjKhJGaVbQ6b4ibL%2FMn4oIH1GFVoQqObJiy7Bw91i3SCFdVy8BYY2kFpqkrkEZSRtvaWemFQd793ePDxyzCDVVGSSUKpjielkqJ%2BFMcEe2XZU7bsjwej8UAAEWIXZmgjq6PkJ7GJZXD5OG56JfDePt95wHm9yPi0zB1b7vkiqVudvRdrl7RG06v%2BNqN0O4OIcKNuHNhaiHC5CCtUApx2eEqTQzHBBHX%2BdDHcIA3WmA3oK3kK74dQbyiDsS4sv5cuguhG6HwUCInDUv27fohlw4mhM2H%2FX7%2F%2BOnzPTYXiIcsjuWcjVWvdn35h1%2BYzxqZ5FJaaqm2DHUWtNBqSfMPGTNe1wQRu7CFURYDNvLCZvI3e40aH%2Bp%2FtNumuf69shu%2FBozVXPG%2FBs7nFw%3D%3D;ipCheck=46.5.16.229;TS01d430e1=012f350623d3cabea36dda2d20a7fd44543bc36b2c680c75669fb3be33330e22141b83e49ee3c40c2517a486fe38d767776912ecfcdb422a8591d96849617940e16e7a95474709e4271ba69594e01f91084155ea9c5ee4bbf2d4a53390e508cfdbd283980de1f94033d2c10e3a7842eca9ebf2c4a821a5cebab477b2067026f8d8f5bb016532ec6d6ccee78c027c80bc664152ddcb0bb7477caad467e72bfd70994d5f4eb1;AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg=1;s_cc=true;HTML_DocIDs=["7491252","7169508"];TS011813a0_26=014082121de9fef828499c15da1de50aa1487d9a4bf3cd8b75deb863fe42eff4fc07abece9ae541a16fa4a552f31e94222cfd65e87c24930ca22e92493e8d2f92dfb659f41;WLSESSION=237134476.20480.0000;JSESSIONID=9IktrRpyFl8Q0afwD81I-Vt2S067Sx_0Ixarrlo0sma7ca4w5c3y!-938447229;TS011813a0=012f350623d7e1cd3807f3213b94f212e2e61f3940bbe05921fbae0f3c2632644979556e5c86e94811f0ff9111020afaccb655dbb95458530c32ac7fc205a17afde0197121546b67fd55b13af2ed3c3d15a7b973b0;AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=1687686476%7CMCIDTS%7C17648%7CMCMID%7C74095325415176263822874241480022061805%7CMCAAMLH-1543264423%7C6%7CMCAAMB-1543264423%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1542666823s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17667%7CvVersion%7C3.0.0;utag_main=v_id:016300b7eb54007c809dcc22ed842706c002b0640086e$_sn:16$_ss:0$_st:1542661425444$vapi_domain:ieee.org$ses_id:1542659621588%3Bexp-session$_pn:1%3Bexp-session;s_sq=ieeexplore.prod%3D%2526pid%253DSearch%252520Results%2526pidt%253D1%2526oid%253D%25250A%252509%252509%252509%252509%252509%252509%25250A%252509%252509%252509%252509%252509%2526oidt%253D3%2526ot%253DSUBMIT;monitor_count=21',
        'Host': 'ieeexplore.ieee.org',
        'Origin': 'https://ieeexplore.ieee.org',
        'Referer': 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=deep%20learning',
        'User-Agent': 'Mozilla/5.0(WindowsNT6.1;WOW64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/63.0.3239.132Safari/537.36'
    }


    def __init__(self, key, num_of_ref):
        self.num = num_of_ref
        self.url = "https://ieeexplore.ieee.org/rest/search"
        self.payloadData = {
        'newsearch': 'true',
        'queryText': key,
        'highlight': 'true',
        'pageNumber': '1',
        'returnFacets': ['ALL'],
        'returnType': 'SEARCH'
    }


    def get_references(self):
        itr = 0
        page_num = 0
        while (itr <= self.num):

            # parse the result of thesis from page to page
            page_num += 1
            self.payloadData['pageNumber'] = str(page_num)
            r = requests.post(self.url, data=json.dumps(self.payloadData), headers=self.header)
            jsobj = json.loads(r.text)
            record_len = len(jsobj['records'])
            itr += record_len

            for i in range(record_len):

                # get the thesis id of ever thesis
                doc = re.findall('\d+', jsobj['records'][i]['documentLink'])
                time.sleep(random.randint(1,2))

                # get the references through thesis_id
                data = self.find_reference(doc[0])
                with open('References.txt', 'a+', encoding='utf-8') as file:
                    file.writelines(data)
            print("<<<<<<<<<<<<<<<<Successfully written page" + str(page_num) + ">>>>>>>>>>>>>>>>")

    def find_reference(self, thesis_id):
        """
        get references from on thesis with given thesis_id
        """
        url = 'https://ieeexplore.ieee.org/rest/document/' + thesis_id + '/references'
        print(url)
        headerData = {
            'Host': 'ieeexplore.ieee.org',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'cache-http-response': 'true',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
            'Referer': url,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': '__guid=200672182.4351965091994103300.1524725436584.2788;fp=3d6a45b88193c6c2c1954dd9aa6bfb1b;unicaID=s9Wvyfe52eM-a1Giear;__utma=98802054.1270575453.1525458044.1525458044.1525458044.1;_ga=GA1.2.1270575453.1525458044;s_vi=[CS]v1|2D70CA6885312F1D-40000103E0001E2D[CE];s_fid=16D44643B96DB2F2-21E70A5644ED5271;cookieconsent_status=dismiss;_parsely_visitor={%22id%22:%22256738f5-0943-4c80-9c61-a9da0d6cf01a%22%2C%22session_count%22:1%2C%22last_session_ts%22:1542361495605};_4c_=jVJdi9swEPwrReX60mDr88OBcBxtOO6pUCh9PGxp%2FUEdy5V8zZWQ%2F34rX9IWCqV5sFY7s%2BP1TE7k2MNEtkxJLjQzgmlTbcg3%2BJnI9kTi4PPxg2xJKxqhtPBM1ZVVwFvGoPWuorZxSlJNNuQ56yjKhJGaVbQ6b4ibL%2FMn4oIH1GFVoQqObJiy7Bw91i3SCFdVy8BYY2kFpqkrkEZSRtvaWemFQd793ePDxyzCDVVGSSUKpjielkqJ%2BFMcEe2XZU7bsjwej8UAAEWIXZmgjq6PkJ7GJZXD5OG56JfDePt95wHm9yPi0zB1b7vkiqVudvRdrl7RG06v%2BNqN0O4OIcKNuHNhaiHC5CCtUApx2eEqTQzHBBHX%2BdDHcIA3WmA3oK3kK74dQbyiDsS4sv5cuguhG6HwUCInDUv27fohlw4mhM2H%2FX7%2F%2BOnzPTYXiIcsjuWcjVWvdn35h1%2BYzxqZ5FJaaqm2DHUWtNBqSfMPGTNe1wQRu7CFURYDNvLCZvI3e40aH%2Bp%2FtNumuf69shu%2FBozVXPG%2FBs7nFw%3D%3D;ipCheck=46.5.16.229;TS01d430e1=012f350623bf2c2e9a8afaa6be0eddfde554214a8c9babb84d845067ee9d3a808adc192a8b71884d670e78635747e8fcddd6727fe0c0c870884c047ea2b0b52b5bbf462b056e800af26f3dc7d5768d934254c02ed2068c356913743499f31fd8248b4bee99;AMCVS_8E929CC25A1FB2B30A495C97%40AdobeOrg=1;AMCV_8E929CC25A1FB2B30A495C97%40AdobeOrg=1687686476%7CMCIDTS%7C17648%7CMCMID%7C74095325415176263822874241480022061805%7CMCAAMLH-1543314463%7C6%7CMCAAMB-1543314463%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1542716863s%7CNONE%7CMCAID%7CNONE%7CMCSYNCSOP%7C411-17667%7CvVersion%7C3.0.0;s_cc=true;s_sq=%5B%5BB%5D%5D;JSESSIONID=-8cw5-nRmzVm_1DiLc4bMk3Zk3fCK7EonbbaVSkXOG8kA6jYSPop!-1132352026;WLSESSION=186802828.20480.0000;TS011813a0_26=014082121dbbc2f8d4061e0e218fe9bda4cf71b5b43147e072ad92edb9764a20f18848e72ef7bacb0b1f4a7afbc95d594167a96ccc36233228a52be2b7e4640a0ee8860329;utag_main=v_id:016300b7eb54007c809dcc22ed842706c002b0640086e$_sn:19$_ss:0$_st:1542715564507$vapi_domain:ieee.org$ses_id:1542713572318%3Bexp-session$_pn:2%3Bexp-session;TS011813a0=012f350623ff9c7abfa3cfffa4b4655de0910c7f9ba907e548dddfa570b13eed70b4d0838f6b15fe13c63fbfbbc15628d7f0a06d8570e9a9614e8f3b01f0bced7fb08ad6ef7e80d88d48b290424d726f8b0aeb7210;monitor_count=34'
        }
        references = []
        try:
            r = requests.get(url, headers=headerData)
        except OSError as e:
            print(e)
            return ''
        try:
            jsobj = json.loads(r.text)
        except json.decoder.JSONDecodeError as e:
            print(e)
            return ''
        if 'references' in jsobj:
            refs_len = len(jsobj['references'])
            for i in range(refs_len):
                references.append(jsobj['references'][i]['text'] + "\n")
        return references


if __name__ == "__main__":
    crawler = RefCrawler("deep learning", 1)
    crawler.get_references()