# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ProvinceItem(scrapy.Item):
    province_code = scrapy.Field()
    province_name = scrapy.Field()
    short_name = scrapy.Field()
    link = scrapy.Field()


class CommonItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    link = scrapy.Field()


class VillageItem(scrapy.Item):
    code = scrapy.Field()
    name = scrapy.Field()
    type_code = scrapy.Field()
