#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

import tornado.ioloop
import tornado.web
import requests
import os
import re


class MainHandler(tornado.web.RequestHandler):

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
        }
        self.url = "https://v.douyin.com/J3Qt7MJ"
        self.api_url = "https://www.iesdouyin.com/web/api/v2/aweme/iteminfo/?item_ids=%s"
        self.session = requests.session()

    def data_received(self, chunk):
        pass

    def get_video_id(self, url):
        mid = url.split('/')[5]
        print("mid ----> " + mid)
        return mid

    def get_video_info(self, mid):
        json_data = requests.get(self.api_url % mid).json()
        print('api_url ---> ' + self.api_url % mid)
        info = json_data['item_list'][0]
        video = {}
        video['pic'] = info['video']['cover']['url_list'][0]
        video['desc'] = info['desc']
        real_url = info['video']['play_addr']['url_list'][0]
        video['url'] = real_url.replace('playwm', 'play')
        print(video)
        return video


    def get(self):
        # """get请求"""
        url = self.get_argument('url')
        json = self.douyin(url)
        self.write(json)

    def douyin(self, url):
        res = self.session.get(url)
        print(res.status_code)
        print(res.url)
#	self.headers['referer'] = res.url
        video_id = self.get_video_id(res.url)
        video_info = self.get_video_info(video_id)
        return video_info

"""
def app():
    print(os.path.dirname(__file__))
    return tornado.web.Application(
        [
            (r"/dy", MainHandler)
        ],
        static_path=os.path.join(
            os.path.dirname(__file__), "html"  # 索引到html文件夹中的html    
        )
    )
"""


if __name__ == "__main__":
    application = tornado.web.Application([(r"/dy", MainHandler)], static_path=os.path.join(os.path.dirname(__file__), "html"))    
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()

