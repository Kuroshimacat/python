#!/usr/bin/python3

import os
import re
import urllib
import json
import socket
import urllib.request
import urllib.parse
import urllib.error
import time
import _thread

timeout = 20
socket.setdefaulttimeout(timeout)

def SaveImage(url='https://original.img.cheerfun.dev/img-original/img/2019/03/05/03/09/55/73518990_p0.png',path='test.png'):
    rq = urllib.request.Request(url)
    rq.add_header('accept','image/webp,image/apng,image/*,*/*;q=0.8')
    rq.add_header('accept-encoding','gzip, deflate, br')
    rq.add_header('accept-languag','zh-CN,zh;q=0.9,en;q=0.8,pl;q=0.7')
    rq.add_header('sec-fetch-dest','image')
    rq.add_header('sec-fetch-mode','no-cors')
    rq.add_header('sec-fetch-site','cross-site')
    rq.add_header('referer','https://pixivic.com/popSearch')
    rq.add_header('user-agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36')
    rp = urllib.request.urlopen(rq)
    #print(rp.getcode())
    s=rp.read()
    #print(len(s))
    f=open(path,'wb')
    f.write(s)
    f.close()

class Crawler:
    __time_sleep = 0.1
    __amount = 0
    __start_amount = 0
    __counter = 0
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'}

    def __init__(self, t=0.1, word='白上吹雪 '):
        self.time_sleep = t
        if not os.path.exists("./" + word):
            os.mkdir("./" + word)
        self.__counter = len(os.listdir('./' + word)) + 1

    def get_suffix(self, name):
        m = re.search(r'\.[^\.]*$', name)
        if m.group(0) and len(m.group(0)) <= 5:
            return m.group(0)
        else:
            return '.jpeg'

    def save_image(self, rsp_data, word):
        
        for image_info in rsp_data['imageUrls']:
            try:
                pps=image_info['original'].replace('https://i.pximg.net/','https://original.img.cheerfun.dev/')
                print(pps)
                suffix = self.get_suffix(pps)
                # 保存图片
                _thread.start_new_thread(SaveImage,(pps,'./' + word + '/' + str(self.__counter) + str(suffix)))
            except urllib.error.HTTPError as urllib_err:
                print(urllib_err)
                continue
            except Exception as err:
                time.sleep(1)
                print(err)
                print("产生未知错误，放弃保存")
                continue
            else:
                sum=len(os.listdir('./' + word))
                print(f'第{str(self.__counter)}张图片正在保存,已有{str(sum)}张图片')
                self.__counter += 1
                time.sleep(self.time_sleep)
        return

    def get_images(self, word='白上吹雪'):
        search = urllib.parse.quote(word)
        pn = self.__start_amount
        while pn <= self.__amount:
            url='https://api.pixivic.com/illustrations?keyword='+search+'&page='+str(pn)
            print(url)
            try:
                req = urllib.request.Request(url=url, headers=self.headers)
                page = urllib.request.urlopen(req)
                rsp = page.read().decode('utf-8')
            except UnicodeDecodeError as e:
                print(e)
                print('-----UnicodeDecodeErrorurl:', url)
            except urllib.error.URLError as e:
                print(e)
                print("-----urlErrorurl:", url)
            except socket.timeout as e:
                print(e)
                print("-----socket timout:", url)
            else:
                rsp_data = json.loads(rsp)
                tmp=rsp_data['data']
                for ele in tmp:
                    self.save_image(ele, word)
                print("下载下一页")
                pn += 1
            finally:
                page.close()
        print("下载任务结束")
        return

    def start(self, word, spider_page_num=1, start_page=1):
        self.__start_amount = start_page
        self.__amount = spider_page_num
        self.get_images(word)


if __name__ == '__main__':
    word=input('你想要谁的图片?请输入:')
    crawler = Crawler(1.3,word)
    crawler.start(word, 10, 1)
