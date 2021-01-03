import json
import requests
from setting import *
from fake_useragent import UserAgent
import re

url1='https://api.bilibili.com/pgc/player/web/playurl?fnval=80&cid={c}'
url2='https://api.bilibili.com/x/player/playurl?fnval=80&avid={a}&cid={c}'

class VideoList:

    headers={
        'User-Agent': '',
        'referer': '',
        'cookie': cookie
    }

    def __init__(self,url,part=[0]):
        self.url=url
        self.part=part
        
    def download(self):
        self.headers['User-Agent'] = str(UserAgent().random)
        try:
            self.html = requests.get(self.url,self.headers).text
        except Exception:
            print('链接失败')
            return None

        if re.findall(r'\.bilibili\.com/video/BV',self.url) != [] or re.findall(r'\.bilibili\.com/video/av',self.url) != []:
            return self.video()
        elif re.findall(r'\.bilibili\.com/bangumi/play/',self.url) != []:
            return self.bangumi()
        else:
            print('url无效')
            return None

    def bangumi(self):
        json_ = json.loads('{'+re.search(r'"epList":\[.+?\]',self.html).group()+'}')
        self.headers['referer']=self.url

        for i in self.part:
            try:
                cid = json_['epList'][i]['cid']
            except Exception:
                print('分p不存在')
                break
            self.headers['User-Agent'] = str(UserAgent().random)
            js = json.loads(requests.get(url1.format(c=cid),headers=self.headers).text)
            js['referer'] = self.url
            js['part'] = i
            yield js

    def video(self):
        json_ = json.loads('{'+re.search(r'"aid":\d+',self.html).group()+'}')
        aid = json_['aid']
        json_ = json.loads('{'+re.search(r'"pages":\[.+?\]',self.html).group()+'}')
        self.headers['referer']=self.url

        for i in self.part:
            try:
                cid = json_['pages'][i]['cid']
            except Exception:
                print('分p不存在')
                break
            self.headers['User-Agent'] = str(UserAgent().random)
            js = json.loads(requests.get(url2.format(a=aid,c=cid),headers=self.headers).text)
            js['referer'] = self.url
            js['part'] = i
            yield js
        

class Download:

    headers={
        'User-Agent': '',
        'referer': '',
        'cookie': cookie
    }

    def __init__(self,js):
        self.js=js

    def download(self,path,type = 0,codecs = 0,byte = None):
        self.headers['User-Agent'] = str(UserAgent().random)
        self.headers['referer'] = self.js['referer']
        p = str(self.js['part'])

        if 'data' in self.js:
            self.js=self.js['data']
        else:
            self.js=self.js['result']

        id = self.js['dash']['video'][0]['id']
        if type == 1:
            id = 80
        elif type == 2:
            id = 64
        elif type == 3:
            id = 32
        elif type == 4:
            id = 16
        elif type == 5:
            id = 112
        elif type != 0:
            print('type参数错误')
            return None
        code = 'avc'
        if codecs == 1:
            code = 'hev'
        elif codecs != 0:
            print('codecs参数错误')
            return None

        js_movie = None
        for i in self.js['dash']['video']:
            if i['id'] == id and re.findall(code,i['codecs']) != []:
                js_movie = i
                break
        js_audio = self.js['dash']['audio'][0]
        if js_movie == None:
            print('指定元素相关视频不存在')
            return None

        if byte!=None:
            self.headers['range'] = 'bytes='+byte

        vid = self.headers['referer'].split('/')[-1]
        with open(path+vid+'_'+p+'.mp4','wb+') as file1, open(path+vid+'_'+p+'.mp3','wb+') as file2:
            print('下载中','网址:'+vid+'   '+'分p:'+p)
            file1.write(requests.get(js_movie['base_url'],headers=self.headers).content)
            file2.write(requests.get(js_audio['base_url'],headers=self.headers).content)
            print('下载成功')



if __name__ == "__main__":
    vl = VideoList('https://www.bilibili.com/video/BV1K5411n7Vn')
    for i in vl.download():
        dl = Download(i)
        dl.download('1.mp4',byte='0-999')