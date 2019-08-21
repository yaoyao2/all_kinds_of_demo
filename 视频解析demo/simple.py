import re
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from urllib.request import urlretrieve

import requests
from scrapy import Selector


class VideoDownLoader(object):
    def __init__(self, url):
        self.api = 'https://jx.618g.com'  #第三方视频解析API接口
        self.get_url = 'http://jx.618ge.com/?url=' + url   #用第三方解析接口，解析这个视频url
        print(self.get_url)
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/63.0.3239.132 Safari/537.36'}

        #多线程下载视频段
        self.thread_num = 4
        self.i = 0
        html = self.get_page(self.get_url)
        if html:
            self.parse_page(html)

    def get_page(self, get_url):
        """获取网页"""
        try:
            print('正在请求目标网页....', get_url)
            response = requests.get(get_url, headers=self.headers)
            if response.status_code == 200:
                print(response.text)
                print('请求目标网页完成....\n准备解析....')
                self.headers['referer'] = get_url
                return response.text
        except Exception:
            print('请求目标网页失败，请检查错误重试')
            return None

    def parse_page(self, html):
        """解析网页"""
        print('目标信息正在解析........')
        self.title = "清华大学2019演讲"  # 获取标题(电影名称)
        # m3u8_url = selector.xpath("//div[@id='a1']/iframe/@src").extract_first()[14:]  # 获取视频地址(m3u8)
        m3u8_url = 'http://zltest2018.oss-cn-beijing.aliyuncs.com/record/test2018/zl_001/2019-07-30-08-08-27_2019-07-30-12-16-34.m3u8'
        self.ts_list = self.get_ts(m3u8_url)  # 得到一个包含ts文件的列表
        print('解析完成，下载ts文件.........')
        self.pool()

    def get_ts(self, m3u8_url):
        """解析m3u8文件获取ts文件"""
        try:
            response = requests.get(m3u8_url, headers=self.headers)
            html = response.text
            print('获取ts文件成功，准备提取信息')
            ret_list = re.findall("(.*?ts)+", html)  # 匹配.ts的字段
            print(ret_list)
            ts_list = []
            for ret in ret_list:
                # 'http://zltest2018.oss-cn-beijing.aliyuncs.com/record/test2018/zl_001/1564456581_10766.ts'
                # 'http://zltest2018.oss-cn-beijing.aliyuncs.com/record/test2018/zl_001/1564445347_10420.ts'
                # 'http://zltest2018.oss-cn-beijing.aliyuncs.com/record/test2018/zl_001/1564445347_10420.ts'
                ts_url = m3u8_url[:-44] + ret
                ts_list.append(ts_url)
                print('**********')
                print(ts_url)
            return ts_list
        except Exception:
            print('缓存文件请求错误1，请检查错误')

    def pool(self):
        print('经计算需要下载%d个文件' % len(self.ts_list))
        if self.title not in os.listdir():
            os.mkdir(r"D:" + self.title)  # 新建视频目录
        print('正在下载...所需时间较长，请耐心等待..')
        # 开启多进程下载
        pool = pool = ThreadPoolExecutor(max_workers=16)  # 多线程下载
        pool.map(self.save_ts, self.ts_list)
        pool.shutdown()
        print('下载完成')
        self.ts_to_mp4()

    def ts_to_mp4(self):
        print('ts文件正在进行转录mp4......')
        str = 'copy /b ' + self.title+'\*.ts ' + self.title + '.mp4'  # copy /b 命令
        print(str)
        os.system(str)
        filename = self.title + '.mp4'
        if os.path.isfile(filename):
            print('转换完成，祝你观影愉快')
            shutil.rmtree(self.title)

    def save_ts(self, ts_list):
        print(self.title)
        self.i += 1
        print('当前进度%d' % self.i)
        urlretrieve(url=ts_list, filename=r"D:" + self.title + '\{}'.format(ts_list[-9:]))


if __name__ == '__main__':
    # 原始视频的url
    url = "http://live.ckcest.cn/Pcweb/pages/PC_play.html?id=723&oid=1"
    video_down_loader = VideoDownLoader(url)
