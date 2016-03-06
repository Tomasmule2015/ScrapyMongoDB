# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SigleuserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    UserId = scrapy.Field()
    Following = scrapy.Field()
    FollowingNum = scrapy.Field()
    Follower = scrapy.Field()
    FollowerNum = scrapy.Field()
    HisCar = scrapy.Field()
    Carport = scrapy.Field()
    Topic = scrapy.Field()
    MTopicNum = scrapy.Field()
    ETopicNum = scrapy.Field()   
    pass
