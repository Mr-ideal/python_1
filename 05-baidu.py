import requests
from lxml import etree

class Tieba(object):

    def __init__(self, name):
        self.url = 'https://tieba.baidu.com/f?ie=utf-8&kw={}'.format(name)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            # 'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.01; Windows NT 5.0)'
        }

    def get_data(self, url):
        response = requests.get(url, headers=self.headers)
        with open('temp.txt', 'wb')as f:
            f.write(response.content)
        return response.content

    def parse_data(self, data):
        data = data.decode().replace("<!--", "").replace("-->", "")
        # 创建element对象
        html = etree.HTML(data)
        el_list = html.xpath('//li[@class=" j_thread_list clearfix"]/div/div[2]/div[1]/div[1]/a ')
        # print(len(el_list))

        data_list = []

        for el in el_list:
            temp = {}

            temp['title'] = el.xpath('./text()')[0]
            temp['link'] = 'http://tieba.baidu.com' + el.xpath('./@href')[0]
            data_list.append(temp)
        # 获取下一页
        try:
            next_url = 'https:' + html.xpath('//a[contains(text(),"下一页>")]/@href')[0]
        except:
            next_url = None

        return data_list, next_url

    def save_data(self, data_list):
        for data in data_list:
            print(data)

    def run(self):
        # url
        # headers
        next_url = self.url
        while True:
            # 发送请求，获取相应
            data = self.get_data(next_url)
            # 从响应中提取数据（数据和翻页用的url）
            data_list, next_url = self.parse_data(data)

            self.save_data(data_list)
            print(next_url)
            # 判断是否终结
            if next_url ==None:
                break

if __name__ == '__main__':
    tieba = Tieba('传智播客')
    tieba.run()