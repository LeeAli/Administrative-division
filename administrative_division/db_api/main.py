import os
import json

city_file = open(r'C:\Users\Lee\Desktop\city.sql', 'w', encoding='utf-8')
area_file = open(r'C:\Users\Lee\Desktop\area.sql', 'w', encoding='utf-8')


def pares():
	with open(r'C:\Users\Lee\Desktop\district.txt', 'r', encoding='utf-8') as f:
		for item in f.readlines():
			temp = item.split(',')
			if temp[0].endswith('0000'):
				pass
			elif temp[0].endswith("00"):
				city_sql = "insert into city (city_code,city_name,province_code) values ('%s','%s','%s');" % (
					temp[0][:4], temp[1], temp[0][:2])
				city_file.write(city_sql)
				city_file.write('\n')
			else:
				area_sql = "insert into area (area_code,area_name,city_code,province_code) values ('{0}','{1}','{2}','{3}');".format(
					temp[0], temp[1], temp[0][:4], temp[0][:2])
				area_file.write(area_sql)
				area_file.write('\n')
	city_file.close()
	area_file.close()

if __name__ == '__main__':
	read_test()
