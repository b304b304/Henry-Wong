# -*- encoding=utf-8 -*-
import sys
from scrapy.cmdline import execute

help_message = """
-b crawl BitAuto
-p crawl PCAuto
"""
version = "win 1.0"

def launch(argv):
    if argv == '-h':
        print(help_message)
    elif argv == '--version':
        print(version)
    elif argv == '-b':
        # Crawl BitAuto
        execute(['scrapy', 'crawl', "BitAuto"])
    elif argv == '-p':
        # Crawl PCAuto
        execute(['scrapy', 'crawl', "PCAuto"])


if __name__ == "__main__":
    launch(sys.argv[1])
