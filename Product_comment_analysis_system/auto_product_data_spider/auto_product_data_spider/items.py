# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# The final data
class DataProductInfo(scrapy.Item):
    Product_ID = scrapy.Field()
    RootURL_ID = scrapy.Field()
    Product_Name = scrapy.Field()
    Product_Model = scrapy.Field()
    CommentNum = scrapy.Field()
    URL = scrapy.Field()
    UpdateTime = scrapy.Field()
    User = scrapy.Field()


class DataProductComment(scrapy.Item):
    Product_Comment_ID = scrapy.Field()
    product_ID = scrapy.Field()
    Product_Type_ID = scrapy.Field()
    Reviewer = scrapy.Field()
    Location = scrapy.Field()
    Comment = scrapy.Field()
    CommentMedia = scrapy.Field()
    CommentTime = scrapy.Field()
    Score = scrapy.Field()
    ScoreSource = scrapy.Field()
    upvote = scrapy.Field()
    reviews = scrapy.Field()
    UpdateTime = scrapy.Field()
    User = scrapy.Field()
