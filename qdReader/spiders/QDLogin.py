# -*- coding: utf-8 -*-
import ctypes
from jpype import *
import os.path
import webbrowser
# 图像处理标准库
from PIL import Image
#web测试
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
# 鼠标操作
from selenium.webdriver.common.action_chains import ActionChains
# 等待时间 产生随机数
import time
import random
from browsermobproxy import Server
from selenium.webdriver import DesiredCapabilities
import urllib
import hashlib
from .user import User
from .device import Device

libcrypto = ctypes.CDLL('libs/libcrypto.so.3')
chaptasets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

user = User()
device = Device
# username = user.name
# password = user.password
username = 'weimingshi90'
password = 'wang14587'
appid = '1600000770'
width = '140'
height = '140'
map = ''
captcha = {
    'sig': "",
    'code': ""
}

ywkey = ''
ywguid = ''
appId = ''
areaId = ''
lang = 'cn'
bar = '72'
source = '1000031'
QDInfo = ''
QDSign = ''
cmfuToken = ''
userInfo = ''

lasthongbaoid = '0'
pn = 1

headers = {
        'referer': 'http://android.qidian.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ptlogin.qidian.com',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.9.1'
}

postData = {
        'password': password,
        'devicename': 'Honor 8',
        'loginType': 23,
        'source': '1000031',
        'signature': '',
        'appid': 12,
        'referer': 'http://android.qidian.com',
        'auto': 1,
        'ticket': 0,
        'devicetype': 'Huawei_FRD-AL00',
        'qimei': '43757bd7111bb806',
        'code': '',
        'format': 'json',
        'osversion': 'Android7.0_7.8.5_380',
        'username': username,
        'imei': '862679037204730',
        'sdkversion': 121,
        'autotime': 30,
        'version': 380,
        'returnurl': 'http://www.qidian.com',
        'areaid': 30,
}

def getPostParams(postdatas):
    ret = ''
    length = len(postdatas)
    index = 0
    c = ''
    tmpdata = {}
    for key in postdatas:
        tmpdata[key.lower()] = postdatas[key]
    sortedLowerKeys = sorted(tmpdata)
    # print(sortedLowerKeys)
    for key in sortedLowerKeys:
        if index < length-1:
            c = '&'
        else:
            c = ''
        ret += key + '=' + str(tmpdata[key]) + c
        index = index + 1
    print(ret)
    return ret

def my_base64(input_data):
        input_len = len(input_data)
        v5 = []
        v6 = input_len - 3
        v2 = 0
        v0 = 0
        while v0 <= v6:
            v3 = (input_data[v0] & 255) << 16 | (input_data[v0 + 1] & 255) << 8 | input_data[v0 + 2] & 255
            v5.append(chaptasets[v3 >> 18 & 63])
            v5.append(chaptasets[v3 >> 12 & 63])
            v5.append(chaptasets[v3 >> 6 & 63])
            v5.append(chaptasets[v3 & 63])
            v3 = v0 + 3
            v0 = v2 + 1
            if v2 >= 14:
                v5.append(' ')
                v0 = 0
            v2 = v0
            v0 = v3
        if v0 == -2 + input_len:
            v0 = (input_data[v0 + 1] & 255) << 8 | (input_data[v0] & 255) << 16
            v5.append(chaptasets[v0 >> 18 & 63])
            v5.append(chaptasets[v0 >> 12 & 63])
            v5.append(chaptasets[v0 >> 6 & 63])
            v5.append("=")
        elif v0 == -1 + input_len:
            v0 = (input_data[v0] & 255) << 16
            v5.append(chaptasets[v0 >> 18 & 63])
            v5.append(chaptasets[v0 >> 12 & 63])
            v5.append("==")

        return ''.join(v5)

def genSignature(plain_text):
    # libcrypto = ctypes.CDLL('libs/libcrypto.so.3')
    result = libcrypto.DES_gen_signature(plain_text)
    # print("%ld" % result)
    tmp = ctypes.string_at(result, 48)
    signature = my_base64(tmp)
    return signature

def getSignature():
    plain_text = '862679037204730|43757bd7111bb806|' + str(int(time.time()))
    return genSignature(bytes(plain_text, encoding='utf-8'))

