# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from contextlib import contextmanager

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from administrative_division.district import DistrictUtils
from administrative_division.items import ProvinceItem, CommonItem, VillageItem
import json


class JsonWriterPipeline(object):
    def __init__(self):
        self.files = {

        }
        self.file_paths = {
            'province': '../data/province.json',
            'city': '../data/city.json',
            'area': '../data/area.json',
            'street_town': '../data/street_town.json',
            'village': '../data/village.json',
        }

    def open_spider(self, spider):
        for key, path in self.file_paths.items():
            self.files[key] = open(path, 'w', encoding='utf-8')
            self.files[key].write('[\n')

    def close_spider(self, spider):
        for key, file in self.files.items():
            file.write(']')
            file.close()
        self.remove_trailing_commas()

    def process_item(self, item, spider):
        if isinstance(item, ProvinceItem):
            self.write_json('province', {
                'province_code': item['province_code'],
                'province_name': item['province_name'],
                'short_name': DistrictUtils.get_short_name(item['province_code']),
                'link': item['link']
            })
        elif isinstance(item, CommonItem):
            self.process_common_item(item)
        elif isinstance(item, VillageItem):
            self.write_json('village', {
                'village_code': item['code'],
                'village_name': item['name'],
                'street_code': item['code'][:-3],
                'area_code': item['code'][:6],
                'city_code': item['code'][:4]+'00',
                'province_code': item['code'][:2],
                'short_name': DistrictUtils.get_short_name(item['code'][:2]),
                'type_code': item['type_code']
            })
        return item

    def remove_trailing_commas(self):
        for key, path in self.file_paths.items():
            with open(path, 'r+', encoding='utf-8') as ff:
                lines = ff.readlines()
                if len(lines) > 1 and lines[-2].strip().endswith(','):
                    lines[-2] = lines[-2].rstrip(',\n') + '\n'
                    ff.seek(0)
                    ff.truncate()
                    ff.writelines(lines)

    def process_common_item(self, item):
        code = str(item.get('code'))
        if code.endswith('00000000'):
            self.write_json('city', {
                'city_code': item['code'][:4]+'00',
                'city_name': item['name'],
                'province_code': item['code'][:2],
                'short_name': DistrictUtils.get_short_name(item['code'][:2]),
                'link': item['link']
            })
        elif code.endswith('000000'):
            self.write_json('area', {
                'area_code': item['code'][:6],
                'area_name': item['name'],
                'city_code': item['code'][:4]+'00',
                'province_code': item['code'][:2],
                'short_name': DistrictUtils.get_short_name(item['code'][:2]),
                'link': item['link']
            })
        else:
            self.write_json('street_town', {
                'code': item['code'][:-3],
                'name': item['name'],
                'area_code': item['code'][:6],
                'city_code': item['code'][:4]+'00',
                'province_code': item['code'][:2],
                'short_name': DistrictUtils.get_short_name(item['code'][:2]),
                'link': item['link']
            })

    def write_json(self, file_key, data):
        line = json.dumps(data, ensure_ascii=False) + ',\n'
        self.files[file_key].write(line)
