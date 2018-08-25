# -*- coding: utf-8 -*-

# This problem is waiting tobe solved
# The anti-spider is too difficult for me...

from __future__ import division

import re
import time
import scrapy
import urllib.request
from scrapy.http import Request

from auto_product_data_spider import settings
from auto_product_data_spider.items import DataProductInfo
from auto_product_data_spider.items import DataProductComment


class AutoHomeSpider(scrapy.Spider):

    name = "AutoHome"
    cls = 1
    start_urls = settings.ROOT_URLS

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url[0], callback=self.parse)

    def parse(self, response):
        self.cls = 1
        html = response.text
        urls = re.findall('href="(//k.autohome.com.cn/\d+?/#pvareaid=\d+?)"', html)
        if len(urls) > 10:
            urls = urls[0:10]
        for url in urls:
            url = "https:" + url
            yield Request(
                url,
                callback=self.get_k_url
            )
            break

    def get_k_url(self, response):
        self.cls = 1
        html = response.text
        k_urls = re.findall(
            "href=\"//(k.autohome.com.cn/detail/view_[\w\W]+?)\?[\w\W]+?\"",
            html
        )
        for url in k_urls:
            url = "https://" + url
            yield Request(
                url,
                callback=self.get_k
            )
            break

    def get_k(self, response):
        self.cls = 1
        html = response.text
        print(html)