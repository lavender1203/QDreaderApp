"""
  该文件用于调试程序
"""
from scrapy.cmdline import execute
import os
import sys
import scrapy
from multiprocessing import Pool
import multiprocessing
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
#print(os.path.dirname(os.path.abspath(__file__)))
execute(['scrapy', 'crawl', 'getHongbao'])

