# -*- coding: utf-8 -*-
from sql import *
from auto_product_data_spider.items import CommentNumber
from auto_product_data_spider.items import DataProductInfo
from auto_product_data_spider.items import DataProductComment

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AutoPipeline(object):
    def __int__(self):
        self.con, self.cur = connect_database()

    def process_item(self, item, spider):
        if spider.name == "PCAuto":
            self.cur.execute(insert_into_Comment.format(
                item["product_ID"],
                item["Product_Type_ID"],
                item["Reviewer"],
                item["Location"],
                item["Comment"],
                item["CommentMedia"],
                item["CommentTime"],
                item["Score"],
                item["ScoreSource"],
                item["upvote"],
                item["reviews"],
                item["UpdateTime"],
                item["User"],
            ))
            self.con.commit()

        elif spider.name == "BitAuto":
            if isinstance(item, DataProductComment):
                self.cur.execute(insert_into_Comment.format(
                    item["product_ID"],
                    item["Product_Type_ID"],
                    item["Reviewer"],
                    item["Location"],
                    item["Comment"],
                    item["CommentMedia"],
                    item["CommentTime"],
                    item["Score"],
                    item["ScoreSource"],
                    item["upvote"],
                    item["reviews"],
                    item["UpdateTime"],
                    item["User"],
                ))
            elif isinstance(item, CommentNumber):
                for number in CommentNumber["nums"].items():
                    self.cur.execute(update_product_info2.format(
                        "CommentNum",
                        number[1],    # comment number
                        number[0],    # product ID
                    ))

            self.con.commit()

        else:
            return item