def genQDSIGN(plain_text):
    # libcrypto = ctypes.CDLL('libs/libcrypto.so.3')
    result = libcrypto.DES_gen_qdsign(plain_text)
    if len(plain_text) % 8:
        length = len(plain_text) + 8 - len(plain_text) % 8
    else:
        length = len(plain_text)
    tmps = ctypes.string_at(result, -1)
    # tmps = ctypes.string_at(result, length)
    # tmps = b'G\xb4\xc2\xb3\xa4\xe8\xbbe\xe7\x15\xfd\xd9R\xa5\x8fPlw\x1c\xb18\xef\x95\xf4\x83\x19\xa46\xaa^\xf3R\xc7J7\xdf\xdf\x06\xb8\xd4TT$\xfe\xc7\xe6\xeft~A\x9cxG\x1e\xf37\xa2v\xe4z\xe7\xb0\x02*\x88\x97\x03\xa9\x94x3\x92\xef\x86\x84\xb5\x8aq\xdd\x86\xb2\xae\x9ey`B\xa8\x05$\xbb\xab\xd7\xe2-2)\x89\x18E\xd1\x8a\xa4\x06\xe6\x8e\xe2\x9b\x14G\x0e\xa2+\x9fO\xf9\x9f\xb0\xdf\xff\xf8'

    print(type(tmps))
    signature = my_base64(tmps)
    print(signature)
    return signature

def getQDSIGN1(postdata="", usertoken='0'):
    src = 'Rv1rPTnczce'
    timestamp = str(int(time.time() * 1000))
    # timestamp = '1558780472479'
    uuid = '862679037204730'
    # uuid = '359250052265715'
    version_name = '7.8.5'
    version_a = '0'
    # postdata = 'appid=12&areaid=30&fromsource=1000031&isfirstregister=false&loginfrom=0&ywguid=800005880124&ywkey=yw4lY4emxuLV'
    signatures = '308204a830820390a003020102020900936eacbe07f201df300d06092a864886f70d0101050500308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d301e170d3038303232393031333334365a170d3335303731373031333334365a308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d30820120300d06092a864886f70d01010105000382010d00308201080282010100d6931904dec60b24b1edc762e0d9d8253e3ecd6ceb1de2ff068ca8e8bca8cd6bd3786ea70aa76ce60ebb0f993559ffd93e77a943e7e83d4b64b8e4fea2d3e656f1e267a81bbfb230b578c20443be4c7218b846f5211586f038a14e89c2be387f8ebecf8fcac3da1ee330c9ea93d0a7c3dc4af350220d50080732e0809717ee6a053359e6a694ec2cb3f284a0a466c87a94d83b31093a67372e2f6412c06e6d42f15818dffe0381cc0cd444da6cddc3b82458194801b32564134fbfde98c9287748dbf5676a540d8154c8bbca07b9e247553311c46b9af76fdeeccc8e69e7c8a2d08e782620943f99727d3c04fe72991d99df9bae38a0b2177fa31d5b6afee91f020103a381fc3081f9301d0603551d0e04160414485900563d272c46ae118605a47419ac09ca8c113081c90603551d230481c13081be8014485900563d272c46ae118605a47419ac09ca8c11a1819aa48197308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d820900936eacbe07f201df300c0603551d13040530030101ff300d06092a864886f70d010105050003820101007aaf968ceb50c441055118d0daabaf015b8a765a27a715a2c2b44f221415ffdace03095abfa42df70708726c2069e5c36eddae0400be29452c084bc27eb6a17eac9dbe182c204eb15311f455d824b656dbe4dc2240912d7586fe88951d01a8feb5ae5a4260535df83431052422468c36e22c2a5ef994d61dd7306ae4c9f6951ba3c12f1d1914ddc61f1a62da2df827f603fea5603b2c540dbd7c019c36bab29a4271c117df523cdbc5f3817a49e0efa60cbd7f74177e7a4f193d43f4220772666e4c4d83e1bd5a86087cf34f2dec21e245ca6c2bb016e683638050d2c430eea7c26a1c49d3760a58ab7f1a82cc938b4831384324bd0401fa12163a50570e684d'
    plain_text = src + '|' + timestamp + '|' + usertoken + '|' + uuid + '|' + '1' + '|' + version_name + '|' + version_a + '|' \
                 + hashlib.md5(postdata.encode(encoding='utf-8')).hexdigest() + '|' + hashlib.md5(signatures.encode(encoding='utf-8')).hexdigest()
    print(plain_text)
    print(len(plain_text))
    plain_text = plain_text.encode('utf-8')

    from Crypto.Cipher import DES3

    key = b'\x7B\x31\x64\x59\x67\x71\x45\x29\x68\x39\x2C\x52\x29\x68\x4B\x71\x45\x63\x76\x34\x5D\x6B\x5B\x68'
    iv = b'\x30\x31\x32\x33\x34\x35\x36\x37'
    cipher = DES3.new(key, DES3.MODE_CBC, iv)

    # plaintext = b'Rv1rPTnczce|1558780472479|5880124|359250052265715|1|7.8.5|0|8afc1ba869e104d10f535458832d4023|e967c9e5fd92879f6bac96358de84d90'
    lx = len(plain_text)
    padding = 8 - lx % 8
    if padding != 0:
        length = lx + padding
        if padding == 1:
            plain_text = plain_text.decode('utf-8') + b'\x01'.decode('utf-8')
        elif padding == 2:
            plain_text = plain_text.decode('utf-8') + b'\x02\x02'.decode('utf-8')
        elif padding == 3:
            plain_text = plain_text.decode('utf-8') + b'\x03\x03\x03'.decode('utf-8')
        elif padding == 4:
            plain_text = plain_text.decode('utf-8') + b'\x04\x04\x04\x04'.decode('utf-8')
        elif padding == 5:
            plain_text = plain_text.decode('utf-8') + b'\x05\x05\x05\x05\x05'.decode('utf-8')
        elif padding == 6:
            plain_text = plain_text.decode('utf-8') + b'\x06\x06\x06\x06\x06\x06'.decode('utf-8')
        elif padding == 7:
            plain_text = plain_text.decode('utf-8') + b'\x07\x07\x07\x07\x07\x07\x07'.decode('utf-8')
    else:
        length = lx
    msg = cipher.encrypt(plain_text.encode('utf-8'))
    signature = my_base64(msg)
    print(signature)
    return signature

