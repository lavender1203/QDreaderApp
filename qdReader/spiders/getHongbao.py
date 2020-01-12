# -*- coding: utf-8 -*-
import scrapy
import os
import json
import urllib.parse
from . import QDLogin
from scrapy.http.cookies import CookieJar
import pymysql
from scrapy.utils.project import get_project_settings
from .tcaptcha import tcaptcha


class GethongbaoSpider(scrapy.Spider):
    name = 'getHongbao'
    allowed_domains = ['druid.if.qidian.com']
    start_urls = ['http://druid.if.qidian.com/Atom.axd/Api/HongBao/Get']
    conn = None

    # 从某本书某个章节里获取红包
    def start_requests(self):
        cookie_path = QDLogin.cookie_path
        deviceId = QDLogin.os_imei + '_' + QDLogin.os_qimei
        cookies = self.getCookies(cookie_path, deviceId)
        #从数据库查找可抢状态的红包
        sql = "select hongbaoId,BookId,Type,Signature from hongbaos where Status >= 0"
        setting = get_project_settings()
        self.conn = pymysql.connect(
            host=setting.get("DB_HOST"),
            port=setting.get("DB_PORT"),
            user=setting.get("DB_USER"),
            password=setting.get("DB_PASSWORD"),
            db=setting.get("DB_NAME"),
            charset=setting.get("DB_CHARSET")
        )
        cursor = self.conn.cursor()
        cursor.execute(sql)
        hongbaos = cursor.fetchall()

        for i,hongbao in enumerate(hongbaos):
            #print(hongbao)
            #print(len(hongbaos))
            if i <  len(hongbaos) - 1:
                continue
            print("************************************************************")    
            hongbaoId = hongbao[0]
            BookId = hongbao[1]
            Type = hongbao[2]
            Signature = hongbao[3]
            usertoken = cookies['usertoken']
            url = 'http://druid.if.qidian.com/Atom.axd/Api/HongBao/Get'
            postData = {
                'hongBaoId': hongbaoId,
            }
            headers = {
                'User-Agent': 'Mozilla/mobile QDReaderAndroid/' + QDLogin.app_versionname + '/' + \
                       QDLogin.app_versioncode + '/' + QDLogin.source + '/' + QDLogin.os_uuid,
                'QDInfo': QDLogin.getQDInfo(app_usertoken=usertoken),
                'AegisSign': QDLogin.getAegisSign(QDLogin.getPostParams(postData), usertoken=usertoken),
                'QDSign': QDLogin.getQDSIGN1(QDLogin.getPostParams(postData), usertoken=usertoken),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'druid.if.qidian.com',
                'Accept-Encoding': 'gzip',
            }
            yield scrapy.Request(url, callback=self.getHongBaoResponse, method="POST",
                         headers=headers, cookies=cookies, \
                             body=urllib.parse.urlencode(postData), meta={'cookies': cookies})
        cursor.close()

    def getHongBaoResponse(self, response):
        data = json.loads(bytes.decode(response.body))
        if data['Result'] == 0:
            BookId = data['Data']['BookId']
            hongbaoId = data['Data']['HongBaoId']
            ccId = data['Data']['ccId']
            HongBaoSign = data['Data']['HongBaoSign']
            Status = data['Data']['Status']
            Type = data['Data']['Type']
            cookies = response.meta['cookies']
            usertoken = cookies['usertoken']
            action_url = data['ActionUrl']

            postData = {
                'gender': 0,
                'HongBaoSign': HongBaoSign,
                'BookId': BookId,
                'hongBaoId': hongbaoId,
                'code': '',
                'sessionKey': ''
            }

            headers = {
                'User-Agent': 'Mozilla/mobile QDReaderAndroid/' + QDLogin.app_versionname + '/' + \
                       QDLogin.app_versioncode + '/' + QDLogin.source + '/' + QDLogin.os_uuid,
                'QDInfo': QDLogin.getQDInfo(app_usertoken=usertoken),
                'AegisSign': QDLogin.getAegisSign(QDLogin.getPostParams(postData), usertoken=usertoken),
                'QDSign': QDLogin.getQDSIGN1(QDLogin.getPostParams(postData), usertoken=usertoken),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'druid.if.qidian.com',
                'Accept-Encoding': 'gzip',
            }
            url = 'http://druid.if.qidian.com/Atom.axd/Api/HongBao/UseHongBao'
            yield scrapy.Request(url, callback=self.parse, method="POST",
                         headers=headers, cookies=cookies, \
                                 body=urllib.parse.urlencode(postData), meta={'postData': postData, 'cookies':cookies})
              #                   body=urllib.parse.urlencode(postData), meta={'postData': postData, 'headers':headers, 'cookies':cookies}) 
        else:
            print(data)

    def parse(self, response):
        data = json.loads(bytes.decode(response.body))
        result = data['Result']
        if result == 0:
            print("抢到了")
        elif result == -70019:
            postData = response.meta['postData']
            #headers = response.meta['headers']
            cookies = response.meta['cookies']
            usertoken = cookies['usertoken']
            captcha = QDLogin.captcha()
            postData['code'] = captcha['code']
            postData['sessionKey'] = data['SessionKey'] 
            headers = {
                'User-Agent': 'Mozilla/mobile QDReaderAndroid/' + QDLogin.app_versionname + '/' + \
                       QDLogin.app_versioncode + '/' + QDLogin.source + '/' + QDLogin.os_uuid,
                'QDInfo': QDLogin.getQDInfo(app_usertoken=usertoken),
                'AegisSign': QDLogin.getAegisSign(QDLogin.getPostParams(postData), usertoken=usertoken),
                'QDSign': QDLogin.getQDSIGN1(QDLogin.getPostParams(postData), usertoken=usertoken),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'druid.if.qidian.com',
                'Accept-Encoding': 'gzip',
            }
            url = 'http://druid.if.qidian.com/Atom.axd/Api/HongBao/UseHongBao'
            if captcha['code'] is not None and captcha['code'] != '':
                print("通过滑块验证,重新抢")
                yield scrapy.Request(url, callback=self.parse1, method="POST",
                         headers=headers, cookies=cookies, \
                         body=urllib.parse.urlencode(postData), \
                         meta={'postData': postData, 'headers':headers, 'cookies':cookies})
            else:
                print("滑块验证失败")
        elif result == -1004009:
            #已抢完   更新数据库红包状态为-3
            newStatus = -3
            sql = "update hongbaos set Status='%d' where hongbaoId='%d' and Status!='%d'" \
                    % (newStatus, postData['hongBaoId'], newStatus)
            cursor = self.conn.cursor()
            cursor.execute(sql)
            self.conn.commit()
            print(data['Message'])
        else:
            print(data['Message'])
    
    def parse1(self, response):
        data = json.loads(bytes.decode(response.body))
        result = data['Result']
        if result == 0:
            print("抢到了")
        elif result == -70019:
            print(data['Message'])
        elif result == -1004009:
            print(data['Message'])
        else:
            print(data['Message'])

        
    def getCookies(self, cookie_path, deviceId):
        cookie_file = cookie_path + deviceId + '.txt'
        if not os.path.exists(cookie_file):
            print(cookie_file + "文件不存在")
            return None
        with open(cookie_file, 'r') as f:
            # 查看cookie是否过期
            import time
            import re
            if time.time() - os.path.getctime(cookie_file) < QDLogin.cookies_expire:
                cookie_jar = f.read()
                p = re.compile(r'<Cookie (.*?) for .*?>')
                cookies = re.findall(p, cookie_jar)
                cookies = (cookie.split('=', 1) for cookie in cookies)
                cookies = dict(cookies)
                if cookies is None or cookies == '':
                    print("cookie 为空")
                    return ''
                else:
                    return cookies
            else:
                # cookies已经过期
                f.truncate()
                return ''
