#-*- coding:utf-8 -*-

"""
破解优酷网站获取视频地址资源
下载优酷视频
"""
import requests
from bs4 import BeautifulSoup
import json
import os,shutil
import re
import base64
import time
import RunJs
import sys

import sys

# import moviepy.editor as mpy



def youku_spider(v_url,save_path):
    # video_url = raw_input(u'请输入视频地址:')
    video_url = v_url

    vid = re.findall(r'id_.*?==',video_url)[0][3:]

    print vid

    getjson_url = 'http://play-ali.youku.com/play/get.json?vid=%s&ct=12&callback=BuildVideoInfo.response' % vid

    user_agent = 'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_5 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13G36 Safari/601.1'

    header = {

        'User-Agent':user_agent,
        'Connection':'keep-alive',
        'Referer':'http://v.youku.com/v_show/id_XMTcwODg2OTQyMA==.html',
        'Cookie':'ykss=48e5d0575151fbf35e174d0e;__ysuid=1473307977492hSiiSc;',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
    }

    html = requests.get(getjson_url,headers=header)

    #
    data = html.content[24:-1]
    dict_data = json.JSONDecoder().decode(data)



    # print data
    encript_string = dict_data['data']['security']['encrypt_string']
    ip = dict_data['data']['security']['ip']

    fileid = dict_data['data']['stream'][0]['segs'][0]['fileid']
    title = dict_data['data']["show"]['title']

    # print dict_data
    # print 'encript_string:',encript_string
    # print "ip",ip
    # print 'fileid',fileid


    type_video = {
        'flv':'flv',
        '3pgphd':'3pgphd',
        'mp4':'mp4',
        'flvhd':'flvhd',
        'hd2':'hd2',
        'hd3':'hd3'
    }

    ts = int(time.time())
    # print ts

    videoid = vid

    # print videoid

    param = RunJs.runjs(videoid)
    ep = param[0]
    sid = param[1]
    token = param[2]

    parse_video_url = r'http://pl.youku.com/playlist/m3u8?vid=%s==&type=%s&ts=%s&keyframe=0&ep=%s&sid=%s&token=%s&ctype=12&ev=1&oip=%s' % (vid,type_video['mp4'],ts,ep,sid,token,ip)

    os.chdir(os.getcwd())

    videoname = (title).replace(' ','')
    print videoname

    video_dir = save_path

    if not video_dir:

        video_dir = save_path


    if os.path.exists(video_dir+'/'+videoname):
        shutil.rmtree(video_dir+'/'+videoname)
        os.mkdir(video_dir + '/' + videoname)
    else:
        os.mkdir(video_dir + '/' + videoname)


    json_video_data = requests.get(parse_video_url)



    video_downlaod_url = re.findall(r'http://.*?mp4.ts',json_video_data.content)



    #数组去重
    new_video_url = []
    for vd in video_downlaod_url:
        if str(vd) not in new_video_url:
            new_video_url.append(str(vd))
    print new_video_url

    count = 0
    videos = []

    for vurl in new_video_url:

        video_data = requests.get(vurl,stream=True)

        print video_data.headers

        video_size = int(video_data.headers['Content-Length'])/(1024*1024)


        vname = '%s.mp4' % count
        videos.append(vname)
        f = open(vname,'wb')
        print('正在下载视频:%s.mp4...' % count)
        shutil.copyfileobj(video_data.raw,f)
        count += 1
        print '下载完成!'
        f.close()

    ts_names = "concat:"

    for i in range(len(videos)):
        os.system("./ffmpeg -i %s.mp4 -vcodec copy -acodec copy -vbsf h264_mp4toannexb %s.ts" % (i,i))
        ts_names += "%s.ts|" % i

    path = video_dir + '/' + videoname + '/'


    os.system('''./ffmpeg -i "%s" -acodec copy -vcodec copy -absf aac_adtstoasc %s.mp4''' % (ts_names[:-1],videoname.encode('utf-8')))



    for i in range(len(videos)):
        shutil.move('./%s.mp4' % i, path)
        shutil.move('./%s.ts' % i, path)

    shutil.move(videoname+'.mp4',path)



