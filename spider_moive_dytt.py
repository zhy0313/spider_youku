# -*- coding: UTF-8 -*-
import urllib,urllib2,time,os,threading
from bs4 import BeautifulSoup

import sys,re,shutil
from Sava_Sql import save_Sql
from Moview_ui import Window

#获取电影天堂高分电影
class SpiderMovie(object):
    def __init__(self,need_film_num):
        self.page_count = 1
        self.movie_count = set()
        self.movie_url = []
        self.movie_name = []
        self.num = 1
        self.need_film_num = int(need_film_num)
        self.failed_count = 1
        self.title_sign =set()
        self.Img = []
        self.movie_thunder = []
        self.file_size = set()
        self.threads = []
    def craw_url(self):
        root_url = 'http://www.ygdy8.net/html/gndy/dyzz/'

#         while True:
#             url = root_url+'list_23_%s.html' % (self.page_count) 
#            
#             self.page_count+=1
# #             time.sleep(1)          
# #             print url
# #             try:
#             self.craw_movie(url)
#             # except:
#             #     print "craw failed:%s" % self.failed_count
#             #     self.failed_count+=1
#             #     if self.failed_count>5:
#             #         break
#             if len(self.movie_name) >= self.need_film_num:
#                 break
#             if self.title_sign ==u'阳光电影--您的访问出错了!-电影天堂迅雷电影下载！':
#                 break
#         self.movie_count = len(self.movie_name)     
        #多线程下载
        for i in range(self.need_film_num+1):
            url = root_url+'list_23_%s.html' % (self.page_count)
            self.page_count+=1
            self.threads.append(threading.Thread(target=self.craw_movie,args=(url,))) 
        for t in self.threads:
            # t.setDaemon(True)
            t.start()
#         for t in self.threads:
        t.join()   
        self.movie_count = len(self.movie_name)       
        print 'All finished!'
    def craw_movie(self,url):
         # 伪装浏览器访问
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
        referer = 'http://www.ygdy8.net/html/gndy/dyzz/'
        headers = { 
                   'User-Agent':user_agent,
                    'Referer':referer
#                     'Accept-encoding':'gzip'
        }
        request = urllib2.Request(url,headers=headers)
        try:
            response = urllib2.urlopen(request,timeout=10)
        except urllib2.URLError,e:
            print e.reason
        html = response.read()
        #编码问题     
        soup= BeautifulSoup(html.decode('gb2312','ignore'))
        
        # print soup.original_encoding
        
        self.title_sign = soup.title.text
#         print self.title_sign
        for link in soup.find_all('a',class_="ulink"):        
#             patter = re.compile(ur'\d{4}(.*?)(\d分|高分)(.*?)BD')
            if re.findall(ur'\d{4}(.*?)(?:\d分|高分)(.*?)(BD|HD)',link.text) and link.text is not None:
                if len(self.movie_name)<self.need_film_num:
                    self.movie_name.append(link.text)
                    self.movie_url.append('http://www.ygdy8.net/'+link['href'])
                    getdir = os.getcwd()
                    pic_dir = getdir + r'/movies/%s' % self.movie_name[-1]
                    print '\n%d.'%(self.num)+link.text+':'+'http://www.ygdy8.net/'+link['href']
                    if not os.path.exists(pic_dir):
                        os.makedirs(pic_dir)
                    else:
                        # dir = getdir+r'\movies'
                        # self.deleteDri(dir)
                        shutil.rmtree(pic_dir)
                        os.makedirs(pic_dir)
                    try:
                        self.craw_contents(self.movie_url[-1],pic_dir)
                    except: 
                        pass
                    
                    self.num+=1
                    
    def add_dict(self):
        dict_movies = {}
        for i in range(len(self.movie_name)):
            dict_movies.setdefault(self.movie_name[i],self.movie_url[i])
        return dict_movies
    
    def craw_contents(self,url_content,dir):
        c = 1
        # 伪装浏览器访问
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:45.0) Gecko/20100101 Firefox/45.0'
        referer = 'http://www.ygdy8.net/html/gndy/dyzz/'
        headers = { 
                   'User-Agent':user_agent,
                    'Referer':referer,
#                     'Accept-Encoding':'gzip,deflate'
                    'Accept':'image/png,image/*;q=0.8,*/*;q=0.5'
                    
        }
        request1 = urllib2.Request(url_content,headers=headers)
        try:
            response1 = urllib2.urlopen(request1,timeout=10)
        except urllib2.URLError,e:
            print e.reason
            
        html_content = response1.read()
        
        soup_content = BeautifulSoup(html_content.decode('gb2312','ignore'))
#
        for pic in soup_content.find_all('img'):
#             self.Img.append(re.findall(r'^http.*[?:jpg|gif|png]',pic['src']))  
            src_Imges = set()
            
            for src_img in re.findall(r'^http.*[?:jpg|gif|png]',pic['src']):
                src_Imges = src_img
#                 print src_Imges

            if len(src_Imges)>=1: 
                local_path = dir+'/%d.jpg' % c    
                print '下载:',src_Imges 
#                 try:              
                time.sleep(0.5)
                try:
                    urllib2.urlopen(urllib2.Request(src_Imges,headers=headers),timeout=10)
                    urllib.urlretrieve(src_Imges,filename=local_path,reporthook=self.report) 
                    print '已下载:%-2.2fKB' %  (self.file_size/1024)
                except urllib2.URLError,e:
                    code_url = e.code
                    print e.code
#                 if len(code_url)==200:
                    
#                 except :
#                     print '下载图片异常！'
                c += 1 
#            

    def report(self,count,blockSize , totalSize):

        if totalSize > blockSize:
            avg = '%d%%\r' % int(100.0 * count * blockSize / totalSize)
            sys.stdout.write(avg)  
            sys.stdout.flush()
            self.file_size = count*blockSize
            
        else:
#             sys.stdout.write('100%')
            downloaded = '%-2.2fKB\r' % (count*blockSize/1024)
            self.file_size = count*blockSize
            sys.stdout.write('已下载:'+downloaded)
            sys.stdout.flush()
            

if __name__ == "__main__":
    
    spider = SpiderMovie(30)
    spider.craw_url()
    save_sql = save_Sql(spider.add_dict())
    save_sql.add_Sql()
    app = Window() 
    app.root.mainloop()
