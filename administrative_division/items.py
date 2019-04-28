# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProvinceItem(scrapy.Item):
	# define the fields for your item here like:
	# name = scrapy.Field()
	# pass
	province_name = scrapy.Field()
	province_code = scrapy.Field()
	link = scrapy.Field()


class CommonItem(scrapy.Item):
	name = scrapy.Field()
	code = scrapy.Field()
	link = scrapy.Field()


class VillageItem(scrapy.Item):
	name = scrapy.Field()
	code = scrapy.Field()
	# 城乡分类代码
	type_code = scrapy.Field()
