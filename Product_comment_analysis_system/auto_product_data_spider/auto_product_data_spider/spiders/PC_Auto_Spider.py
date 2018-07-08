# -*- coding: utf-8 -*-
from __future__ import division

import re
import time
import scrapy
import urllib.request
from scrapy.http import Request

from Product_comment_analysis_system.auto_product_data_spider.auto_product_data_spider import settings
from Product_comment_analysis_system.auto_product_data_spider.auto_product_data_spider.items import DataProductComment


class PCAutoSpider(scrapy.Spider):

    name = "AutoSpider"
    cls = 1
    start_urls = settings.ROOT_URLS
    product_id = 30
    product_comment_id = 4619
    user = "wdh"

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url[0], callback=self.parse, meta={"rootURL_Id": url[1]})

    def parse(self, response):
        html = response.text
        urls = re.findall('href="(/comment/[^/]+?/)"', html)
        product_names = re.findall('<p class="tit"><a href="/.+?/" title="([\w\W]+?)"', html)
        if len(urls) > 10:
            urls = urls[0:10]
            product_names = product_names[0: 10]
        product_models = product_names
        for pack in map(list, zip(urls, product_names, product_models)):
            url, product_name, product_model = pack[0], pack[1], pack[2]
            url = "http://price.pcauto.com.cn" + url
            page = urllib.request.urlopen(url).read().decode("gbk")
            if len(re.findall("main_nav_page\">[\w\W]*?<span>1/(\d+?)</span", page)) > 0:
                max_page = int(re.findall("main_nav_page\">[\w\W]*?<span>1/(\d+?)</span", page)[0]) + 1
            else:
                max_page = 1
            comment_num = max_page * 10
            yield Request(url, callback=self.get_k)
            for i in range(2, max_page):
                yield Request(
                    url + 'p' + str(i) + ".html",
                    callback=self.get_k
                )
            self.product_id += 1
            # yield DataProductInfo(
            #     Product_ID=self.product_id,
            #     RootURL_ID=response.meta["rootURL_Id"],
            #     Product_Name=product_name,
            #     Product_Model=product_model,
            #     CommentNum=comment_num,
            #     UpdateTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
            #     User=self.user
            # )

    def get_k(self, response):
        self.cls = 1
        html = response.text
        comment_classes = re.findall('<div class="litDy clearfix">([\w\W]+?)</table>', html)
        for comment_class in comment_classes:
            reviewer = re.findall("<a href=\"//my.pcauto.com.cn/\d+?/\" target=\"_blank\">([^<>]+?)</a>", comment_class)
            location = re.findall('<em>购买地点</em>([\w\W]*?)</div>', comment_class)
            comments = re.findall('class="dianPing[\w\W]+?>([\w\W]+?)<div class="desline', comment_class)
            f_comment = []
            for comment in comments:
                comment = re.sub("<[\w\W]+?>", '', comment)
                comment = re.sub('\s', '', comment)
                f_comment.append(comment)
            comment_media = len(re.findall(
                '<a href="//price\.pcauto\.com\.cn/.+?\.html" title="" target="_blank">',
                comment_class
            ))
            comment_time = re.findall('html" target="_blank">(.+?) 发表</a>', comment_class)
            score = re.findall("'score' : '(.+?)'", comment_class)
            score_source = re.findall('<ul>([\w\W]+?)</ul>', comment_class)[0]
            score_source = re.findall('span>([\w\W]+?)</span>[\w\W]*?<div class="penFenxx" datas="([\w\W]+?)"', score_source)
            up_vote = re.findall('<em id="#vote_1_871790">\((\d+?)\)</em>', comment_class)
            reviews = 0
            self.product_comment_id += 1
            item = DataProductComment(
                Product_Comment_ID=self.product_comment_id,
                product_ID=self.product_id,
                Reviewer=reviewer,
                Location=location,
                Comment=f_comment,
                CommentMedia=comment_media,
                CommentTime=comment_time,
                Score=score,
                ScoreSource=score_source,
                upvote=up_vote,
                reviews=reviews,
                UpdateTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                User=self.user
            )
            yield item