def getQDSIGN(postdata="", usertoken='0'):
    src = 'Rv1rPTnczce'
    timestamp = str(int(time.time() * 1000))
    # timestamp = '1558780472479'
    uuid = '862679037204730'
    # uuid = '359250052265715'
    version_name = '7.8.5'
    version_a = '0'
    # postdata = 'appid=12&areaid=30&fromsource=1000031&isfirstregister=false&loginfrom=0&ywguid=800005880124&ywkey=yw4lY4emxuLV'
    signatures = '308204a830820390a003020102020900936eacbe07f201df300d06092a864886f70d0101050500308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d301e170d3038303232393031333334365a170d3335303731373031333334365a308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d30820120300d06092a864886f70d01010105000382010d00308201080282010100d6931904dec60b24b1edc762e0d9d8253e3ecd6ceb1de2ff068ca8e8bca8cd6bd3786ea70aa76ce60ebb0f993559ffd93e77a943e7e83d4b64b8e4fea2d3e656f1e267a81bbfb230b578c20443be4c7218b846f5211586f038a14e89c2be387f8ebecf8fcac3da1ee330c9ea93d0a7c3dc4af350220d50080732e0809717ee6a053359e6a694ec2cb3f284a0a466c87a94d83b31093a67372e2f6412c06e6d42f15818dffe0381cc0cd444da6cddc3b82458194801b32564134fbfde98c9287748dbf5676a540d8154c8bbca07b9e247553311c46b9af76fdeeccc8e69e7c8a2d08e782620943f99727d3c04fe72991d99df9bae38a0b2177fa31d5b6afee91f020103a381fc3081f9301d0603551d0e04160414485900563d272c46ae118605a47419ac09ca8c113081c90603551d230481c13081be8014485900563d272c46ae118605a47419ac09ca8c11a1819aa48197308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d820900936eacbe07f201df300c0603551d13040530030101ff300d06092a864886f70d010105050003820101007aaf968ceb50c441055118d0daabaf015b8a765a27a715a2c2b44f221415ffdace03095abfa42df70708726c2069e5c36eddae0400be29452c084bc27eb6a17eac9dbe182c204eb15311f455d824b656dbe4dc2240912d7586fe88951d01a8feb5ae5a4260535df83431052422468c36e22c2a5ef994d61dd7306ae4c9f6951ba3c12f1d1914ddc61f1a62da2df827f603fea5603b2c540dbd7c019c36bab29a4271c117df523cdbc5f3817a49e0efa60cbd7f74177e7a4f193d43f4220772666e4c4d83e1bd5a86087cf34f2dec21e245ca6c2bb016e683638050d2c430eea7c26a1c49d3760a58ab7f1a82cc938b4831384324bd0401fa12163a50570e684d'
    plain_text = src + '|' + timestamp + '|' + usertoken + '|' + uuid + '|' + '1' + '|' + version_name + '|' + version_a + '|' \
                 + hashlib.md5(postdata.encode(encoding='utf-8')).hexdigest() + '|' + hashlib.md5(signatures.encode(encoding='utf-8')).hexdigest()
    print(plain_text)
    print(len(plain_text))
    plain_text = plain_text.encode(encoding='utf-8')
    return genQDSIGN(plain_text)

