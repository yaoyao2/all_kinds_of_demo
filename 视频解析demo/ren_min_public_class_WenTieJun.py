import requests
from scrapy import Selector


class VideoDownLoader(object):
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/63.0.3239.132 Safari/537.36'}

        #多线程下载视频段
        self.get_mp4()

    def get_mp4(self):

        print("开始下载")
        url = 'https://pic.ibaotu.com/00/51/34/88a888piCbRB.mp4'
        url = 'http://vipmp4i.vodfile.m1905.com/201908212027/03f0333268869e7a1cf9893553c755b9/logo/rzdfcy.mp4'
        url = 'https://leicloud.ulearning.cn/resources/939286/201706131914386807.mp4'
        r = requests.get(url, stream=True)

        with open('test.mp4', "wb") as mp4:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    mp4.write(chunk)

        print("下载结束")

if __name__ == '__main__':
    # 原始视频的url----是.mp4视频，很好下载
    video_down_loader = VideoDownLoader()
