# -*- coding: utf-8 -*-
import scrapy

class CompanySpider(scrapy.Spider):
    name = 'company'

    start_urls = ["https://www.liepin.com/zhaopin/?key=python&d_sfrom=search_industry"]

    def parse(self, response):
        for company in response.css('dl.comp-list-box dd ul li'):
            yield {
                    'name': company.css('a span::text').extract_first(),
                    'logo': company.css('a img::attr(src)').extract_first(),
                    'website': response.urljoin(company.css('a::attr(href)').extract_first())
                    }
    
