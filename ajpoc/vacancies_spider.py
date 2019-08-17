#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crawler spider for the vacancies
"""
import re
from scrapy.http import Response
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ajpoc.setup_logger import setup_module_logger

# Define module logger
LOGGER = setup_module_logger(__name__)


class VacanciesSpider(CrawlSpider):
    """
    This class defines a crawler spider for the contents of the Airbus
    Job portal vacancies
    """

    name = 'vacancies'
    allowed_domains = ['airbus.com']
    start_urls = ['https://www.airbus.com/careers/search-and-apply/'
                  'search-for-vacancies.html/?page=1']

    @staticmethod
    def parse_next_listing_page(this_page: str) -> str:
        """
        This static method generates the link for the next vacancies listing
        page.
        :param this_page: String with the url of the current page
        :return: String with the url of the next page to index
        """
        this_page_number = int(
            re.search('(?<=(\\?page\\=))(\\d+)', this_page).group())
        next_page = re.sub('(?<=(\\?page\\=))(\\d+)',
                           str(this_page_number + 1), this_page)
        return next_page

    @staticmethod
    def parse_vacancies_links(response: Response):
        """
        TODO
        :param response:
        :return:
        """
        LOGGER.info('Processing listing page: %s', response.url)
        # vacancies_links = response.css(
        #     '.thumbnail-info-wrapper > .display-block > a.title::attr(href)').extract()
        # for vacancy_link in vacancies_links:
        #     vacancy_link = response.urljoin(playlist_link)
        #     yield Request(vacancy_link, callback=self.parse_vacancies_contents)

    @staticmethod
    def parse_vacancies_contents(response: Response):
        """
        TODO
        :param response:
        :return:
        """
        playlist_name = response.css("#watchPlaylist::text")[-1].extract()
        LOGGER.info(
            'Processing vacancy: %s --> %s', playlist_name, response.url)

    def parse_start_url(self, response: Response):
        """
        This dummy function is requested for not to skipping the indexing of
        the initial listing page.
        :param response:
        :return:
        """
        return self.parse_vacancies_links(response)

    rules = (
        Rule(LinkExtractor(allow=(),
                           restrict_css=(
                               'a.c-pagination--item.link.'
                               'c-jobsearchpage_searchlink.current',),
                           tags=('a',),
                           attrs=('href',),
                           process_value=parse_next_listing_page.__get__(
                               parse_next_listing_page.__class__,
                               parse_next_listing_page.__class__)
                           ),
             callback="parse_vacancies_links",
             follow=True),)
