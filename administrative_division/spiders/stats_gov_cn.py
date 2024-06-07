from urllib.parse import urljoin

import scrapy

from administrative_division.items import VillageItem, CommonItem, ProvinceItem


class StatsGovCnSpider(scrapy.Spider):
    name = 'stats_gov_cn'
    allowed_domains = ['stats.gov.cn']
    start_urls = ['https://www.stats.gov.cn/sj/tjbz/tjyqhdmhcxhfdm/2023/index.html']

    def parse(self, response):
        base_url = response.url
        province_elements = response.xpath("//table[@class='provincetable']/tr[@class='provincetr']/td/a")

        for province in province_elements:
            province_name = province.xpath("text()").get()
            province_url = province.xpath("@href").get()
            full_url = urljoin(base_url, province_url)
            province_code = province_url[:2]
            province_code = province_code
            item = ProvinceItem(
                province_name=province_name,
                province_code=province_code,
                link=province_url
            )
            yield item
            # self.logger.info(f"Province URL: {full_url}")
            yield scrapy.Request(full_url, callback=self.parse_city)

    def parse_city(self, response):
        return self.parse_region(response, "//table[@class='citytable']/tr", self.parse_county)

    def parse_county(self, response):
        return self.parse_region(response, "//table[@class='countytable']/tr", self.parse_town)

    def parse_town(self, response):
        return self.parse_region(response, "//table[@class='towntable']/tr", self.parse_village)

    def parse_village(self, response):
        villages = response.xpath("//tr[@class='villagetr']")

        for village in villages:
            village_code = village.xpath("./td[1]/text()").get()
            type_code = village.xpath("./td[2]/text()").get()
            village_name = village.xpath("./td[3]/text()").get()

            item = VillageItem(
                code=village_code,
                type_code=type_code,
                name=village_name
            )
            yield item

    def parse_region(self, response, xpath_expr, next_callback):
        base_url = response.url
        elements = response.xpath(xpath_expr)[1:]
        for element in elements:
            name = element.xpath("./td[2]/a/text() | ./td[2]/text()").get()
            code = element.xpath("./td[1]/a/text() | ./td[1]/text()").get()
            url = element.xpath("./td[2]/a/@href").get()
            yield CommonItem(
                name=name,
                code=code,
                link=url
            )
            if url and next_callback:
                full_url = urljoin(base_url, url)
                yield scrapy.Request(full_url, callback=next_callback)
