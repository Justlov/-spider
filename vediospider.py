#coding:utf-8
import csv
import json
import os
import random
import re
import time
from lxml import  etree
import requests
from bs4 import BeautifulSoup
# from retrying import retry


"""
1 .爬取代理获取代理ip验证代理IP 是否可行,作为爬取视屏使用
2. 请求目标网站获取响应,保存文件
"""





user_agent_list = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]

class Fetch_proxy():

    def __init__(self):
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'}
        self.api = 'http://www.xicidaili.com/nn/{}'



    def fetch_proxy(self,num):
        for i in range(num+1):
                api = self.api.format(i)
                respones = requests.get(url=api, headers=self.header)
                soup = BeautifulSoup(respones.text, 'lxml')
                container = soup.find_all(name='tr', attrs={'class': 'odd'})
                for tag in container:
                    try:
                        con_soup = BeautifulSoup(str(tag), 'lxml')
                        td_list = con_soup.find_all('td')
                        ip = str(td_list[1])[4:-5]
                        port = str(td_list[2])[4:-5]
                        IPport = ip + '\t' + port + '\n'
                        with open('ip.text','a+') as f:
                            f.write(IPport)
                    except Exception as e:
                        print('No IP！')
                time.sleep(1)



    # 检验代理IP是否有效 将有效的代理IP写入文件 备用
    def Check_proxy(self):
        fp = open('ip.text')
        ips = fp.readlines()
        proxys =list()
        url = 'https://www.baidu.com'
        for p in ips:
            ip = p.strip('\n').split('\t')
            proxy = 'http:\\' + ip[0] + ':' + ip[1]
            proxies = {'proxy': proxy}
            proxys.append(proxies)
        for N,pro in enumerate(proxys):
            try:
                s = requests.get(url, proxies=pro)
                # print('第{}个ip：{} 状态{}'.format(N,pro,s.status_code))
                print(s.status_code)
                if s.status_code == 200:
                    pro = pro.get('proxy')
                    lastpro = pro + '\n'
                    print(lastpro,222)
                    with open('b.txt','a+') as f:
                        f.write(lastpro)
                else:
                    print('无效代理')
            except Exception as e:
                print(e)



    # 生成代理池备用
    def proxypool(self):
        fp = open('b.txt', 'r')
        proxys = list()
        ips = fp.readlines()
        for p in ips:
            proxies = {'proxy': p.strip('\n')}
            proxys.append(proxies)

        return proxys







class Vedio():

    """
    1. 获取html
    2.解析html 获取数据源地址
    3.请求数据源地址
    4.保存文件
    """
    def __init__(self):
        self.headers = {'Origin': 'http://www.222tv.co/',
           'Referer': 'http://www.222tv.co/video/2545/%E3%81%B6%E3%81%A3%E3%81%8B%E3%81%91%E7%86%9F%E5%A5%B3-vol-5-%E3%83%91%E3%83%BC%E3%83%882-031715-046',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36',
            'Host':'www.222tv.co'
          }



    # 请求目标网站获取响应
    def get_html(self,url):
        try:
            response = requests.get(url, headers = self.headers)
            if response.status_code == 200:
                response.encoding = 'utf-8'
                return response.text
            return None
        except Exception as e:
            print(e)
            return None

    # 解析html  获取影片名和 对应的url地址
    def parserhtml(self,htmlstr):
        selector = etree.HTML(htmlstr)
        vedioname = selector.xpath('//*[@id="wrapper"]/div[1]/div[2]/div[1]/div/div/div/a/span//text()')
        # print(vedioname)
        vedioname2 = selector.xpath('//*[@id="wrapper"]/div[1]/div[4]/div/div/div/div/a/span//text()')
        # print(vedioname2,len(vedioname2))
        vedioname.extend(vedioname2)
        vediourl = re.findall('<div class="well well-sm"> <a href="(.*?)"> <div class="thumb-overlay">', htmlstr)
        realurllist = []
        for i in vediourl:
            realurl = 'http://www.222tv.co' + i
            realurllist.append(realurl)
        d = dict(zip(vedioname, realurllist))
        return d

    def parseurls(self,name,url):
        # 对url请求获取资源链接
        source = self.get_html(url)

        # 资源包地址
        mu8url = re.findall('<source src="(.*?)" type=', str(source))
        # mu8url = source2.xpath('//*[@id="video_html5_api"]/source//text()')
        print(mu8url, 77777)
        print(666)
        mu8url = 'http:' + mu8url[0]
        print(mu8url)

        # 对资源包地址发出请求 获取响应文本
        response = requests.get(mu8url)
        print(response.text)
        with open(r'C:\Users\huangqi\Desktop\spider\spider_smooc-master\vediotxt\{}.txt'.format(name), 'wb') as f:
            f.write((str(response.text) + url).encode('utf-8'))


    # 请求资源

    def get_contrnt_url(self):
        file = r'C:\Users\huangqi\Desktop\spider\spider_smooc-master\vediotxt'
        list = os.listdir(file)
        contentdict = {}
        for v,i in enumerate(list):
            filename = i.split('.txt')[0]
            path = os.path.join(file,i)
            tslist = []
            if i.endswith('.txt'):
                with open(path, 'r',encoding='utf-8') as f:
                    b = f.readlines()
                    url = b[-1]

                    # print(b)
                    for i in b:
                        # print(type(i))
                        # print(i)
                        if i.endswith('.ts\n'):
                            if i.startswith('https'):
                                continue
                            tslist.append(i)

                            # print(i.split('.txt')[0])
                    tslist.append(url)

                    contentdict[filename] = tslist
        return contentdict


    # 保存数据
    def save_to(self,contentdict, property):

        ua = random.choice(user_agent_list)

        for name, tslist in contentdict.items():
            refer = str(tslist[-1]).strip()
            rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
            name = re.sub(rstr, "_", name)
            headers = {'Origin': 'http://www.222tv.co/',
                       'Referer': refer,
                       'User-Agent': ua
                       }
            for index, i in enumerate(tslist):
                print("正在解析{}".format(i))
                print('传入的{}'.format(refer))
                try:
                    respones = requests.get(i, headers=headers, proxies=random.choice(property), timeout=5)
                    if respones.status_code == 200:
                        # respones = requests.get(i, headers=headers, proxies=random.choice(property))
                        time.sleep(3)
                        content = respones.content
                        if os.path.exists(r'C:\Users\huangqi\Desktop\spider\spider_smooc-master\vedio\{}'.format(name)):
                            print("已经存在此文件夹")
                        else:
                            os.makedirs(r'C:\Users\huangqi\Desktop\spider\spider_smooc-master\vedio\{}'.format(name))

                        with open(r'C:\Users\huangqi\Desktop\spider\spider_smooc-master\vedio\{}\{}.ts'.format(name,index), "wb") as f:
                            f.write(content)
                except Exception as e:
                    print(e)




def run():
    fetch_proxy = Fetch_proxy()
    fetch_proxy.fetch_proxy(2)
    fetch_proxy.Check_proxy()
    proxypool = fetch_proxy.proxypool()
    #
    url = 'http://www.222tv.co/'
    vedio = Vedio()
    htmlstr = vedio.get_html(url)
    vedict = vedio.parserhtml(htmlstr)
    for name, url in vedict.items():
        vedio.parseurls(name,url)
        contentdict = vedio.get_contrnt_url()
        vedio.save_to(contentdict,proxypool)







if __name__ == '__main__':
    run()
