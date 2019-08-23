#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crawler spider for the vacancies
"""
import re
import scrapy
from ajpoc import logger_setup, vacancy_item


class VacanciesSpider(scrapy.spiders.CrawlSpider):
    """
    This class defines a crawler spider for the contents of the Airbus
    Job portal vacancies
    """
    # Define module logger
    logger = logger_setup.setup_module_logger(__name__)

    # Spider properties
    name = 'vacancies'
    allowed_domains = ['airbus.com']
    start_urls = ['https://www.airbus.com/careers/search-and-apply/'
                  'search-for-vacancies.html/?page=1']

    # Scraped data
    scraped_data = []

    @staticmethod
    def get_next_listing_page(this_page: str) -> str:
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

    def parse_vacancies_links(self, response: scrapy.http.Response) -> \
            scrapy.http.Request:
        """
        This method gets the links of the vacancies listed in the response,
        requests its own response and calls the ´´parse_vacancy_contents´´
        method for each of them to parse its data.
        :param response: Scraped response of the listing page
        :return: Request of parsing the contents of each listed vacancy
        """
        # self.logger.info('Processing listing page: %s', response.url)
        for href in response.xpath(
                "//section[@class='c-jobsearchpage__content']"
                "//div[@class='c-jobcarousel__slider--title']"
                "//a/@href").getall():
            yield scrapy.Request(response.urljoin(href),
                                 self.parse_vacancies_contents)

    def parse_vacancies_contents(self, response: scrapy.http.Response) -> None:
        """
        This method parses the contents of the vacancy from the scraped web
        page and stores them in the fields of an Scrapy Item.
        :param response:
        :return:
        """
        # Parse vacancy fields
        vacancy = vacancy_item.Vacancy()
        vacancy['title'] = response.xpath(
            "//div[@class='c-jobdetails']"
            "//h2[@class='c-banner__title col-sm-12']/text()").get()
        vacancy['url'] = response.url
        self.logger.info('Processing vacancy: %s --> %s',
                         vacancy.get('title'), vacancy.get('url'))
        self.scraped_data.append(vacancy)

    def parse_start_url(self, response: scrapy.http.Response):
        """
        This dummy function is requested for not to skipping the indexing of
        the initial listing page.
        :param response:
        :return:
        """
        return self.parse_vacancies_links(response)

    def closed(self, reason: str) -> None:
        """
        This method is called on spider closing and prints the parsed vacancies
        for debugging purposes. It will be removed in the future.
        :param reason: The reason of the spider closing
        :return:
        """
        print("Spider will close, reason: {}".format(reason))
        print("The scraped data is as follows:")
        print(self.scraped_data)

    rules = (
        scrapy.spiders.Rule(
            scrapy.linkextractors.LinkExtractor(
                allow=(),
                restrict_css=('a.c-pagination--item.link.'
                              'c-jobsearchpage_searchlink.current', ),
                tags=('a', ),
                attrs=('href', ),
                process_value=get_next_listing_page.__func__),
            callback="parse_vacancies_links",
            follow=True
        ),
    )
