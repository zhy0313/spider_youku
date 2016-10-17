# -*- coding:utf-8 -*-
import urllib2,json
from bs4 import BeautifulSoup
import time,threading,xlwt
from xlwt.Workbook import Workbook
import Queue
from multiprocessing.pool import Pool,Process
import multiprocessing


# queue = Queue.Queue()#存放网址的队列

out_queue = Queue.Queue()#存放网址页面的队列
queueLock = threading.Lock()
dealdata_count = 0
exitFlag = 0

#创建自己的线程类
class MyThread(threading.Thread):
    def __init__(self,target,args,out_queue):
        threading.Thread.__init__(self)
        self.setDaemon(True)

        self.target = target
        self.args = args
        self.out_queue = out_queue

    def run(self):

            self.out_queue.put(self.target(self.args))
            self.out_queue.task_done()

class ThreadData(threading.Thread):
    def __init__(self,target,args):
        threading.Thread.__init__(self)
        self.setDaemon(True)
        self.target = target
        self.args = args

    def run(self):

        self.target(self.args)


class MusicStyle(object):

    def __init__(self):

        manager = multiprocessing.Manager()
        self.style_url = []

        self.style = {}

        self.style = manager.dict()

        self.threads = []
        self.count = manager.Value('tmp',0)

        self.topic_content = 0
        self.root_url = [
            "https://www.youtube.com/channel/UC-9-kyTW8ZkZNDHQJ6FgpwQ/channels?view=49&shelf_id=17886269310742802550",
            "https://www.youtube.com/browse_ajax?action_continuation=1&continuation=4qmFsgJOEhhVQy05LWt5VFc4WmtaTkRIUUo2Rmdwd1EaMkVnaGphR0Z1Ym1Wc2N5QXhPQUZnQVdvQWNQYmdydjdDNWJLYy1BRjZBVEs0QVFBJTNE",
            "https://www.youtube.com/browse_ajax?action_continuation=1&continuation=4qmFsgJOEhhVQy05LWt5VFc4WmtaTkRIUUo2Rmdwd1EaMkVnaGphR0Z1Ym1Wc2N5QXhPQUZnQVdvQWNQYmdydjdDNWJLYy1BRjZBVE80QVFBJTNE",
            "https://www.youtube.com/browse_ajax?action_continuation=1&continuation=4qmFsgJOEhhVQy05LWt5VFc4WmtaTkRIUUo2Rmdwd1EaMkVnaGphR0Z1Ym1Wc2N5QXhPQUZnQVdvQWNQYmdydjdDNWJLYy1BRjZBVFM0QVFBJTNE",
        ]
        self.workbook = Workbook()
        self.worksheet = self.workbook.add_sheet(u'MusicStyle_ID')


    def spider(self,url):

        # 伪装浏览器访问
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
        #         referer = 'http://secure.verycd.com/signin/*/http://www.verycd.com/account/profile/base/'
        headers = {
            'User-Agent': user_agent,
            #                    'Referer':referer
        }

        try:
            request = urllib2.Request(url, headers=headers)
            response = urllib2.urlopen(request, timeout=200)

        except (urllib2.HTTPError,urllib2.URLError),e:
            print e.reason

        html = response.read()
        return html

    def dealdata(self,html_content,lock):

        topic_content = BeautifulSoup(html_content)
        try:
            for t in topic_content.find_all(class_='branded-page-module-title'):

                if ('Top Tracks' in str(t.a.text).strip()) or ('Popular Videos' in str(t.a.text).strip()):
                    id = t.a.get('href')[15:]
                    text = str(self.count.value) + '.' +str(t.a.text).strip()

                    lock.acquire()

                    self.count.value += 1
                    key = (t.a.text).strip()
                    self.style[key] = id
                    print '\n',self.count.value,'.',time.ctime(time.time()),'#',key, ':',id,
                    lock.release()
                    break
                else:
                    continue

        except Exception ,e:

            print '异常!:',e,
            pass



    def GetData(self):

        for i in range(len(self.root_url)):

            if(i==0):

                soup = BeautifulSoup(self.spider(self.root_url[i]))

                for i in soup.find_all(class_='channels-content-item yt-shelf-grid-item'):

                    topic_url = 'https://www.youtube.com' + i.a.get('href')
                    self.style_url.append(topic_url)

                    # 将网址都存放到queue队列中
                mythread = []
                for url in self.style_url:
                    print(url)
                    mythread.append(MyThread(self.spider,url,out_queue))
                for thread in mythread:
                    thread.start()

                for t in mythread:
                    t.join()

                storage = []
                while True:
                    if out_queue.qsize()>=len(self.style_url):
                        break

                while not out_queue.empty():
                    storage.append(out_queue.get())

                # p = multiprocessing.Pool(processes=4)


                lock = multiprocessing.Lock()

                processes = []

                for msg in storage:
                    # p.apply_async(self.dealdata, args=(msg,lock,))
                    t = Process(target=self.dealdata,args=(msg,lock,))
                    t.daemon = True
                    processes.append(t)

                for i in range(len(processes)):
                    processes[i].start()
                for i in range(len(processes)):
                    processes[i].join()


            else:

                    del self.style_url[:]
                    del processes[:]
                    d = json.JSONDecoder().decode(self.spider(self.root_url[i]))

                    soup = BeautifulSoup(d['content_html'])

                    for i in soup.find_all(class_='channels-content-item yt-shelf-grid-item'):
                        topic_url = 'https://www.youtube.com' + i.a.get('href')
                        self.style_url.append(topic_url)

                        # 将网址都存放到queue队列中
                    mythread = []
                    for url in self.style_url:
                        print(url)
                        mythread.append(MyThread(self.spider, url, out_queue))
                    for thread in mythread:
                        thread.start()

                    for t in mythread:
                        t.join()

                    storage = []
                    while True:
                        if out_queue.qsize() >= len(self.style_url):
                            break

                    while not out_queue.empty():
                        storage.append(out_queue.get())

                    # p = multiprocessing.Pool(processes=4)

                    lock = multiprocessing.Lock()

                    processes = []

                    for msg in storage:
                        # p.apply_async(self.dealdata, args=(msg,lock,))
                        t = Process(target=self.dealdata, args=(msg, lock,))
                        t.daemon = True
                        processes.append(t)

                    for i in range(len(processes)):
                        processes[i].start()
                    for i in range(len(processes)):
                        processes[i].join()


        #写入excel

        tall_style = xlwt.easyxf('font:height 480;')

        c = 0
        for key,value in self.style.items():
            # k = key.split('-')[1]
            self.worksheet.write(c, 0, key,self.fontStyle())
            self.worksheet.col(0).width = 256*60
            self.worksheet.write(c, 1, value,self.fontStyle())
            self.worksheet.col(1).width = 256 * 60

            self.worksheet.row(c).set_style(tall_style)
            c = c + 1
        self.workbook.save(u'/Users/holysor/Desktop/MusicStyle_ID.xls')
        print('完成!')

    # 设置表格的字体和单元格样式
    def fontStyle(self, link=None):
        # 初始化表格样式
        style = xlwt.XFStyle()
        # 字体样式
        font = xlwt.Font()
        font.name = 'Times New Roman'
        font.bold = False
        font.height = 300
        font.wigth = 300
        if link == True:
            font.underline = font.UNDERLINE_SINGLE
            font.colour_index = 4

        # 单元格内文字对齐方式
        cell_alignment = xlwt.Alignment()
        #         cell_style.horz = cell_style.HORZ_CENTER
        cell_alignment.vert = cell_alignment.VERT_CENTER
        # 单元格边框大小及宽高设定
        cell_border = xlwt.Borders()
        cell_border.top = 1
        cell_border.right = 1
        cell_border.left = 1
        cell_border.bottom = 1
        #         cell_border.diag = cell_border.THIN
        #         cell_border.bottom_colour = 0x3A


        style.alignment = cell_alignment
        style.borders = cell_border
        style.font = font
        return style

if __name__ == "__main__":
    starttime = time.ctime(time.time())
    ms = MusicStyle()
    ms.GetData()
    print '启动时间:', starttime
    print '结束时间:', time.ctime(time.time())
