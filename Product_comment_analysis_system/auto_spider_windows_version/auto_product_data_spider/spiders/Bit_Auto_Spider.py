# -*- coding: utf-8 -*-
from __future__ import division

import re
import time
import scrapy
import urllib.request
from scrapy.http import Request

from sql import *
from auto_product_data_spider import settings
from auto_product_data_spider.items import CommentNumber
from auto_product_data_spider.items import DataProductComment


class BitAutoSpider(scrapy.Spider):
    # Declare the connect and cursor of the spider
    con = ''
    cur = ''

    # The flag of continuous redundant number
    redundant_counter = 0

    name = "BitAuto"
    start_urls = settings.ROOT_URLS
    comment_num = dict()
    user = "wdh"

    def start_requests(self):
        # Initialize the connect and cursor
        self.con, self.cur = connect_database()

        for url in self.start_urls:
            # Start the spider
            yield Request(url[0], callback=self.parse, meta={"rootURL_Id": url[1]})

        # Yield the number of comments
        yield CommentNumber(
            nums=self.comment_num
        )
        # Close the connection by the spider
        self.con.commit()
        self.cur.close()
        self.con.close()

    def parse(self, response):
        html = response.text
        selected_urls = re.findall('class="name"><a target="_blank" href=".+?">[\w\W]+?</a></li>', html)
        counter = 0
        urls = []
        product_names = []
        for selected_url in selected_urls:
            if selected_url in urls:
                continue
            else:
                counter += 1
            if counter > 10:
                break
            urls.append(selected_url)
        for i in range(len(urls)):
            product_names.append(re.sub("<[\w\W]+?>", '', re.findall('">([\w\W]*?)</a>', urls[i])[0]))
            urls[i] = "http://car.bitauto.com" + re.findall('href="(.+?)"', urls[i])[0] + "koubei/"
        product_models = product_names
        # The comment_num will be update after the end of the spider
        comment_num = 0

        for pack in map(list, zip(urls, product_names, product_models)):
            if self.redundant_counter >= 3:
                continue

            url, product_name, product_model = pack[0], pack[1], pack[2]

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
                    time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                    product_name
                ))
                self.cur.execute(update_product_info.format(
                    'User', self.user, product_name
                ))
            self.con.commit()
            product_id = query(self.cur, query_product_id.format(product_name))

            yield Request(url, callback=self.get_more_ks, meta={"product_id": product_id})

    def get_more_ks(self, response):
        html = response.text
        try:
            more_url = re.findall('hidden" value="(.+?)"', html)[0]
            more_url = re.sub("--1-", "--{}-", more_url)
        except Exception as e:
            print(e)
            more_url = ''
        try:
            page = urllib.request.urlopen(more_url.format('1')).read().decode("utf-8")
            page_n = re.findall('<a href="http://.+?">(\d+?)</a>', page)[-1]
        except Exception as e:
            with open("e_url.txt", "a+") as f:
                f.write(more_url.format('1'))
            print(e)
            page_n = 0
        for i in range(1, int(page_n)):
            try:
                Request(more_url.format(str(i)), callback=self.get_more_k)
            except Exception as e:
                with open("e_url.txt", "a+") as f:
                    f.write(more_url.format(str(i)))
                print(e)
                break
            yield Request(
                more_url.format(str(i)),
                callback=self.get_more_k,
                meta={"product_id": response.meta["product_id"]}
            )

    def get_more_k(self, response):
        html = response.text
        k_urls = re.findall('href="(.+?)" rel="nofollow" target="_blank" class="more', html)
        for k_url in k_urls:
            yield Request(k_url, callback=self.get_k, meta=response.meta)

    def get_k(self, response):
        html = response.text
        reviewer = re.findall('user-head"[\w\W]+?<p>([\w\W]+?)</p>', html)[0]
        reviewer = re.sub("<.+?>", '', reviewer)
        reviewer = re.sub("\s", '', reviewer)
        try:
            location = re.findall('"addredd">购车地址：<em>([\w\W]+?)</em>', html)[0]
        except Exception as e:
            print(e)
            location = ''
        location = re.sub("&nbsp;", '', location)
        if len(re.findall('wkb-details', html)) > 0:
            comments = re.findall('<!--微口碑内容 开始-->([\w\W]+?)<!--微口碑内容 结束-->', html)[0]
            comment_media = len(re.findall('<img src=', comments))
            comments = re.findall('details-cont wkb-details ">([\w\W]+?)</p>', comments)
            f_comment = []
            for comment in comments:
                comment = re.sub("<[\w\W]+?>", '', comment)
                comment = re.sub("&nbsp;", '', comment)
                comment = re.sub('\s', '', comment)
                f_comment.append(comment)
            score = int(re.findall('start0-box[\w\W]*?style="width: (\d+?)%;"></em>', html)[0]) / 20
            score_source = []
        else:
            comments = re.findall('<!--完整口碑内容 开始-->([\w\W]+?)<!--完整口碑内容 结束-->', html)[0]
            comment_media = len(re.findall('<img class=', comments))
            comments = re.findall('item-box div_ImgLoadArea">([\w\W]+?)</p>', comments)
            f_comment = []
            score_source = []
            score_source_n = []
            for comment in comments:
                comment = re.sub("&nbsp;", '', comment)
                try:
                    head = re.findall('head">([\w\W]+?)：', comment)[0]
                    head = re.sub('\s', '', head)
                    score_n = re.findall('style="([\w\W]+?)"', comment)[0]
                    score_n = int(re.findall('\d+', score_n)[0]) / 20
                    score_source.append(head)
                    score_source.append(score_n)
                    score_source_n.append(score_n)
                except Exception as e:
                    print(e)
                comment = re.sub("<[\w\W]+?>", '', comment)
                comment = re.sub("&nbsp;", '', comment)
                comment = re.sub('\s', '', comment)
                f_comment.append(comment)
            if len(score_source_n) > 0:
                score = score_source_n[-1]
            else:
                score = 0
        comment_time = re.findall("发布时间：([\w\W]+?)<", html)[0]
        comment_time = re.sub('\s', '', comment_time)
        up_vote = re.findall('<span id="spSupportCount">(\d+?)</span>', html)
        reviews = re.findall("评论数：(\d+?)<", html)[0]

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
        else:
            # Fill the item and yield it
            product_id = response.meta["product_id"]
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
            if product_id in self.comment_num.keys():
                self.comment_num[product_id] += 1
            else:
                self.comment_num[product_id] = 0
            yield item
