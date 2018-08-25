# -*- coding: utf-8 -*-
from __future__ import division

import re
import time
import scrapy
import urllib.request
from scrapy.http import Request

from sql import *
from auto_product_data_spider import settings
from auto_product_data_spider.items import DataProductComment


class PCAutoSpider(scrapy.Spider):
    # Declare the connect and cursor of the spider
    con = ''
    cur = ''

    # The flag of continuous redundant number
    redundant_counter = 0

    name = "PCAuto"
    cls = 1
    start_urls = settings.ROOT_URLS
    user = "wdh"

    def start_requests(self):
        # Initialize the connect and cursor
        self.con, self.cur = connect_database()

        # Start the spider
        for url in self.start_urls:
            yield Request(url[0], callback=self.parse, meta={"rootURL_Id": url[1]})

        # Close the connection by the spider
        self.con.commit()
        self.cur.close()
        self.con.close()

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

            # pit -> product in the table
            # If product is in the table, update it.Else add into the table.
            # Get the product_id from table
            pit = query(self.cur, if_product_in_table.format(product_name))[0] == 1
            if not pit:
                self.cur.execute(insert_into_Info.format(
                    response.meta["rootURL_Id"],
                    product_name,
                    product_model,
                    comment_num,
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    self.user
                ))
            else:
                self.cur.execute(update_product_info.format(
                    'CommentNum', comment_num, product_name
                ))
                self.cur.execute(update_product_info.format(
                    'UpdateTime',
                    time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),
                    product_name
                ))
                self.cur.execute(update_product_info.format(
                    'User', self.user, product_name
                ))
            self.con.commit()
            product_id = query(self.cur, query_product_id.format(product_name))

            yield Request(url, callback=self.get_k, meta={"product_id": product_id})
            for i in range(2, max_page):
                yield Request(
                    url + 'p' + str(i) + ".html",
                    callback=self.get_k,
                    meta={"product_id": product_id}
                )

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

            # cit -> comment in the table
            # Judge if the comment is redundant by content, reviewer,
            # comment time and location
            cit = query(self.cur, if_comment_in_table.format(
                f_comment,
                reviewer,
                comment_time,
                location
            ))[0] == 1
            if cit:
                self.redundant_counter += 1
                if self.redundant_counter >= 3:
                    break
            else:
                # Fill the item and yield it
                item = DataProductComment(
                    product_ID=response.meta["product_id"],
                    Product_Type_ID=4,
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
