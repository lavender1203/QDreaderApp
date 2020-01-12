# -*- coding: utf-8 -*-
import ctypes
import operator
from jpype import *
import os.path
import math
import urllib.parse
import webbrowser
import tempfile
import time
from functools import reduce
from io import BytesIO
# 图像处理标准库
from PIL import Image
from PIL import ImageChops

import urllib
import hashlib
#from .user import User
#from .device import Device
from .tcaptcha import tcaptcha

libcrypto = ctypes.CDLL('libs/libcrypto.so.3')
chaptasets = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

#user = User()
#device = Device

#os_uuid = '359250052265715'
#os_imei = os_uuid
#os_qimei = '359250052265715'
#os_android_version = '6.0'
#os_device_type = 'Nexus 5'
#os_version_1 = 'MRA58K'
#os_dim = '1080'
#devicename = 'Nexus 5'
#devicetype = 'google_Nexus 5'
#user_agent = 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36 TCSDK/1.0.2'
#sdkversion = '201'

#一个手机号一天最多获取10次验证码
#imei和qimei同时变化才认为不是同一设备
os_uuid = '862679037204730'
os_uuid = '862679037204733'
os_uuid = '866174010680714'
os_uuid = '866174010680719'
os_imei = os_uuid
os_qimei = '43757bd7111bb806'
os_qimei = '866174010680714'
os_qimei = '866174010680719'
os_android_version = '7.0'
os_android_version = '5.1.1'
os_device_type = 'FRD-AL00'
os_device_type = 'OPPO _OPPO R11'
os_version_1 = '1794'
os_dim = '1080'
devicename = 'Honor 8'
devicename = 'Nexus 6'
devicetype = 'OPPO _OPPO R11'
user_agent = 'Mozilla/5.0 (Linux; Android 7.0; FRD-AL00 Build/HUAWEIFRD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/55.0.2883.91 Mobile Safari/537.36' + ' TCSDK/1.0.2'
sdkversion = '121'
sdkversion = '201'

app_versioncode = '418'
#app_versioncode = '380'
app_versionname = '7.9.14'
#app_versionname = '7.8.5'
# username = user.name
# password = user.password

username = 'xuelong1012'
#username = 'oneto160'
password = '1212aaq'
#username = user.name
#password = user.password

ywkey = ''
ywguid = '800005880124'
appId = '12'
areaId = '30'
lang = 'cn'
bar = '72'
mode = 'normal'
source = '1000017'
sessionkey = ''
QDInfo = ''
QDSign = ''
cmfuToken = ''
userInfo = ''

lasthongbaoid = '0'
pn = 1
cookies_expire = 30 * 24 * 60 * 60
cookie_path = 'cookies/' + username + '/'

headers = {
        'referer': 'http://android.qidian.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'ptlogin.qidian.com',
        'Accept-Encoding': 'gzip',
        'User-Agent': 'okhttp/3.12.6'
}

