#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Crawler spider for the vacancies
"""
import re
import html2text
import scrapy

from scrapy.linkextractors import LinkExtractor
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
        # Url
        vacancy['url'] = response.url
        # Title
        vacancy['title'] = response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='header-job']"
            "//h2[@class='c-banner__title col-xs-12 col-sm-12']/text()").get()
        # Posting Date
        vacancy['published_date'] = response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='header-job']"
            "//div[@class='c-banner__jobinfo-ligne'][1]"
            "/span[2]/text()").get()
        # Division
        vacancy['division'] = response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='header-job']"
            "//div[@class='c-banner__jobinfo-ligne'][2]"
            "/span[2]/text()").get()
        # Location
        vacancy['location'] = str(response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='header-job']"
            "//div[@class='c-banner__jobinfo-ligne'][3]"
            "/span[2]/text()").get()).strip()
        # Reference Code
        vacancy['reference_code'] = str(response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='c-banner__jobinfo-botton-ligne']"
            "//span[text()='External code']"
            "/parent::*/span[2]/text()").get()).strip()
        # Functional Area
        vacancy['job_family'] = str(response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='c-banner__jobinfo-botton-ligne']"
            "//span[text()='Job family']"
            "/parent::*/span[2]/text()").get()).strip()
        # Contract Type
        vacancy['contract_type'] = str(response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='c-banner__jobinfo-botton-ligne']"
            "//span[text()='Contract type']"
            "/parent::*/span[2]/text()").get()).strip()
        # Work Experience
        vacancy['work_experience'] = str(response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='c-banner__jobinfo-botton-ligne']"
            "//span[text()='Experience level']"
            "/parent::*/span[2]/text()").get()).strip()
        # Working Time
        vacancy['working_time'] = str(response.xpath(
            "//div[@class='c-jobdetails']"
            "//div[@class='c-banner__jobinfo-botton-ligne']"
            "//span[text()='Working Time']"
            "/parent::*/span[2]/text()").get()).strip()
        # Description
        vacancy['description'] = html2text.html2text(response.xpath(
            "//div[@class='has-padding c-contentjob']"
            "//h2[text()='Job Description']"
            "/parent::*/div[2]").get())

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
            LinkExtractor(
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
