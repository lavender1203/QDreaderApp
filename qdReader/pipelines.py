# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

class QdreaderPipeline(object):
    def process_item(self, item, spider):
        return item

class SquareHongbaoPipeline(object):
    def open_spider(self, spider):
        self.conn = pymysql.connect(
            host="127.0.0.1",
            port=3306,
            user="root",
            password="toor",
            db="hongbaodb",
            charset="utf8",
        )
        self.cursor = self.conn.cursor()
        '''
        sql = "CREATE TABLE IF NOT EXISTS hongbaos( \
                    id INT UNSIGNED AUTO_INCREMENT, \
                    hongbaoId BIGINT UNSIGNED NOT NULL DEFAULT 0, \
                    Status INT NOT NULL, \
                    BookId BIGINT UNSIGNED DEFAULT 0, \
                    BookName longtext , \
                    Type INT NOT NULL DEFAULT 0,\
                    Signature varchar(100) , \
                    create_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP, \
                    update_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, \
                    PRIMARY KEY (id) \
                )DEFAULT CHARSET=utf8;"
        self.cursor.execute(sql)
        self.conn.commit()
        '''
    def process_item(self, item, spider):
        #创建一个sql语句
        #print("开始插入数据")
        #insert into hongbaos(hongbaoId, Status)  select '1008611','1' from dual where not exists (select hongbaoId from hongbaos where hongbaoId = '143569398')
        sql = "insert into hongbaos ( hongbaoId, Status, BookId, BookName, Type, Signature) \
                select '%d', '%d', '%d','%s', '%d','%s' from dual \
                where not exists (select hongbaoId from hongbaos where hongbaoId = '%d')" \
                % (item["hongbaoId"], item["Status"], item['BookId'],  \
                  item['BookName'],  item['Type'],  item['Signature'], item['hongbaoId'])
        #print(sql)
        #更新数据 同一红包状态不同
        #sql = "update hongbaos set Status='%d' where hongbaoId='%d' and Status!='%d'" % (item['Status'], item['hongbaoId'], item['Status'])
        #sql = "if not exists (select hongbaoId from hongbaos where hongbaoId = '%d') then \
        #            insert into hongbaos values(NULL,'%d','%d') \
        #       elseif exists (select Status from hongbaos where Status != '%d')  then \
        #            update hongbaos set Status='%d' \
        #       end if" % (item["hongbaoId"], item["hongbaoId"], item["Status"], item["Status"], item["Status"])
        #sql = "INSERT INTO hongbaos VALUES(NULL,'%s','%s')" % (item["hongbaoId"], item["Status"])
        #print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.conn.close()
        self.cursor.close()

