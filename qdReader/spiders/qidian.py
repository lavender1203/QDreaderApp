# -*- coding: utf-8 -*-
import time
import urllib.parse
import scrapy
import json
from . import QDLogin
import sys
import datetime
import os
import re
from scrapy.http.cookies import CookieJar
from ..items import SquareHongbaoItem
import requests
import time
import logging
import pymysql
from scrapy.utils.project import get_project_settings                                                                              


cookiejar = CookieJar()
class QidianSpider(scrapy.Spider):
    name = 'qidian'
    allowed_domains = ['qidian.com']
    start_urls = ['https://ptlogin.qidian.com/sdk/staticlogin']
    start = 0
    # user = User()
    # device = Device()
    # cookie = getCookies()

    def start_requests(self):
        self.start = time.time()
        #QDLogin.getAegisSign()
        #QDLogin.getQDSIGN1()
        #self.init() #初始化用户和设备信息
        #1 判断登录状态，已经登录就直接获取广场红包
        cookie_path = QDLogin.cookie_path
        device_id = QDLogin.os_imei + '_' + QDLogin.os_qimei
        cookies = self.isOnline(cookie_path, device_id)
        if cookies == '' or cookies is None: 
            QDLogin.setPostdata(signature=QDLogin.getSignature())
            yield scrapy.Request('https://ptlogin.qidian.com/sdk/staticlogin', callback=self.checkcodelogin, method="POST",\
                        headers=QDLogin.headers, body=urllib.parse.urlencode(QDLogin.getPostdata()))
        else:
            lasthongbaoid = QDLogin.lasthongbaoid
            pn = QDLogin.pn
            urlParams = 'lasthongbaoid=' + lasthongbaoid + '&pn=' + str(pn) + '&pz=20'
            url_last = 'pn=' + str(QDLogin.pn) + '&pz=20' + '&lastHongbaoId=' + lasthongbaoid
            url = 'https://druid.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?' + url_last
            userToken = cookies['usertoken']
            #print(str(sys._getframe().f_lineno))
            headers = {
                'User-Agent':'Mozilla/mobile QDReaderAndroid/' + QDLogin.app_versionname + '/' + \
                QDLogin.app_versioncode+ '/'+ QDLogin.source + '/'+ QDLogin.os_uuid, 
                'QDInfo': QDLogin.getQDInfo(app_usertoken=userToken),
                'AegisSign': QDLogin.getAegisSign(urlParams, usertoken=userToken),
                'QDSign': QDLogin.getQDSIGN1(urlParams, usertoken=userToken),
                'Host': 'druid.if.qidian.com',
                'Accept-Encoding': 'gzip',
            }
            #print(str(sys._getframe().f_lineno))
            cookie = {
                'ywkey': cookies['ywkey'],
                'ywguid': cookies['ywguid'],
                'appId': cookies['appId'],
                'areaId': cookies['areaId'],
                'lang': cookies['lang'],
                'mode': cookies['mode'],
                'bar': cookies['bar'],
                'qimei': cookies['qimei'],
                'loginType': cookies['loginType'],
                'lgk': cookies['lgk'],
                'QDInfo': QDLogin.getQDInfo(app_usertoken=userToken),
                'cmfuToken': cookies['cmfuToken'],
                'usertoken': cookies['usertoken']
            }
            yield scrapy.Request(url, callback=self.parseHongbaoList, method="GET",
                         headers=headers,cookies=cookie, meta={'pn': 1, \
                         'lasthongbaoid': '0', 'cookie': cookie})

    def isOnline(self, cookie_path, device_id):
        return self.getCookies(cookie_path, device_id)

    def checkcodelogin(self, response):
        if response.status == 200:
            data = json.loads(bytes.decode(response.body))
            session_key = data['data']['sessionKey']
            captcha = QDLogin.captcha()
            #print(captcha)
            if captcha['sig'] != "" and captcha['code'] != "":
                QDLogin.setPostdata(sig=captcha['sig'])
                QDLogin.setPostdata(code=captcha['code'])
                #print(QDLogin.headers)
                #print(QDLogin.postData)
                if session_key != '':
                    QDLogin.setPostdata(sessionkey=session_key)
                    yield scrapy.Request('https://ptlogin.qidian.com/sdk/checkcodelogin', callback=self.loginValidate,
                                     method="POST",
                                     headers=QDLogin.headers,
                                     body=urllib.parse.urlencode(QDLogin.getPostdata()))
                else:
                    ywkey = data['data']['ywKey']
                    appId = data['data']['appId']
                    areaId = data['data']['areaId']
                    ywguid = data['data']['ywGuid']
                    postData = {
                        'ywkey': ywkey,
                        'appId': appId,
                        'areaId': areaId,
                        'isFirstRegister': 'false',
                        'fromSource': QDLogin.source,
                        'loginfrom': '0',
                        'ywguid': ywguid
                    }
                    headers = {
                        'User-Agent': 'Mozilla/mobile QDReaderAndroid/' + QDLogin.app_versionname + '/' + \
                                QDLogin.app_versioncode+ '/'+ QDLogin.source + '/'+ QDLogin.os_uuid,
                        'QDInfo': QDLogin.getQDInfo(),
                        'AegisSign': QDLogin.getAegisSign(QDLogin.getPostParams(postData)),
                        'QDSign': QDLogin.getQDSIGN1(QDLogin.getPostParams(postData)),
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'Host': 'druid.if.qidian.com',
                        'Accept-Encoding': 'gzip',
                    }
                    url = 'https://druid.if.qidian.com/Atom.axd/Api/User/LoginValidate'
                    import re
                    import os
                    #先获取绑定的设备 选择用哪台设备登录
                    if not os.path.exists(QDLogin.cookie_path):
                        print("当前账号"+QDLogin.username+"绑定设备所有cookie文件丢失")
                        print("请手动创建目录:"+ QDLogin.cookie_path)
                    else:
                        #查找绑定设备
                        cookiefiles = os.listdir(QDLogin.cookie_path)
                        deviceNum = len(cookiefiles)
                        if cookiefiles is not None and deviceNum > 0:
                            #用户操作选择绑定设备
                            print("当前账号已绑定设备如下：")
                            i = 0
                            for devicefile in cookiefiles:
                                print(str(i)+ '.' + os.path.splitext(devicefile)[0])
                                i = i+1
                            if deviceNum == 1:
                                n = 0
                            else:
                                print("请输入选择设备的序号:")
                                n = input().split()[0]
                                n = int(n)
                            if n >= 0 and n < deviceNum:
                                cookie_file = QDLogin.cookie_path + cookiefiles[n]
                                with open(cookie_file, 'r') as f:
                                    #查看cookie是否过期 一个月
                                    import datetime
                                    import time
                                    expire = 30*24*60*60 
                                    if time.time() - os.path.getctime(cookie_file) < expire:
                                        cookie_jar = f.read()
                                        p = re.compile(r'<Cookie (.*?) for .*?>')
                                        cookies = re.findall(p, cookie_jar)
                                        cookies = (cookie.split('=', 1) for cookie in cookies)
                                        cookies = dict(cookies)
                                        if cookies is None or cookies == '':
                                            print("cookie 不存在")
                                        else:
                                            if cookies['ywkey'] is not None and cookies['appId'] is not None and \
                                               cookies['areaId'] is not None and cookies['loginType'] is not None and \
                                               cookies['cmfuToken'] is not None:
                                                new_cookies = {
                                                    'ywkey': cookies['ywkey'],
                                                    'ywguid': ywguid,
                                                    'appId': cookies['appId'],
                                                    'areaId': cookies['areaId'],
                                                    'lang': QDLogin.lang,
                                                    'mode': 'normal',
                                                    'bar': QDLogin.bar,
                                                    'qimei': QDLogin.os_qimei,
                                                    'loginType': cookies['loginType'],
                                                    'cmfuToken': cookies['cmfuToken'],
                                                    'QDInfo': QDLogin.getQDInfo()
                                                }   
                                                yield scrapy.Request(url, callback=self.loginCheck, method="POST",
                                                            headers=headers, cookies=new_cookies, body=urllib.parse.urlencode(postData)) 
                                            else:
                                                print(cookie_file + "cookies 格式错误")
                                    else:
                                        f.truncate()
                            else:
                                print("无此绑定设备")
                        else:
                            print("当前账号"+QDLogin.username+"绑定设备所有cookie文件丢失")
                            print("请手动恢复"+ QDLogin.cookie_path + "目录下的cookie文件：")
                            print("文件名为绑定设备的imei_qimei.txt, 如:cookies/xuelong1012/866174010680714_866174010680714.txt")
                            print("文件内容示例:")
                            example_file = 'cookies/cookie_example.txt'
                            if not os.path.exists(example_file):
                                print("示例文件不存在")
                            else:
                                with open(example_file) as f:
                                    content = f.read()
                                    print(content)
            else:
                print('验证码校验未通过')

    def loginValidate(self, response):
        url = 'https://druid.if.qidian.com/Atom.axd/Api/User/LoginValidate'
        data = json.loads(bytes.decode(response.body))
        if data['code'] == 0:
            print('验证码校验通过')
            QDLogin.ywkey = data['data']['ywKey']
            if QDLogin.ywkey == '':
                print("设备未绑定")
                QDLogin.sessionkey = data['data']['contextId']
                url = 'https://ptlogin.qidian.com/sdk/sendphonemsg'
                postData = {
                    'devicename': QDLogin.devicename,
                    'source': QDLogin.source,
                    'signature': QDLogin.getSignature(),
                    'appid': QDLogin.appId,
                    'referer': 'http://android.qidian.com',
                    'auto': 1,
                    'ticket': 0,
                    'devicetype': QDLogin.devicetype,
                    'qimei': QDLogin.os_qimei,
                    'format': 'json',
                    'osversion': 'Android'+QDLogin.os_android_version + QDLogin.app_versionname + QDLogin.app_versioncode,
                    'imei': QDLogin.os_imei,
                    'sdkversion': QDLogin.sdkversion,
                    'version': QDLogin.app_versioncode,
                    'areaid': QDLogin.areaId,
                    'returnurl': 'http://www.qidian.com',
                    'sessionkey': QDLogin.sessionkey 
                }
                headers = {
                    'User-Agent': 'okhttp/3.12.6',
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'referer': 'http://android.qidian.com',
                    'Host': 'ptlogin.qidian.com',
                    'Accept-Encoding': 'gzip',
                }
                #print(postData)
                #print(headers)
                yield scrapy.Request(url, callback=self.phoneKeyCodeLogin, method="POST",
                                 headers=headers, body=urllib.parse.urlencode(postData))
            QDLogin.ywguid = data['data']['ywGuid']
            if data['data']['appId'] != 0:
                QDLogin.appId = data['data']['appId']
            if data['data']['areaId'] != 0:
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
                'User-Agent': 'Mozilla/mobile QDReaderAndroid/' + QDLogin.app_versionname + '/' + \
                    QDLogin.app_versioncode+ '/'+ QDLogin.source + '/'+ QDLogin.os_uuid,
                'QDInfo': QDLogin.getQDInfo(),
                'AegisSign': QDLogin.getAegisSign(QDLogin.getPostParams(postData)),
                'QDSign': QDLogin.getQDSIGN1(QDLogin.getPostParams(postData)),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'druid.if.qidian.com',
                'Accept-Encoding': 'gzip',
            }

            cookies = {
                'ywkey': QDLogin.ywkey,
                'ywguid': QDLogin.ywguid,
                'appId': QDLogin.appId,
                'areaId': QDLogin.areaId,
                'lang': QDLogin.lang,
                'mode': QDLogin.mode,
                'bar': QDLogin.bar,
                'qimei': QDLogin.os_qimei,
                'QDInfo': QDLogin.getQDInfo()
            }

            yield scrapy.Request(url, callback=self.loginCheck, method="POST",
                                 headers=headers, cookies=cookies, body=urllib.parse.urlencode(postData))
        else:
            print(data)

    def getCode(self):
        print("请输入6位手机验证码：")
        code =  input().split()
        return code

    def phoneKeyCodeLogin(self, response):
        data = json.loads(bytes.decode(response.body))
        if data['code'] == 0:
            print('请查收手机验证码.')
            #code = '142080'
            code = self.getCode()[0]
            url = 'https://ptlogin.qidian.com/sdk/phonekeycodelogin'
            postData = {
                'devicename': QDLogin.devicename,
                'source': QDLogin.source,
                'signature': QDLogin.getSignature(),
                'appid': QDLogin.appId,
                'referer': 'http://android.qidian.com',
                'auto': 1,
                'ticket': 0,
                'devicetype': QDLogin.devicetype,
                'qimei': QDLogin.os_qimei,
                'code': code,
                'format': 'json',
                'osversion': 'Android'+QDLogin.os_android_version + QDLogin.app_versionname + QDLogin.app_versioncode,
                'imei': QDLogin.os_imei,
                'sdkversion': QDLogin.sdkversion,
                'autotime': 30,
                'version': QDLogin.app_versioncode,
                'areaid': QDLogin.areaId,
                'returnurl': 'http://www.qidian.com',
                'sessionkey': QDLogin.sessionkey 
            }
            headers = {
                'User-Agent': 'okhttp/3.12.6',
                'Content-Type': 'application/x-www-form-urlencoded',
                'referer': 'http://android.qidian.com',
                'Host': 'ptlogin.qidian.com',
                'Accept-Encoding': 'gzip',
            }
            #print(postData)
            #print(headers)
            yield scrapy.Request(url, callback=self.phoneKeyCodeLoginValidate, method="POST",
                             headers=headers, body=urllib.parse.urlencode(postData))	
        else:
            print(data['message'])
        
    def phoneKeyCodeLoginValidate(self, response):
        url = 'https://druid.if.qidian.com/Atom.axd/Api/User/LoginValidate'
        data = json.loads(bytes.decode(response.body))
        if data['code'] == 0:
            QDLogin.ywkey = data['data']['ywKey']
            QDLogin.ywguid = data['data']['ywGuid']
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
                'User-Agent': 'Mozilla/mobile QDReaderAndroid/' + QDLogin.app_versionname + '/' + \
                    QDLogin.app_versioncode+ '/'+ QDLogin.source + '/'+ QDLogin.os_uuid,
                'QDInfo': QDLogin.getQDInfo(),
                'AegisSign': QDLogin.getAegisSign(QDLogin.getPostParams(postData)),
                'QDSign': QDLogin.getQDSIGN1(QDLogin.getPostParams(postData)),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'druid.if.qidian.com',
                'Accept-Encoding': 'gzip',
            }
            cookies = {
                'ywkey': QDLogin.ywkey,
                'ywguid': QDLogin.ywguid,
                'appId': QDLogin.appId,
                'areaId': QDLogin.areaId,
                'lang': QDLogin.lang,
                'mode': QDLogin.mode,
                'bar': QDLogin.bar,
                'qimei': QDLogin.os_qimei,
                'QDInfo': QDLogin.getQDInfo()
            }

            yield scrapy.Request(url, callback=self.loginCheck, method="POST",
                         headers=headers, cookies=cookies, body=urllib.parse.urlencode(postData))
        else: 
            print(data['message'])

    def loginCheck(self, response):
        data = json.loads(bytes.decode(response.body))
        if data['Result'] == 0:
            print('登录成功')
            QDLogin.cmfuToken = data['Data']['CmfuToken']
            QDLogin.userInfo = data['Data']['UserInfo']  # usertoken = userInfo[0]
            # 到这里我们的登录状态已经写入到response header中的'Set-Cookies'中了,
            # 使用extract_cookies方法可以提取response中的cookie
            cookiejar.extract_cookies(response, response.request)
            # cookiejar是类字典类型的,将它写入到文件中
            #每次登录成功都要更新该账号对应绑定设备的cookie
            deviceId = QDLogin.os_imei + '_' + QDLogin.os_qimei
            if not os.path.exists(QDLogin.cookie_path):
                os.mkdirs(QDLogin.cookie_path)
            cookie_file = QDLogin.cookie_path + deviceId + '.txt'
            cookie_ywguid = "<Cookie ywguid="+str(QDLogin.ywguid)+" for .qidian.com/>\n"
            cookie_lang = "<Cookie lang="+str(QDLogin.lang)+" for .qidian.com/>\n"
            cookie_mode = "<Cookie mode="+str(QDLogin.mode)+" for .qidian.com/>\n"
            cookie_bar = "<Cookie bar="+str(QDLogin.bar)+" for .qidian.com/>\n"
            cookie_qimei = "<Cookie qimei="+str(QDLogin.os_qimei)+" for .qidian.com/>\n"
            cookie_QDInfo = "<Cookie QDInfo="+QDLogin.QDInfo+" for .qidian.com/>\n"
            cookie_usertoken = "<Cookie usertoken="+QDLogin.userInfo.split('|')[0]+" for .qidian.com/>\n"
            with open(cookie_file, 'w') as f:
                for cookie in cookiejar:
                    f.write(str(cookie) + '\n')
                f.write(cookie_ywguid)
                f.write(cookie_lang)
                f.write(cookie_mode)
                f.write(cookie_bar)
                f.write(cookie_qimei)
                f.write(cookie_QDInfo)
                f.write(cookie_usertoken)
        else:
            print(data)

    def parseHongbaoList(self, response):
        #timeArray = time.localtime(time.time() - self.start)
        #timeStr = time.strftime("%S", timeArray)
        #print("到开始解析红包列表耗时:" + timeStr + "s")
        data = json.loads(bytes.decode(response.body))
        cookies = response.meta['cookie']
        if data['Result'] == 0:
            pn = response.meta['pn'] 
            lasthongbaoid = response.meta['lasthongbaoid'] 
            #print(cookies)
            if data['Data']['HongbaoList'] is not None:
                count = data['Data']['HongbaoList']['TotalCount']
                hongbaolist = data['Data']['HongbaoList']['Data']
                if count != len(hongbaolist):
                    count = len(hongbaolist)
                if pn == 1:
                    pass
                    #print("用户"+QDLogin.username+"在红包广场共发现"+str(count)+"个红包")
                i = 0
                page_max = 20
                if count % 20 != 0: 
                    page_max = int(count%20)
                for hongbao in hongbaolist:
                    status = hongbao['Status']
                    hongbaoId = hongbao['HongbaoId']
                    item = SquareHongbaoItem()
                    item['hongbaoId'] = hongbaoId
                    item['Status'] = status
                    item['BookName'] = hongbao['BookName']
                    item['BookId'] = hongbao['BookId']
                    item['Signature'] = str(hongbao['Signature'])
                    item['Type'] = hongbao['Type']
                    yield item
                    #print(hongbaoId)
                    if status == 0:
                        print("*******************************************")
                        print("id="+ str(hongbaoId) + "的红包可以抢.")
                        #抢红包
                        BookId = hongbao['BookId']
                        Type = hongbao['Type']
                        Signature = hongbao['Signature']
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
                    if i == page_max -1:
                        lasthongbaoid = str(hongbao['HongbaoId'])
                    i = i + 1
                if count%20 != 0 and pn < int(count/20)+1 or count%20 == 0 and pn < int(count/20):
                    pn = pn + 1
                    urlParams = 'lasthongbaoid=' + lasthongbaoid + '&pn=' + str(pn) + '&pz=20'
                    url_last = 'pn=' + str(pn) + '&pz=20' + '&lastHongbaoId=' + lasthongbaoid
                    url = 'https://druid.if.qidian.com/Atom.axd/Api/HongBao/GetSquare?' + url_last
                    userToken = cookies['usertoken']
                    # print(str(sys._getframe().f_lineno))
                    headers = {
                        'User-Agent':'Mozilla/mobile QDReaderAndroid/' + QDLogin.app_versionname + '/' + \
                        QDLogin.app_versioncode+ '/'+ QDLogin.source + '/'+ QDLogin.os_uuid, 
                        'QDInfo': QDLogin.getQDInfo(app_usertoken=userToken),
                        'AegisSign': QDLogin.getAegisSign(urlParams, usertoken=userToken),
                        'QDSign': QDLogin.getQDSIGN1(urlParams, usertoken=userToken),
                        'Host': 'druid.if.qidian.com',
                        'Accept-Encoding': 'gzip',
                    }
                    yield scrapy.Request(url, callback=self.parseHongbaoList, method="GET",
                                         headers=headers, cookies=cookies, meta={'pn':pn, \
                                                                                 'lasthongbaoid':lasthongbaoid, 'cookie': cookies})
        else:
            print(data['message'])

    def getHongBaoResponse(self, response):
        data = json.loads(bytes.decode(response.body))
        #print(data)
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
                'sessionKey': '',
                'sig':''
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
              #                   body=urllib.parse.urlencode(postData), meta={'postData': postData, 'headers':headers, 'cookies':cooki
        else:
            print(data)

    def getCookies(self, cookie_path, device_id):
        cookie_file = cookie_path + device_id + '.txt'
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
    
    def parse1(self, response):
        data = json.loads(bytes.decode(response.body))
        #print("parse1")
        #print(data)
        postData = response.meta['postData']
        result = data['Result']
        if result == 0:
            print("过验证码抢到了一个红包")
        elif result == -70019:
            print("还要验证????不是过了吗")
            print(data['Message'])
        elif result == -1004009:
            #已抢完   更新数据库红包状态为-3
            '''
            newStatus = -3
            setting = get_project_settings()
            sql = "update hongbaos set Status='%d' where hongbaoId='%d' and Status!='%d'" % (newStatus, postData['hongBaoId'], newStatus)
            conn = pymysql.connect(
                host=setting.get("DB_HOST"),
                port=setting.get("DB_PORT"),
                user=setting.get("DB_USER"),
                password=setting.get("DB_PASSWORD"),
                db=setting.get("DB_NAME"),
                charset=setting.get("DB_CHARSET")
            )
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            '''
            print(data['Message'])
        else:
            print(data['Message'])

    def parse(self, response):
        data = json.loads(bytes.decode(response.body))
        #print("parse")
        #print(data)
        result = data['Result']
        postData = response.meta['postData']
        #headers = response.meta['headers']
        cookies = response.meta['cookies']
        usertoken = cookies['usertoken']
        if result == 0:
            print("无验证码抢到了一个红包")
        elif result == -70019:
            captcha = QDLogin.captcha()
            postData['code'] = captcha['code']
            postData['sig'] = captcha['sig']
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
                                 body=urllib.parse.urlencode(postData), meta={'postData': postData, 'headers':headers, 'cookies':cookies})
            else:
                print("滑块验证失败")
        elif result == -1004009:                                                                                                       
            #已抢完   更新数据库红包状态为-3
            '''
            setting = get_project_settings()
            newStatus = -3
            sql = "update hongbaos set Status='%d' where hongbaoId='%d' and Status!='%d'" % (newStatus, postData['hongBaoId'], newStatus)
            conn = pymysql.connect(
                host=setting.get("DB_HOST"),
                port=setting.get("DB_PORT"),
                user=setting.get("DB_USER"),
                password=setting.get("DB_PASSWORD"),
                db=setting.get("DB_NAME"),
                charset=setting.get("DB_CHARSET")
            )
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            cursor.close()
            '''
            print(data['Message'])                                                                                                     
        else:
            print(data['Message'])
    