def getPostdata():
    return postData

def setPostdata(signature="", password="", ticket="", username="", sessionkey="", sig="", code=""):
    if signature != "":
        postData['signature'] = signature
    if password != "":
        postData['password'] = password
    if ticket != "":
        postData['ticket'] = ticket
    if username != "":
        postData['username'] = username
    if sessionkey != "":
        postData['sessionkey'] = sessionkey
    if sig != "":
        postData['sig'] = sig
    if code != "":
        postData['code'] = code

def getQDInfo(app_usertoken='0'):
    libpath = os.path.dirname(os.path.abspath(__file__)) + '/../..' + "/libs/"
    jarpath = os.path.join(os.path.abspath('.'), libpath)
    if not isJVMStarted():
        startJVM("/usr/lib/jvm/java-8-openjdk-amd64/jre/lib/amd64/server/libjvm.so", "-ea",
             "-Djava.class.path=%s" % (jarpath + 'testDes3Cbc.jar'))

    JDClass = JClass("QDInfo")
    os_uuid = '862679037204730'
    app_versionname = '7.8.5'
    os_android_version = '7.0'
    os_device_type = 'FRD-AL00'
    app_versioncode = '380'
    os_version_1 = '1794'
    os_dim = '1080'
    timestamp = str(int(time.time() * 1000))
    source = '1000031'
    os_qimei = '43757bd7111bb806'
    data = os_uuid + '|' + app_versionname + '|' + os_dim + '|' + os_version_1 + '|' + source + '|' \
           + os_android_version + '|' + '1' + '|' + os_device_type + '|' + app_versioncode + '|' + source + '|' + '4' \
           + '|' + app_usertoken + '|' + timestamp + '|' + '1' + '|' + os_qimei
    key = "0821CAAD409B8402"
    # print(data)
    QDInfo = JDClass.getQDInfo(data, key)
    return QDInfo

