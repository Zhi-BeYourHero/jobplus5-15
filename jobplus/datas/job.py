# -*- coding: utf-8 -*-
import scrapy


class JobSpider(scrapy.Spider):
    name = 'job'
    start_urls = ['http://https://www.liepin.com/zhaopin/?key=python&d_sfrom=search_industry/']

    def parse(self, response):
        yield {
                
                
                }
