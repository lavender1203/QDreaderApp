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
#execute(['scrapy', 'crawl', 'qidian', '-s', 'LOG_FILE=debug.log'])
execute(['scrapy', 'crawl', 'qidian'])
#execute(['scrapy', 'crawl', 'getHongbao'])
def task(i):
    execute('scrapy crawl qidian -s IDQUEUE_MOD={} -s LOG_FILE=logs/scrapy_spider_{}.log'.format(i,i).split())

if __name__ == '__main__':
    settings = scrapy.utils.project.get_project_settings()
    queuesize = settings.getint('IDQUEUE_SIZE')   #10
    if not os.path.exists('logs'):
        os.makedirs('logs')
    #pool=Pool(queuesize)
    #for i in range(queuesize):
    #    pool.apply_async(task,args=(i,))
    #pool.close()
    #pool.join()
    #while 1:
    #    time.sleep(1e4)
    #    time.sleep(1)
    #jobs = []
    #while 1:
    #    for i in range(2):
    #        p = multiprocessing.Process(target=task, args=(i,))
    #        jobs.append(p)
    #        p.start()
    #        time.sleep(5)

