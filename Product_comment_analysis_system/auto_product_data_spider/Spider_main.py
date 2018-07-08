# -*- encoding=utf-8 -*-

from scrapy.cmdline import execute

if __name__ == "__main__":
    # Debug
    # spider_name = 'AutoSpider'
    execute(['scrapy', 'crawl', "AutoHome"])
    # Download ProductInfo bitauto
    # execute("scrapy crawl BitAuto -o ProductInfoBitAuto.csv".split())
    # Download ProductInfo pcauto
    # execute("scrapy crawl AutoSpider -o ProductInfoPCAuto.csv".split())
    # Download ProductComment bitauto
    # execute("scrapy crawl BitAuto -o ProductCommentBitAuto.csv".split())
    # Download ProductComment pcauto
    # execute("scrapy crawl AutoSpider -o ProductCommentPCAuto.csv".split())
    pass
