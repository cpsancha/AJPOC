#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main module
"""
import scrapy.crawler
import ajpoc.vacancies_spider
import ajpoc.setup_logger


def main():
    """
    This function configures the logger, initializes the database and runs the
    crawler spider.
    """
    # Configure scrapy logger
    ajpoc.setup_logger.setup_scrapy_logger()

    # Launch crawler process
    crawler_process = scrapy.crawler.CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
    })
    crawler_process.crawl(ajpoc.vacancies_spider.VacanciesSpider)
    crawler_process.start()


if __name__ == "__main__":
    main()
