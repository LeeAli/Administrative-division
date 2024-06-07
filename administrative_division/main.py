import json

from scrapy import cmdline
import os
import sys

current_path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_path)
cmdline.execute(["scrapy", "crawl", "stats_gov_cn"])

# with open('../data/province.json', 'r', encoding='utf-8') as file:
#     lines = file.readlines()
#
# # 移除每行末尾的换行符并存储到列表中
#     if len(lines) > 1 and lines[-2].strip().endswith(','):
#         lines[-2] = lines[-2].rstrip(',\n') + '\n'
#
# # 将列表写入JSON文件
#     with open('../data/data.json', 'w', encoding='utf-8') as json_file:
#         json_file.writelines(lines)
# file_paths = {
#     'province': '../data/province.json',
#     'city': '../data/city.json',
#     'area': '../data/area.json',
#     'street_town': '../data/street_town.json',
#     'village': '../data/village.json',
# }
# for key, path in file_paths.items():
#     with open(path, 'r+', encoding='utf-8') as ff:
#         lines = ff.readlines()
#         if len(lines) > 1 and lines[-2].strip().endswith(','):
#             lines[-2] = lines[-2].rstrip(',\n') + '\n'
#             ff.seek(0)
#             ff.truncate()
#             ff.writelines(lines)
# lines = [
#     {"province_code": "110000", "province_name": "北京市", "short_name": "京", "link": "11.html"},
#     {"province_code": "120000", "province_name": "天津市", "short_name": "津", "link": "12.html"}]
# with open('../data/province.json', 'w+', encoding='utf-8') as file:
#     file.write('[\n')
#     for line in lines:
#         file.write(json.dumps(line, ensure_ascii=False) + ',\n')
#     print(file.tell()-2)
#     file.seek(file.tell() - 2, 0)
#     file.truncate()
#     file.write('\n]')
