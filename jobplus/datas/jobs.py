# -*- coding: utf-8 -*-
import scrapy
import json
class JobsSpider(scrapy.Spider):
    name = 'jobs'
    
    @property
    def start_urls(self):
        with open('companymsg.json') as f:
            data=json.load(f)
        url_tmp = [data[i]['website'] for i in range(len(data))]
        return url_tmp


    def parse(self, response):
        for job in response.css('div.sojob-item-main'):
            yield {
                    'name': job.css('div.job-info h3 a::text').extract_first().strip(),
                    'salary': job.css('div.job-info p span.text-warning::text').extract_first(),
                    'address': job.css('div.job-info p a::text').extract_first(),
                    'experience_requirement': job.xpath('.//div[@class="job-info"]/p/span[3]/text()').extract_first(),
                    'degree_requirement': job.css('div.job-info p span.edu::text').extract_first(),

                    'company': job.xpath('//div[contains(@class,"company-info")]/p[@class="company-name"]/a/text()').extract_first(),
                    'tags': job.xpath('//div[contains(@class,"company-info")]/p[@class="field-financing"]/span/a/text()').extract_first()#.split('/')
                    }
