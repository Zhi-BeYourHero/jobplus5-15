# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from getcompany.models import db, User
from faker import Faker
f = Faker(locale='zh-cn')

class GetcompanyPipeline(object):
    def process_item(self, item, spider):
        user = User(
                name=item['name'],
                email=f.email(),
                password=f.password()
                #company_msg.logo=item['logo']
                )

        db.session.add(user)
        return item

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        db.session.commit() 
