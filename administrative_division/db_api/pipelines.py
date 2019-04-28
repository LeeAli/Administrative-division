import pymysql
from administrative_division.items import ProvinceItem, CommonItem, VillageItem
from administrative_division.db_api.districts import DistrictUtils
import json


class AdministrativeDivisionPipeline(object):
	'''
	MYSQL_HOSTS='localhost'
	MYSQL_PORT=3306
	MYSQL_USER='knight'
	MYSQL_PASSWORD='123456'
	MYSQL_DB=''
	'''

	def __init__(self, mysql_host, mysql_port, mysql_user, my_password, mysql_db):
		self.mysql_host = mysql_host
		self.mysql_port = mysql_port
		self.mysql_user = mysql_user
		self.mysql_password = my_password
		self.mysql_db = mysql_db
		self.charset = 'utf8'

	def process_item(self, item, spider):
		if isinstance(item, ProvinceItem):
			sql = "insert into province(province_code,province_name,short_name,link) values (%s,%s,%s,%s)"
			short_name = DistrictUtils.get_short_name(item['province_code'])
			self.cursor.execute(sql, (item['province_code'], item['province_name'], short_name, item['link']))
		elif isinstance(item, CommonItem):
			code = str(item.get('code'))
			# 城市
			if code.endswith('00000000'):
				sql = 'insert into city (city_code,city_name,province_code,link) values (%s,%s,%s,%s)'
				self.cursor.execute(sql, (item['code'][:4], item['name'], item['code'][:2], item['link']))
			elif code.endswith('000000'):
				sql = "insert into area (area_code,area_name,city_code,province_code,link) values (%s,%s,%s,%s,%s)"
				self.cursor.execute(sql, (
					item['code'][:6], item['name'], item['code'][:4], item['code'][:2], item['link']
				))
			else:
				sql = 'insert into street_town (code,name,area_code,city_code,province_code,link) values ' \
				      '(%s,%s,%s,%s,%s,%s) '
				self.cursor.execute(sql, (
					item['code'][:-3], item['name'], item['code'][:6], item['code'][:4], item['code'][:2],
					item['link']
				))
		elif isinstance(item, VillageItem):
			sql = 'insert into village (village_code,village_name,street_code,area_code,city_code,province_code,type_code) values ' \
			      '(%s,%s,%s,%s,%s,%s,%s)'
			self.cursor.execute(sql, (
				item['code'], item['name'], item['code'][:-3], item['code'][:6], item['code'][:4], item['code'][:2],
				item['type_code']
			))

	@classmethod
	def from_crawler(cls, crawler):
		return cls(
			mysql_host=crawler.settings.get('MYSQL_HOST'),
			mysql_port=crawler.settings.get('MYSQL_PORT'),
			mysql_user=crawler.settings.get('MYSQL_USER'),
			my_password=crawler.settings.get('MYSQL_PASSWORD'),
			mysql_db=crawler.settings.get('MYSQL_DB'),
		)

	def open_spider(self, spider):
		self.connect = pymysql.connect(
			host=self.mysql_host,
			port=self.mysql_port,
			user=self.mysql_user,
			passwd=self.mysql_password,
			database=self.mysql_db,
			harset=self.charset)
		self.cursor = self.connect.cursor()
		self.connect.autocommit(True)


	def close_spider(self, spider):
		self.cursor.close()
		self.connect.close()

class JsonWriterPipeline(object):
	def open_spider(self, spider):
		self.province_file = open('province.json', 'w', encoding='utf-8')
		self.province_file.write('[' + '\n')
		self.city_file = open('city.json', 'w', encoding='utf-8')
		self.city_file.write('[' + '\n')
		self.area_file = open('area.json', 'w', encoding='utf-8')
		self.area_file.write('[' + '\n')
		self.street_town_file = open('street_town.json', 'w', encoding='utf-8')
		self.street_town_file.write('[' + '\n')
		self.village_file = open('village.json', 'w', encoding='utf-8')
		self.village_file.write('[' + '\n')

	def close_spider(self, spider):
		self.province_file.write(']')
		self.province_file.close()
		self.city_file.write(']')
		self.city_file.close()
		self.area_file.write(']')
		self.area_file.close()
		self.street_town_file.write(']')
		self.street_town_file.close()
		self.village_file.write(']')
		self.village_file.close()

	def process_item(self, item, spider):
		if isinstance(item, ProvinceItem):
			short_name = DistrictUtils.get_short_name(item['province_code'])
			result = dict(
				province_code=item['province_code'], province_name=item['province_name'], short_name=short_name,
				link=item['link'])
			line = json.dumps(result, ensure_ascii=False) + ',\n'
			self.province_file.write(line)
			return item
		elif isinstance(item, CommonItem):
			code = str(item.get('code'))
			# 城市
			if code.endswith('00000000'):
				result = dict(
					city_code=item['code'][:4], city_name=item['name'], province_code=item['code'][:2],
					link=item['link']
				)
				line = json.dumps(result, ensure_ascii=False) + ',\n'
				self.city_file.write(line)
				return item
			elif code.endswith('000000'):
				result = dict(
					area_code=item['code'][:6], area_name=item['name'], city_code=item['code'][:4],
					province_code=item['code'][:2], link=item['link']
				)
				line = json.dumps(result, ensure_ascii=False) + ',\n'
				self.area_file.write(line)
				return item
			else:
				result = dict(
					code=item['code'][:-3], name=item['name'], area_code=item['code'][:6], city_code=item['code'][:4],
					province_code=item['code'][:2],
					link=item['link']
				)
				line = json.dumps(result, ensure_ascii=False) + ',\n'
				self.street_town_file.write(line)
				return item
		elif isinstance(item, VillageItem):
			result = dict(
				village_code=item['code'], village_name=item['name'], street_code=item['code'][:-3],
				area_code=item['code'][:6], city_code=item['code'][:4], province_code=item['code'][:2],
				link=item['type_code']
			)
			line = json.dumps(result, ensure_ascii=False) + ',\n'
			self.village_file.write(line)
			return item
