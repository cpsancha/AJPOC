#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Vacancy scrapy item
"""

import scrapy


class Vacancy(scrapy.Item):  # pylint: disable=too-many-ancestors
    """
    Vacancy scrapy item
    """
    contract_type = scrapy.Field()
    description = scrapy.Field()
    division = scrapy.Field()
    functional_area = scrapy.Field()
    interest_group = scrapy.Field()
    location = scrapy.Field()
    published_date = scrapy.Field()
    reference_code = scrapy.Field()
    required_skills = scrapy.Field()
    tasks_and_responsibilities = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    work_experience = scrapy.Field()
    working_time = scrapy.Field()
