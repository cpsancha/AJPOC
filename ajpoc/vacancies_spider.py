#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ajpoc.setup_logger import setup_module_logger, setup_scrapy_logger
from re import search, sub
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

# Define module logger
logger = setup_module_logger(__name__)


class VacanciesSpider(CrawlSpider):
    name = 'vacancies'
    allowed_domains = ['airbus.com']
    start_urls = ['https://www.airbus.com/careers/search-and-apply/search-for-vacancies.html/?page=1']
    rules = (
        Rule(LinkExtractor(allow=(),
                           restrict_css=('a.c-pagination--item.link.c-jobsearchpage_searchlink.current',),
                           tags=('a',),
                           attrs=('href',),
                           process_value=lambda this_page: VacanciesSpider.parse_next_page(this_page)
                           ),
             callback="parse_vacancies_links",
             follow=True),)

    def parse_start_url(self, response: Response):
        return self.parse_vacancies_links(response)

    @staticmethod
    def parse_next_page(this_page: str):
        this_page_number = int(search('(?<=(\\?page\\=))(\\d+)', this_page).group())
        next_page = sub('(?<=(\\?page\\=))(\\d+)', str(this_page_number + 1), this_page)
        return next_page

    @staticmethod
    def parse_vacancies_links(response: Response):
        logger.info('Processing listing page: ' + response.url)
        # vacancies_links = response.css(
        #     '.thumbnail-info-wrapper > .display-block > a.title::attr(href)').extract()
        # for vacancy_link in vacancies_links:
        #     vacancy_link = response.urljoin(playlist_link)
        #     yield Request(vacancy_link, callback=self.parse_vacancies_contents)
        pass

    @staticmethod
    def parse_vacancies_contents(response: Response):
        playlist_name = response.css("#watchPlaylist::text")[-1].extract()
        logger.info('Processing vacancy: ' + playlist_name + ' --> ' + response.url)
        pass