postData = {
        'password': password,
        'devicename': devicename,
        'loginType': 23,
        'source': source,
        'signature': '',
        'appid': 12,
        'referer': 'http://android.qidian.com',
        'auto': 1,
        'ticket': 0,
        'devicetype': devicetype,
        'qimei': os_qimei,
        'code': '',
        'format': 'json',
        'osversion': 'Android' + os_android_version + '_'+ app_versionname + '_'+ app_versioncode,
        'username': username,
        'imei': os_uuid,
        'sdkversion': sdkversion,
        'autotime': 30,
        'version': app_versioncode,
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
    #print(ret)
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
    plain_text = os_imei + '|' + os_qimei + '|' + str(int(time.time()))
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

    signature = my_base64(tmps)
    return signature

def getAegisSign(postdata="", usertoken='0'):
    #src = '0201359dcd3'
    timestamp = str(int(time.time() * 1000))
    #timestamp = '1578464052468'
    #os_uuid = '359250052265715'
    #postdata = 'appid=12&areaid=30&fromsource=1000017&isfirstregister=false&loginfrom=0&ywguid=800005880124&ywkey=ywzuMR7P4A0c'
    version_name = app_versionname
    version_a = '0'
    tmp = hashlib.md5((os_uuid + usertoken).encode(encoding='utf-8')).hexdigest() #前11位为src 后24位为key
    src = tmp[:11]
    key = tmp[8:]
    # postdata = 'appid=12&areaid=30&fromsource=1000031&isfirstregister=false&loginfrom=0&ywguid=800005880124&ywkey=yw4lY4emxuLV'
    #signatures = '308204a830820390a003020102020900936eacbe07f201df300d06092a864886f70d0101050500308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d301e170d3038303232393031333334365a170d3335303731373031333334365a308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d30820120300d06092a864886f70d01010105000382010d00308201080282010100d6931904dec60b24b1edc762e0d9d8253e3ecd6ceb1de2ff068ca8e8bca8cd6bd3786ea70aa76ce60ebb0f993559ffd93e77a943e7e83d4b64b8e4fea2d3e656f1e267a81bbfb230b578c20443be4c7218b846f5211586f038a14e89c2be387f8ebecf8fcac3da1ee330c9ea93d0a7c3dc4af350220d50080732e0809717ee6a053359e6a694ec2cb3f284a0a466c87a94d83b31093a67372e2f6412c06e6d42f15818dffe0381cc0cd444da6cddc3b82458194801b32564134fbfde98c9287748dbf5676a540d8154c8bbca07b9e247553311c46b9af76fdeeccc8e69e7c8a2d08e782620943f99727d3c04fe72991d99df9bae38a0b2177fa31d5b6afee91f020103a381fc3081f9301d0603551d0e04160414485900563d272c46ae118605a47419ac09ca8c113081c90603551d230481c13081be8014485900563d272c46ae118605a47419ac09ca8c11a1819aa48197308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d820900936eacbe07f201df300c0603551d13040530030101ff300d06092a864886f70d010105050003820101007aaf968ceb50c441055118d0daabaf015b8a765a27a715a2c2b44f221415ffdace03095abfa42df70708726c2069e5c36eddae0400be29452c084bc27eb6a17eac9dbe182c204eb15311f455d824b656dbe4dc2240912d7586fe88951d01a8feb5ae5a4260535df83431052422468c36e22c2a5ef994d61dd7306ae4c9f6951ba3c12f1d1914ddc61f1a62da2df827f603fea5603b2c540dbd7c019c36bab29a4271c117df523cdbc5f3817a49e0efa60cbd7f74177e7a4f193d43f4220772666e4c4d83e1bd5a86087cf34f2dec21e245ca6c2bb016e683638050d2c430eea7c26a1c49d3760a58ab7f1a82cc938b4831384324bd0401fa12163a50570e684d'
    postdataMD5 = hashlib.md5(postdata.encode(encoding='utf-8')).hexdigest()
    rPostdataMD5 = ''.join(reversed(list(postdataMD5)))
    rHalfPostdataMD5 = ''.join(list(rPostdataMD5)[::2])
    data = rHalfPostdataMD5 + usertoken + version_name
    plain_text = src + '|' + timestamp + '|' + usertoken + '|' + os_uuid + '|' + '1' + '|' + version_name + '|' + version_a + '|' \
                 + hashlib.md5(data.encode(encoding='utf-8')).hexdigest() + '|' + rPostdataMD5
    plain_text = plain_text.encode('utf-8')

    from Crypto.Cipher import DES3

    #key = b'\x63\x64\x33\x63\x64\x37\x34\x31\x35\x35\x36\x31\x63\x33\x62\x61\x62\x38\x37\x35\x37\x34\x30\x60'
    iv = b'\x30\x31\x32\x33\x34\x35\x36\x37'
    cipher = DES3.new(key, DES3.MODE_CBC, iv)

    # plaintext = b'Rv1rPTnczce|1558780472479|5880124|359250052265715|1|7.8.5|0|8afc1ba869e104d10f535458832d4023|e967c9e5fd92879f6bac96358de84d90'
    lx = len(plain_text)
    padding = 8 - lx % 8
    if padding != 0:
        length = lx + padding
        if padding == 1:
            plain_text = plain_text.decode('utf-8') + b'\x01'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 2:
            plain_text = plain_text.decode('utf-8') + b'\x02\x02'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 3:
            plain_text = plain_text.decode('utf-8') + b'\x03\x03\x03'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 4:
            plain_text = plain_text.decode('utf-8') + b'\x04\x04\x04\x04'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 5:
            plain_text = plain_text.decode('utf-8') + b'\x05\x05\x05\x05\x05'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 6:
            plain_text = plain_text.decode('utf-8') + b'\x06\x06\x06\x06\x06\x06'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 7:
            plain_text = plain_text.decode('utf-8') + b'\x07\x07\x07\x07\x07\x07\x07'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
    else:
        length = lx
    #msg = cipher.encrypt(plain_text.encode('utf-8'))
    msg = cipher.encrypt(plain_text)
    signature = my_base64(msg)
    filename = '/tmp/in.txt'
    fin = open(filename, 'w', encoding='utf-8')
    fin.write(plain_text.decode('utf-8'))
    fin.close()
    import subprocess
    out = subprocess.check_output(["openssl", "des-ede3-cbc", "-in",filename,"-K", bytes(key, encoding='utf-8').hex(), "-iv", iv.hex()])

    #out = os.system("openssl des-ede3-cbc -in in.txt  -K '7B3164596771452968392C5229684B71456376345D6B5B68' -iv '3031323334353637'
    signature = my_base64(out)
    return signature

def getQDSIGN1(postdata="", usertoken='0'):
    src = 'Rv1rPTnczce'
    timestamp = str(int(time.time() * 1000))
    #timestamp = '1578464052466'
    #postdata = 'appid=12&areaid=30&fromsource=1000017&isfirstregister=false&loginfrom=0&ywguid=800005880124&ywkey=ywzuMR7P4A0c'
    #os_uuid = '359250052265715'
    version_name = app_versionname
    version_a = '0'
    # postdata = 'appid=12&areaid=30&fromsource=1000031&isfirstregister=false&loginfrom=0&ywguid=800005880124&ywkey=yw4lY4emxuLV'
    signatures = '308204a830820390a003020102020900936eacbe07f201df300d06092a864886f70d0101050500308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d301e170d3038303232393031333334365a170d3335303731373031333334365a308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d30820120300d06092a864886f70d01010105000382010d00308201080282010100d6931904dec60b24b1edc762e0d9d8253e3ecd6ceb1de2ff068ca8e8bca8cd6bd3786ea70aa76ce60ebb0f993559ffd93e77a943e7e83d4b64b8e4fea2d3e656f1e267a81bbfb230b578c20443be4c7218b846f5211586f038a14e89c2be387f8ebecf8fcac3da1ee330c9ea93d0a7c3dc4af350220d50080732e0809717ee6a053359e6a694ec2cb3f284a0a466c87a94d83b31093a67372e2f6412c06e6d42f15818dffe0381cc0cd444da6cddc3b82458194801b32564134fbfde98c9287748dbf5676a540d8154c8bbca07b9e247553311c46b9af76fdeeccc8e69e7c8a2d08e782620943f99727d3c04fe72991d99df9bae38a0b2177fa31d5b6afee91f020103a381fc3081f9301d0603551d0e04160414485900563d272c46ae118605a47419ac09ca8c113081c90603551d230481c13081be8014485900563d272c46ae118605a47419ac09ca8c11a1819aa48197308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d820900936eacbe07f201df300c0603551d13040530030101ff300d06092a864886f70d010105050003820101007aaf968ceb50c441055118d0daabaf015b8a765a27a715a2c2b44f221415ffdace03095abfa42df70708726c2069e5c36eddae0400be29452c084bc27eb6a17eac9dbe182c204eb15311f455d824b656dbe4dc2240912d7586fe88951d01a8feb5ae5a4260535df83431052422468c36e22c2a5ef994d61dd7306ae4c9f6951ba3c12f1d1914ddc61f1a62da2df827f603fea5603b2c540dbd7c019c36bab29a4271c117df523cdbc5f3817a49e0efa60cbd7f74177e7a4f193d43f4220772666e4c4d83e1bd5a86087cf34f2dec21e245ca6c2bb016e683638050d2c430eea7c26a1c49d3760a58ab7f1a82cc938b4831384324bd0401fa12163a50570e684d'
    signatures = '308202253082018ea00302010202044e239460300d06092a864886f70d0101050500305731173015060355040a0c0ec386c3b0c2b5c3a3c396c390c38e311d301b060355040b0c14c386c3b0c2b5c3a3c396c390c38ec384c38dc3b8311d301b06035504030c14c386c3b0c2b5c3a3c396c390c38ec384c38dc3b8301e170d3131303731383032303331325a170d3431303731303032303331325a305731173015060355040a0c0ec386c3b0c2b5c3a3c396c390c38e311d301b060355040b0c14c386c3b0c2b5c3a3c396c390c38ec384c38dc3b8311d301b06035504030c14c386c3b0c2b5c3a3c396c390c38ec384c38dc3b830819f300d06092a864886f70d010101050003818d0030818902818100a3d47f8bfd8d54de1dfbc40a9caa88a43845e287e8f40da2056be126b17233669806bfa60799b3d1364e79a78f355fd4f72278650b377e5acc317ff4b2b3821351bcc735543dab0796c716f769c3a28fedc3bca7780e5fff6c87779f3f3cdec6e888b4d21de27df9e7c21fc8a8d9164bfafac6df7d843e59b88ec740fc52a3c50203010001300d06092a864886f70d0101050500038181001f7946581b8812961a383b2d860b89c3f79002d46feb96f2a505bdae57097a070f3533c42fc3e329846886281a2fbd5c87685f59ab6dd71cc98af24256d2fbf980ded749e2c35eb0151ffde993193eace0b4681be4bcee5f663dd71dd06ab64958e02a60d6a69f21290cb496dd8784a4c31ebadb1b3cc5cb0feebdaa2f686ee2'
    plain_text = src + '|' + timestamp + '|' + usertoken + '|' + os_uuid + '|' + '1' + '|' + version_name + '|' + version_a + '|' \
                 + hashlib.md5(postdata.encode(encoding='utf-8')).hexdigest() + '|' + hashlib.md5(signatures.encode(encoding='utf-8')).hexdigest()
    plain_text = plain_text.encode('utf-8')

    from Crypto.Cipher import DES3

    key = b'\x7B\x31\x64\x59\x67\x71\x45\x29\x68\x39\x2C\x52\x29\x68\x4B\x71\x45\x63\x76\x34\x5D\x6B\x5B\x68'
    iv = b'\x30\x31\x32\x33\x34\x35\x36\x37'
    cipher = DES3.new(key, DES3.MODE_CBC, iv)

    #plain_text = b'Rv1rPTnczce|1578464052466|0|359250052265715|1|7.9.14|0|9f813dae5163c4f2390f2bd3a38e5102|f189adc92b816b3e9da29ea304d4a7e4'
    # plaintext = b'Rv1rPTnczce|1558780472479|5880124|359250052265715|1|7.8.5|0|8afc1ba869e104d10f535458832d4023|e967c9e5fd92879f6bac96358de84d90'
    lx = len(plain_text)
    padding = 8 - lx % 8
    if padding != 0:
        length = lx + padding
        if padding == 1:
            plain_text = plain_text.decode('utf-8') + b'\x01'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 2:
            plain_text = plain_text.decode('utf-8') + b'\x02\x02'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 3:
            plain_text = plain_text.decode('utf-8') + b'\x03\x03\x03'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 4:
            plain_text = plain_text.decode('utf-8') + b'\x04\x04\x04\x04'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 5:
            plain_text = plain_text.decode('utf-8') + b'\x05\x05\x05\x05\x05'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 6:
            plain_text = plain_text.decode('utf-8') + b'\x06\x06\x06\x06\x06\x06'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
        elif padding == 7:
            plain_text = plain_text.decode('utf-8') + b'\x07\x07\x07\x07\x07\x07\x07'.decode('utf-8')
            plain_text = plain_text.encode('utf-8')
    else:
        length = lx
    filename = '/tmp/in.txt'
    fin = open(filename, 'w', encoding='utf-8')
    fin.write(plain_text.decode('utf-8'))
    fin.close()
    import subprocess
    out = subprocess.check_output(["openssl", "des-ede3-cbc", "-in",filename,"-K", '7B3164596771452968392C5229684B71456376345D6B5B68', "-iv", '3031323334353637'])

    #out = os.system("openssl des-ede3-cbc -in in.txt  -K '7B3164596771452968392C5229684B71456376345D6B5B68' -iv '3031323334353637'")
    signature = my_base64(out)
    return signature

def getQDSIGN(postdata="", usertoken='0'):
    src = 'Rv1rPTnczce'
    timestamp = str(int(time.time() * 1000))
    # timestamp = '1558780472479'
    uuid = os_uuid
    # uuid = '359250052265715'
    version_name = app_versionname
    version_a = '0'
    # postdata = 'appid=12&areaid=30&fromsource=1000031&isfirstregister=false&loginfrom=0&ywguid=800005880124&ywkey=yw4lY4emxuLV'
    signatures = '308204a830820390a003020102020900936eacbe07f201df300d06092a864886f70d0101050500308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d301e170d3038303232393031333334365a170d3335303731373031333334365a308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d30820120300d06092a864886f70d01010105000382010d00308201080282010100d6931904dec60b24b1edc762e0d9d8253e3ecd6ceb1de2ff068ca8e8bca8cd6bd3786ea70aa76ce60ebb0f993559ffd93e77a943e7e83d4b64b8e4fea2d3e656f1e267a81bbfb230b578c20443be4c7218b846f5211586f038a14e89c2be387f8ebecf8fcac3da1ee330c9ea93d0a7c3dc4af350220d50080732e0809717ee6a053359e6a694ec2cb3f284a0a466c87a94d83b31093a67372e2f6412c06e6d42f15818dffe0381cc0cd444da6cddc3b82458194801b32564134fbfde98c9287748dbf5676a540d8154c8bbca07b9e247553311c46b9af76fdeeccc8e69e7c8a2d08e782620943f99727d3c04fe72991d99df9bae38a0b2177fa31d5b6afee91f020103a381fc3081f9301d0603551d0e04160414485900563d272c46ae118605a47419ac09ca8c113081c90603551d230481c13081be8014485900563d272c46ae118605a47419ac09ca8c11a1819aa48197308194310b3009060355040613025553311330110603550408130a43616c69666f726e6961311630140603550407130d4d6f756e7461696e20566965773110300e060355040a1307416e64726f69643110300e060355040b1307416e64726f69643110300e06035504031307416e64726f69643122302006092a864886f70d0109011613616e64726f696440616e64726f69642e636f6d820900936eacbe07f201df300c0603551d13040530030101ff300d06092a864886f70d010105050003820101007aaf968ceb50c441055118d0daabaf015b8a765a27a715a2c2b44f221415ffdace03095abfa42df70708726c2069e5c36eddae0400be29452c084bc27eb6a17eac9dbe182c204eb15311f455d824b656dbe4dc2240912d7586fe88951d01a8feb5ae5a4260535df83431052422468c36e22c2a5ef994d61dd7306ae4c9f6951ba3c12f1d1914ddc61f1a62da2df827f603fea5603b2c540dbd7c019c36bab29a4271c117df523cdbc5f3817a49e0efa60cbd7f74177e7a4f193d43f4220772666e4c4d83e1bd5a86087cf34f2dec21e245ca6c2bb016e683638050d2c430eea7c26a1c49d3760a58ab7f1a82cc938b4831384324bd0401fa12163a50570e684d'
    plain_text = src + '|' + timestamp + '|' + usertoken + '|' + uuid + '|' + '1' + '|' + version_name + '|' + version_a + '|' \
                 + hashlib.md5(postdata.encode(encoding='utf-8')).hexdigest() + '|' + hashlib.md5(signatures.encode(encoding='utf-8')).hexdigest()
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
    timestamp = str(int(time.time() * 1000))
    #source = '1000031'
    data = os_uuid + '|' + app_versionname + '|' + os_dim + '|' + os_version_1 + '|' + source + '|' \
           + os_android_version + '|' + '1' + '|' + os_device_type + '|' + app_versioncode + '|' + source + '|' + '4' \
           + '|' + app_usertoken + '|' + timestamp + '|' + '1' + '|' + os_qimei
    key = "0821CAAD409B8402"
    # print(data)
    QDInfo = JDClass.getQDInfo(data, key)
    return QDInfo

def captcha():
	return tcaptcha()



