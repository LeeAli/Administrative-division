from scrapy import cmdline
import os
import sys

# os.path.abspath(__file__)  获取当前文件所在的路径
# os.path.dirname(os.path.abspath(__file__))  #获取当前路径的上级（父级路径）
# os.path.dirname('D:\codeworkplace\python\JobArticleSpider\main.py')   
# sys.path.append() 设置添加项目工程所在的路径，让编译器知道是哪个项目要执行  
# 路径设置两种方法：1.绝对路径 2.相对路径，获取当前项目所在系统的对应目录
curent_path=os.path.dirname(os.path.abspath(__file__))
sys.path.append(curent_path)
cmdline.execute(["scrapy","crawl","provinceSpider"])