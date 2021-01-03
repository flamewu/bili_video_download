from download import *
from setting import *

# 需要下载的视频网址
url = 'https://www.bilibili.com/bangumi/play/ss34421'
# 需要下载的视频p数列表(番剧则为集数)
part = range(0,1)
# 下载路径
path = 'file\\'

# 运行此文件即可下载
if __name__ == "__main__":
    vl = VideoList(url,part)
    for i in vl.download():
        dl = Download(i)
        dl.download(path,type = type,codecs = codecs,byte = byte)