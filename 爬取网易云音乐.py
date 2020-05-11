import requests
import json
import re
import os

class GetMusic():
    def  __init__(self):
        self.n = str(input('【网易云音乐搜索下载】输入名称:'))
        self.name = str(self.n.encode())[2:-1].replace('\\x','%').upper()
        if self.n == 'q':
            quit()
        self.url = 'https://music.sounm.com/'
        self.jumpHeaders = {
            'Host':'music.163.com',
            'User-Agent':'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
        }

    def Post(self,page=1):
        self.headers = {
            'Host': 'music.sounm.com',
            'accept':'application/json, text/javascript, */*; q=0.01',
            'origin':'https//music.sounm.com',
            'referer':'https//music.sounm.com/?name=%s&type=netease' % self.name,
            'user-agent':'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
            'X-Requested-With': 'XMLHttpRequest',
        }
        data = {
                    'input':self.n,
                    'filter':'name',
                    'type':'netease',
                    'page':page
        }
        response = requests.post(url=self.url,headers=self.headers,data=data)
        self.html = json.loads(response.text)
        return self.html

    def GetMusic_url(self):
        url_html = self.html['data']
        for i in range(len(url_html)):
            ID = 'ID:%s' % str(i+1)
            self.t = url_html[i]['title']
            title = 'Title:%s'% self.t
            author = 'Author:%s' % url_html[i]['author']
            print(ID.ljust(5),author.ljust(15),title)

        Id = int(input('输入你下要在的歌曲ID：')) - 1
        url = self.html['data'][Id]['url']
        response1 = requests.get(url=url, headers=self.jumpHeaders, allow_redirects=False)
        mp3_url = response1.headers['Location']
        mp3_headers = {
            'Host': re.findall('://(.*?)/', mp3_url)[0],
            'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
        }
        response2 = requests.get(url=mp3_url, headers=mp3_headers)
        self.content = response2.content

    def SaveMusic(self):
        self.file = '%s\\%s.mp3' % (os.path.abspath(os.path.dirname(__file__)),self.t)
        with open(self.file,'wb') as f:
            f.write(self.content)
        print('下载完成至:%s' % self.file)
        print('')

if __name__ == '__main__':
    while True:
        m = GetMusic()
        m.Post()
        m.GetMusic_url()
        m.SaveMusic()


