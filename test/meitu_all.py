import requests
import time
from bs4 import BeautifulSoup
import os


class MeiTu():
    def __init__(self):
        self.max_num_sleep = 1000
        self.current_num = 0
        self.dir = "D:\mzitu\meitu_all"
        self.headers = {'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}

    def all_page(self, type_path, url):
        html = self.request(url)  ##调用request函数把套图地址传进去会返回给我们一个response
        max_page = BeautifulSoup(html.text, 'lxml').find('div', class_='nav-links').find_all('a', class_='page-numbers')[-2].get_text()
        for page in range(1, int(max_page) + 1):
            page_url = href + 'page/' + str(page)
            self.all_url(type_path, page_url)

    def all_url(self, type_path, url):
        html = self.request(url)  ##调用request函数把套图地址传进去会返回给我们一个response
        if html is None:
            return False
        all_li = BeautifulSoup(html.text, 'lxml').find('div', class_='postlist').find_all('li')
        for li in all_li:
            a = li.find('a')
            title = a.find('img')['alt']
            print(u'开始保存：', title)  ##加点提示不然太枯燥了
            path = str(title).replace("?", '_')  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
            self.mkdir(os.path.join(type_path, path))  ##调用mkdir函数创建文件夹！这儿path代表的是标题title哦！！！！！不要糊涂了哦！
            href = a['href']
            self.html(type_path, path, href)  ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！

    def html(self, type_path, path, href):  ##这个函数是处理套图地址获得图片的页面地址
        html = self.request(href)
        if html is None:
            return False
        self.headers['referer'] = href
        max_span = BeautifulSoup(html.text, 'lxml').find('div', class_='pagenavi').find_all('span')[-2].get_text()
        for page in range(1, int(max_span) + 1):
            page_url = href + '/' + str(page)
            self.current_num += 1
            self.img(type_path, path, page_url)  ##调用img函数

    def img(self, type_path, path, page_url):  ##这个函数处理图片页面地址获得图片的实际地址
        if self.current_num > self.max_num_sleep:
            self.current_num = 0
            time.sleep(10)
        img_html = self.request(page_url)
        if img_html is None:
            return False
        img_url = BeautifulSoup(img_html.text, 'lxml').find('div', class_='main-image').find('img')['src']
        self.save(type_path, path, img_url)

    def save(self, type_path, path, img_url):  ##这个函数保存图片
        name = img_url[-9:-4]
        file_name = os.path.join(self.dir, type_path, path, name + '.jpg')
        if os.path.isfile(file_name):
            print(u'文件已经存在', name + '.jpg')
            return True
        img = self.request(img_url)
        if img is None:
            return False
        f = open(file_name, 'ab')
        f.write(img.content)
        f.close()
        print(u'文件已经保存成功', file_name)

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(os.path.join(self.dir, path))
        if not isExists:
            print(u'建了一个名字叫做', path, u'的文件夹！')
            os.makedirs(os.path.join(self.dir, path))
            return True
        else:
            print(u'名字叫做', path, u'的文件夹已经存在了！')
            return False

    def request(self, url):  ##这个函数获取网页的response 然后返回
        try:
            r = requests.get(url, headers=self.headers, timeout=3)
            return r
        except (requests.ConnectionError, IndexError, UnicodeEncodeError, TimeoutError, requests.ReadTimeout) as e:
            print(e.args)
            return None
        except requests.HTTPError as f:
            print('The server couldn\'t fulfill the request.')
            return None
        except requests.RequestException as e:
            print(e.args)
            return None


start = time.time()
meitu = MeiTu()  ##实例化
url = "http://www.mzitu.com/"
html = meitu.request(url)
if html is None:
    print('网站没有图片')
all_li = BeautifulSoup(html.text, 'lxml').find('ul', class_='menu').find_all('li')
for li in all_li:
    a = li.find('a')
    title = a.get_text()
    if title == "每日更新":
        continue
    path = str(title).replace("?", '_')  ##我注意到有个标题带有 ？  这个符号Windows系统是不能创建文件夹的所以要替换掉
    href = a['href']
    meitu.all_page(path, href)  ##调用html函数把href参数传递过去！href是啥还记的吧？ 就是套图的地址哦！！不要迷糊了哦！
    time.sleep(10)

print(u'执行时间:', time.time() - start)


# meitu.all_url('http://www.mzitu.com/all')  ##给函数all_url传入参数  你可以当作启动爬虫（就是入口）
# print(u'执行时间:', time.time() - start)
