# -*- coding: utf-8 -*-

# Scrapy settings for auto_product_data_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'auto_product_data_spider'

SPIDER_MODULES = ['auto_product_data_spider.spiders']
NEWSPIDER_MODULE = 'auto_product_data_spider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'auto_product_data_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'auto_product_data_spider.middlewares.AutoProductDataSpiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'auto_product_data_spider.middlewares.AutoProductDataSpiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'auto_product_data_spider.pipelines.AutoProductDataSpiderPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
HTTPCACHE_ENABLED = True
HTTPCACHE_EXPIRATION_SECS = 0
HTTPCACHE_DIR = 'httpcache'
HTTPCACHE_IGNORE_HTTP_CODES = []
HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# My settings
# START_URLS = [
#     "https://car.autohome.com.cn/price/brand-36.html#pvareaid=3311273",
#     "https://car.autohome.com.cn/price/brand-15.html",
#     "https://car.autohome.com.cn/price/brand-33.html",
#     "http://price.pcauto.com.cn/price/nb20/?ad=5657",
#     "http://price.pcauto.com.cn/price/nb4/?ad=5657",
#     "http://price.pcauto.com.cn/price/nb1/?ad=5657",
#     "http://car.bitauto.com/mercedesbenz/",
#
# ]


ROOT_URLS = [
    ["https://car.autohome.com.cn/price/brand-36.html#pvareaid=3311273", 34],
    # ["https://car.autohome.com.cn/price/brand-15.html", 35],
    # ["https://car.autohome.com.cn/price/brand-33.html", 36],
    # ["http://price.pcauto.com.cn/price/nb20/?ad=5657", 37],
    # ["http://price.pcauto.com.cn/price/nb4/?ad=5657", 38],
    # ["http://price.pcauto.com.cn/price/nb1/?ad=5657", 39],
    # ["http://car.bitauto.com/mercedesbenz/", 40],
    # ["http://car.bitauto.com/bmw/", 41],
    # ["http://car.bitauto.com/audi/", 42]
]

AUTO_HOME_HEADERS = {
    "user-agent": "MQQBrowser/26 Mozilla/5.0 (linux; U; Android 2.3.7; zh-cn; MB200 Build/GRJ22; CyanogenMod-7) "
                  "AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1"
}
