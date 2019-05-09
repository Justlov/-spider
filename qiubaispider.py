# coding = utf-8
import json

import requests
from lxml import etree


class QiuBai():
    def __init__(self):
        self.headers ={
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            "Referer" : "https://www.qiushibaike.com/text/"
        }
        pass

    def get_url_list(self):
        urllist = ["https://www.qiushibaike.com/text/page/{}" .format(i)for i in range(1,14)]
        return urllist

    def get_html_str(self,url):
            response = requests.get(url,headers = self.headers)
            return response.content.decode()



    def parser_html(self,html_str):
        html_etree = etree.HTML(html_str)
        # print(html_etree)
        div_list = html_etree.xpath('//div[@id="content-left"]/div')
        # print(div_content)
        # 爬取用户名, 文本,
        valuedict = {}
        content_list = []
        for div in div_list:
            valuedict = {}
            name = div.xpath('./div//h2/text()')[0].strip() if div.xpath('./div//h2/text()') else None

            content = div.xpath('.//div[@class="content"]/span//text()')
            content = [i.strip() for i in content]
            valuedict["author"] = name
            valuedict["content"] = content
            content_list.append(valuedict)
        return content_list



    def saveto (self,content):
        with open("糗百.txt",'a',encoding="utf-8") as f:
            for content in content:
                f.write(json.dumps(content,ensure_ascii = False,indent =2))
                f.write('\n')
        print('保存成功')



    def run(self):
        # 1 获取url列表
        urllist = self.get_url_list()

        # 请求url 获取响应html_str
        for url in urllist:
            html_str = self.get_html_str(url)
            # 解析html_str

            content_list = self.parser_html(html_str)
            self.saveto(content_list)



        # 保存解析结果

if __name__ == '__main__':
    qiubai = QiuBai()
    qiubai.run()