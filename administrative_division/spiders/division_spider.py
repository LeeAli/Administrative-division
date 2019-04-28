import scrapy

from scrapy.utils.response import get_base_url
from scrapy.utils.url import urlparse
from scrapy.utils.url import urljoin_rfc
from urllib.parse import urljoin
from administrative_division.items import ProvinceItem, CommonItem, VillageItem


class ProvinceSpider(scrapy.Spider):
	name = "provinceSpider"
	allowed_domains = ["stats.gov.cn"]
	start_urls = ["http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2018/index.html"]

	def parse(self, response):
		base_url = get_base_url(response)
		province_name = response.xpath("//table/tr/td/a/text()").getall()
		link = response.xpath("//table/tr/td/a/@href").getall()
		dictionary = dict(zip(province_name, link))
		for k, v in dictionary.items():
			# url=urljoin_rfc(base_url,v)
			code = v[:2]
			relative_url = urljoin(base_url, v)
			dictionary.update({k: relative_url})
			# print('省份: {0},url: {1}'.format(k, relative_url))
			item = ProvinceItem(province_name=k, province_code=code, link=relative_url)
			yield item
		next_page = response.xpath("//table/tr/td/a/@href").getall()
		for temp_url in next_page:
			if temp_url is not None:
				yield response.follow(temp_url, callback=self.parse_other)

	def parse_other(self, response):
		base_url = get_base_url(response)
		name = response.xpath("//table/tr/td[2]/a/text()").getall()
		code = response.xpath("//table/tr/td[1]/a/text()").getall()
		link = response.xpath("//table/tr/td[1]/a/@href").getall()
		# 处理市辖区没有获取到的问题
		city_area_name = response.xpath('//table/tr').css('tr.countytr>td:nth-child(2)::text').get()
		city_url = response.url[response.url.rfind('/') + 1:response.url.rfind('.html')]
		if city_area_name == '市辖区' and len(city_url) == 4:
			area_code = response.xpath('//table/tr').css('tr.countytr>td:nth-child(1)::text').get()
			item = CommonItem(name=city_area_name, code=area_code, link=response.url)
			yield item
		for idx, val in enumerate(name):
			# print("地区名称:{0},地区编码:{1},链接:{2}".format(val, code[idx], link[idx]))
			item = CommonItem(name=val, code=code[idx], link=urljoin(base_url, link[idx]))
			yield item
		next_page = response.xpath("//table/tr/td[1]/a/@href").getall()
		for temp_url in next_page:
			if temp_url is not None and len(temp_url) < 17:
				yield response.follow(temp_url, callback=self.parse_other)
			elif temp_url is not None and len(temp_url) == 17:  # 处理村委会级别的区划代码
				yield response.follow(temp_url, callback=self.parse_village)

	def parse_village(self, response):
		code = response.css("tr.villagetr>td:nth-child(1)::text").getall()
		type_code = response.css("tr.villagetr>td:nth-child(2)::text").getall()
		name = response.css("tr.villagetr>td:nth-child(3)::text").getall()
		for idx, val in enumerate(name):
			item = VillageItem(name=val, code=code[idx], type_code=type_code[idx])
			yield item