# 20分钟内只能连续3次
def tcaptcha():
    libpath = os.path.dirname(os.path.abspath(__file__)) + '/../..' + "/libs/"
    url = 'file://' + libpath + 'tcaptcha_webview.html' + '?appid=' + appid + '&width=' + width + '&height=' + height + '&map=' + map
    user_agent = 'Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36' + ' TCSDK/1.0.2'

    QDInfo = getQDInfo()
    # server = Server("/opt/project/qdReader/libs/browsermob-proxy-2.1.4/bin/browsermob-proxy")
    # server.start()
    # proxy = server.create_proxy()
    options = Options()
    options.add_argument('--headless')
    # options.add_argument("--proxy-server={0}".format(proxy.proxy))
    options.add_argument('--no-sandbox')
    options.add_argument("--touch-events")
    # options.add_argument('auto-open-devtools-for-tabs')
    options.add_argument('X-Requested-With="com.qidian.QDReader"')
    mobile_emulation = {"deviceMetrics": {"width": 1080, "height": 1920, "pixelRatio": 3.0}, "userAgent": user_agent}
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_experimental_option('prefs', {'profile.default_content_settings.popups': 0,'intl.accept_languages': 'zh-CN,en-US;q=0.8'})
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options)
    # tag the har(network logs) with a name
    # proxy.new_har("tcaptcha", options={'captureHeaders': True})
    # proxy.headers(headers={'Via': '', 'X-Requested-With': 'com.qidian.QDReader'})
    driver.get("http://ssl.captcha.qq.com:443")
    time.sleep(3)
    # print(driver.get_cookies())
    driver.add_cookie({'name': 'ywkey', 'value': ''})
    driver.add_cookie({'name': 'ywguid', 'value': ''})
    driver.add_cookie({'name': 'QDInfo', 'value': QDInfo})

    driver.get(url)
    time.sleep(3)
    # print(driver.get_cookies())
    captcha['sig'] = driver.execute_script('return localStorage.getItem("ticket")')
    captcha['code'] = driver.execute_script('return localStorage.getItem("randstr")')
    # result = proxy.har
    # print(result)  # returns a Network logs (HAR) as JSON
    # for entry in result['log']['entries']:
        # if entry['request']['url'].find("cap_union_prehandle") > 0:
        # print(entry)

    # driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    # el = driver.find_element_by_id('TencentCaptcha')
    # el.click()
    # time.sleep(3)
    # captcha['sig'] = driver.execute_script('return localStorage.getItem("sig")')
    # captcha['code'] = driver.execute_script('return localStorage.getItem("code")')

    # print(captcha)
    # 因为QQ登录是在一个框架中又有一个框架
    # 所以需要先进框架, 再定位节点元素
    # 进入框架有两种方法
    # 1. 通过框架id进入
    while captcha['sig'] == "" or captcha['code'] == "" or captcha['sig'] == None or captcha['code'] == None:
        time.sleep(10)
        # 2. 通过节点定位   如果登录成功就不需要往下。。。
        now_window = driver.window_handles
        print(now_window)
        el_frame = driver.find_element_by_xpath('//*[@id="tcaptcha_iframe"]')
        driver.switch_to.frame(el_frame)

        # 获取拖拽的圆球
        slide_block = driver.find_element_by_id('tcaptcha_drag_thumb')

        # 生成拖拽移动轨迹，加3是为了模拟滑过缺口位置后返回缺口的情况
        loc = 210
        track_list = get_track(loc + 1)
        time.sleep(1)
        ActionChains(driver).click_and_hold(slide_block).perform()
        time.sleep(0.2)
        # 根据轨迹拖拽圆球
        for track in track_list:
            ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
        # 模拟人工滑动超过缺口位置返回至缺口的情况，数据来源于人工滑动轨迹，同时还加入了随机数，都是为了更贴近人工滑动轨迹
        imitate = ActionChains(driver).move_by_offset(xoffset=-1, yoffset=0)
        time.sleep(0.015)
        imitate.perform()
        time.sleep(random.randint(6, 10) / 10)
        imitate.perform()
        time.sleep(0.04)
        imitate.perform()
        time.sleep(0.012)
        imitate.perform()
        time.sleep(0.019)
        imitate.perform()
        time.sleep(0.033)
        ActionChains(driver).move_by_offset(xoffset=1, yoffset=0).perform()
        # 放开圆球
        ActionChains(driver).pause(random.randint(6, 14) / 10).release(slide_block).perform()
        time.sleep(5)
        captcha['sig'] = driver.execute_script('return localStorage.getItem("sig")')
        captcha['code'] = driver.execute_script('return localStorage.getItem("code")')
    # 务必记得加入quit()或close()结束进程，不断测试电脑只会卡卡西
    # server.stop()
    driver.close()
    return captcha

# 滑块移动轨迹
def get_track(distance):
    track = []
    current = 0
    mid = distance*3/4
    t = random.randint(2, 3)/10
    v = 0
    while current < distance:
        if current < mid:
            a = 25
        else:
            a = -3
        v0 = v
        v = v0+a*t
        move = v0*t+1/2*a*t*t
        current += move
        track.append(round(move))
    return track

def match_source(image):
    imagea = Image.open('img/source1.png')
    imageb = Image.open('img/source2.png')
    imagec = Image.open('img/source3.png')
    imaged = Image.open('img/source4.png')
    list = [imagea, imageb, imagec, imaged]
    # 通过像素差遍历匹配本地原图
    for i in list:
        # 本人电脑原图与缺口图对应滑块图片横坐标相同，纵坐标原图比缺口图大88px，可根据实际情况修改
        pixel1 = image.getpixel((868, 340))
        pixel2 = i.getpixel((868, 428))
        # pixel[0]代表R值，pixel[1]代表G值，pixel[2]代表B值
        if abs(pixel1[0] - pixel2[0]) < 5:
            return i
    return image

