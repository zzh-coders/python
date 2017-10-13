import urllib

import requests
import time
from bs4 import BeautifulSoup
import os
import threading
from requests import exceptions


class MeiTu():
    def __init__(self):
        self.dir_path = "D:\mzitu\meitu"
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

    def all_url(self, url):
        html = self.request(url)  ##调用request函数把套图地址传进去会返回给我们一个response
        if html is None:
            return False
        obj = BeautifulSoup(html.text, 'lxml')
        if obj is None:
            return
        all_a = obj.find('div', class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            print(u'开始保存：', title)  ##加点提示不然太枯燥了
            path = str(title).replace("?", '_')  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            href = a['href']
            self.html(path, href)

    def for_request(self, listA):
        for info in listA:
            self.img(info[0], info[1])

    def html(self, path, href):  ##这个函数是处理套图地址获得图片的页面地址
        html = self.request(href)
        if html is None:
            return False
        self.headers['referer'] = href
        obj = BeautifulSoup(html.text, 'lxml')
        if obj is None:
            return
        max_span = obj.find('div', class_='pagenavi').find_all('span')[-2].get_text()
        listAvalue = []
        self.mkdir(path)
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            listAvalue.append([path, page_url])

        thread = threading.Thread(target=self.for_request, args=(listAvalue,))
        thread.start()

    def img(self, path, page_url):  ##这个函数处理图片页面地址获得图片的实际地址
        img_html = self.request(page_url)
        if img_html is None:
            return False
        obj = BeautifulSoup(img_html.text, 'lxml')
        if obj is None:
            return
        img_url = obj.find('div', class_='main-image').find('img')['src']
        self.save(path, img_url)

    def save(self, path, img_url):  ##这个函数保存图片
        name = img_url[-9:-4]
        img = self.request(img_url)
        if img is None:
            return False
        if os.path.exists(self.dir_path + '/' + path + '/' + name + '.jpg'):
            return True
        f = open(self.dir_path + '/' + path + '/' + name + '.jpg', 'ab')
        f.write(img.content)
        f.close()

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join(self.dir_path, path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join(self.dir_path, path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def request(self, url, count=0):  ##这个函数获取网页的response 然后返回
        time.sleep(0.5)
        try:
            r = requests.get(url, headers=self.headers, timeout=3)
            return r
        except exceptions.Timeout as e:
            print('请求超时')
            count += 1
            if count < 3:
                return self.request(url, count)
            return None
        except exceptions.HTTPError as e:
            print('http请求错误:' + e.errno)
            return None
        except exceptions.ConnectionError as e:
            print(e.strerror)
            return None
        except exceptions.ReadTimeout as e:
            print(e.strerror)
            return None


start = time.time()
meitu = MeiTu()  ##实例化
meitu.all_url('http://www.mzitu.com/all')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
print(u'执行时间:', time.time() - start)
