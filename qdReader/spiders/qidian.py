# -*- coding: utf-8 -*-
import time
import urllib.parse
import scrapy
import json
from . import QDLogin
import sys
from scrapy.http.cookies import CookieJar

cookiejar = CookieJar()
class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['https://ptlogin.qidian.com/sdk/staticlogin']

    def start_requests(self):
        QDLogin.getQDSIGN1()
        # QDLogin.getQDSIGN('lasthongbaoid=0&pn=1&pz=20', usertoken='5880124')
        # QDLogin.genQDSIGN('Rv1rPTnczce|1558840202436|0|862679037204730|1|7.8.5|0|1180b6bf822f4ad2c451959a2a558a36|e967c9e5fd92879f6bac96358de84d90')
        QDLogin.setPostdata(signature=QDLogin.getSignature())
        yield scrapy.Request('https://ptlogin.qidian.com/sdk/staticlogin', callback=self.checkcodelogin, method="POST",\
                             headers=QDLogin.headers, body=urllib.parse.urlencode(QDLogin.getPostdata()))

    def checkcodelogin(self, response):
        if response.status == 200:
            data = json.loads(bytes.decode(response.body))

            session_key = data['data']['sessionKey']
            QDLogin.setPostdata(sessionkey=session_key)
            captcha = QDLogin.tcaptcha()
            # print(captcha)
            if captcha['sig'] != "" and captcha['code'] != "":
                QDLogin.setPostdata(sig=captcha['sig'])
                QDLogin.setPostdata(code=captcha['code'])
                print(QDLogin.postData)

                # yield scrapy.Request('https://ptlogin.qidian.com/sdk/checkcodelogin', callback=self.loginValidate, method="POST", \
                #              headers=QDLogin.headers, meta={'cookiejar': cookiejar}, body=urllib.parse.urlencode(QDLogin.getPostdata()))
                yield scrapy.Request('https://ptlogin.qidian.com/sdk/checkcodelogin', callback=self.loginValidate,
                                     method="POST",
                                     headers=QDLogin.headers,
                                     body=urllib.parse.urlencode(QDLogin.getPostdata()))
            else:
                print('验证码校验未通过')

    def loginValidate(self, response):
        url = 'https://druid.if.qidian.com/Atom.axd/Api/User/LoginValidate'
        data = json.loads(bytes.decode(response.body))
        if data['code'] == 0:
            print('验证码校验通过')
            QDLogin.ywkey = data['data']['ywKey']
            QDLogin.ywguid = data['data']['ywGuid']
            QDLogin.appId = data['data']['appId']
            QDLogin.areaId = data['data']['areaId']
            postData = {
                'ywkey': QDLogin.ywkey,
                'ywguid': QDLogin.ywguid,
                'loginfrom': 0,
                'isFirstRegister': 'false',
                'fromSource': QDLogin.source,
                'areaId': QDLogin.areaId,
                'appId': QDLogin.appId
            }
            headers = {
                'User-Agent': 'Mozilla/mobile QDReaderAndroid/7.8.5/380/1000031/862679037204730',
                'QDInfo': QDLogin.getQDInfo(),
                'QDSign': QDLogin.getQDSIGN1(QDLogin.getPostParams(postData)),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'druid.if.qidian.com',
                'Accept-Encoding': 'gzip',
            }

            # cookiejar.extract_cookies(response, response.request)
            # print(cookiejar._cookies)
            cookies = {
                'ywkey': '',
                'ywguid': '',
                'appId': QDLogin.appId,
                'areaId': QDLogin.areaId,
                'lang': QDLogin.lang,
                'bar': QDLogin.bar,
                'QDInfo': QDLogin.getQDInfo()
            }

            yield scrapy.Request(url, callback=self.getHongBaoList, method="POST",
                                 headers=headers, cookies=cookies, body=urllib.parse.urlencode(postData))
        else:
            print(data['message'])

    def getHongBaoList(self, response):
        data = json.loads(bytes.decode(response.body))
        if data['Result'] == 0:
            print('登录成功')
            QDLogin.cmfuToken = data['Data']['CmfuToken']
            QDLogin.userInfo = data['Data']['UserInfo']  # usertoken = userInfo[0]
            print(QDLogin.cmfuToken)
            print(QDLogin.userInfo)
            if QDLogin.pn > 5:
                QDLogin.pn = 1
            if QDLogin.pn < 6:
                # print(QDLogin.pn)
                lasthongbaoid = QDLogin.lasthongbaoid
                pn = QDLogin.pn
                urlParams = 'lasthongbaoid=' + lasthongbaoid + '&pn=' + str(pn) + '&pz=20'
                url_last = 'pn=' + str(QDLogin.pn) + '&pz=20' + '&lastHongbaoId=' + lasthongbaoid
                url = 'https://druid.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?' + url_last
                userToken = QDLogin.userInfo.split('|')[0]
                print(str(sys._getframe().f_lineno))
                headers = {
                    'User-Agent': 'Mozilla/mobile QDReaderAndroid/7.8.5/380/1000031/862679037204730',
                    'QDInfo': QDLogin.getQDInfo(app_usertoken=userToken),
                    'QDSign': QDLogin.getQDSIGN1(urlParams, usertoken=userToken),
                    'Host': 'druid.if.qidian.com',
                    'Accept-Encoding': 'gzip',
                }
                print(str(sys._getframe().f_lineno))
                cookie = {
                    'ywkey': QDLogin.ywkey,
                    'ywguid': QDLogin.ywguid,
                    'appId': QDLogin.appId,
                    'areaId': QDLogin.areaId,
                    'lang': QDLogin.lang,
                    'bar': QDLogin.bar,
                    'loginType': 4,
                    'lgk': 1,
                    'QDInfo': QDLogin.getQDInfo(app_usertoken=userToken),
                    'cmfuToken': QDLogin.cmfuToken
                }
                yield scrapy.Request(url, callback=self.parseHongbaoList, method="GET",
                                     headers=headers, cookies=cookie)
        else:
            print(data['message'])

    def parseHongbaoList(self, response):
        data = json.loads(bytes.decode(response.body))
        if data['Result'] == 0:
            hongbaolist = data['Data']['HongbaoList']['Data']
            i = 0
            QDLogin.pn = QDLogin.pn + 1
            for hongbao in hongbaolist:
                print(hongbao)
                if i == 19:
                    QDLogin.lasthongbaoid = str(hongbao['HongbaoId'])
                i = i + 1
            if QDLogin.lasthongbaoid is not None and QDLogin.pn < 6:
                time.sleep(2)
                lasthongbaoid = QDLogin.lasthongbaoid
                pn = QDLogin.pn
                urlParams = 'lasthongbaoid=' + lasthongbaoid + '&pn=' + str(pn) + '&pz=20'
                url_last = 'pn=' + str(QDLogin.pn) + '&pz=20' + '&lastHongbaoId=' + lasthongbaoid
                url = 'https://druid.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?' + url_last
                userToken = QDLogin.userInfo.split('|')[0]
                # print(str(sys._getframe().f_lineno))
                headers = {
                    'User-Agent': 'Mozilla/mobile QDReaderAndroid/7.8.5/380/1000031/862679037204730',
                    'QDInfo': QDLogin.getQDInfo(app_usertoken=userToken),
                    'QDSign': QDLogin.getQDSIGN1(urlParams, usertoken=userToken),
                    'Host': 'druid.if.qidian.com',
                    'Accept-Encoding': 'gzip',
                }

                cookie = {
                    'ywkey': QDLogin.ywkey,
                    'ywguid': QDLogin.ywguid,
                    'appId': QDLogin.appId,
                    'areaId': QDLogin.areaId,
                    'lang': QDLogin.lang,
                    'bar': QDLogin.bar,
                    'loginType': 4,
                    'lgk': 1,
                    'QDInfo': QDLogin.getQDInfo(app_usertoken=userToken),
                    'cmfuToken': QDLogin.cmfuToken
                }
                yield scrapy.Request(url, callback=self.parseHongbaoList, method="GET",
                                     headers=headers, cookies=cookie)
        else:
            print(data['message'])

