from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import re

def getPage():
    try:
        url = 'http://www.66news.org/forum-48-1.html'
        # 构建请求的request
        request = Request(url)
        # 利用urlopen获取页面代码
        response = urlopen(request)
        # 将页面转化为UTF-8编码
        pageCode = response.read().decode('GBK')
        return pageCode
    except HTTPError as e:
        print('The server couldn\'t fulfill the request.')
        print('Error code: ', e.code)
        return None
    except URLError as e:
        print('We failed to reach a server.')
        print('Reason: ', e.reason)
        return None


pageCode = getPage()
# print(pageCode)

pattern = re.compile('<a.*?href="(.*?)".*?onclick="atarget(this)".*?class="z">',re.S)
items = re.findall(pattern,pageCode)
print(items)
# 用来存储每页的段子们
# pageStories = []
# 遍历正则表达式匹配的信息
# for item in items:
   # print(item)
        # item[0]是一个段子的发布者，item[1]是内容，item[2]是发布时间,item[4]是点赞数
        # pageStories.append([item[0].strip(), text.strip(), item[2].strip(), item[4].strip()])
# return pageStories