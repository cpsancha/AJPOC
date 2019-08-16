#!/usr/bin/env python
# -*- coding: utf-8 -*-


from ajpoc.vacancies_spider import VacanciesSpider
from ajpoc.setup_logger import setup_scrapy_logger
from scrapy.crawler import CrawlerProcess


def main():
    # Configure scrapy logger
    setup_scrapy_logger()

    # Launch crawler process
    crawler_process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    crawler_process.crawl(VacanciesSpider)
    crawler_process.start()


if __name__ == "__main__":
    main()
