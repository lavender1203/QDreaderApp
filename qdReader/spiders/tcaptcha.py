#!/usr/bin/env python
# coding=utf-8
import time
import os
import webbrowser
#web测试
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# 鼠标操作
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.common.keys import Keys
# 等待时间 产生随机数
import time
import random
from selenium.webdriver import DesiredCapabilities
from .download import download_image_as_jpeg
from .get_distance import get_pos1

#appid = '1600000770'
width = '140'
height = '140'
map = ''
captcha = {
    'sig': "",
    'code': ""
}
# 20分钟内只能连续3次
def tcaptcha(appid='1600000770'):
    start = time.time()
    libpath = os.path.dirname(os.path.abspath(__file__)) + '/../..' + "/libs/"
    img_dir = os.path.dirname(os.path.abspath(__file__)) + '/../..' + "/img/"
    url = 'file://' + libpath + 'tcaptcha_webview.html' + '?appid=' + appid + '&width=' + width + '&height=' + height + '&map=' + map
    from fake_useragent import UserAgent
    ua = UserAgent()
    #ua.update()
    user_agent = ua.random
    #QDInfo = getQDInfo()
    options = Options()
    options.add_argument('--headless')
    options.add_experimental_option('w3c', False)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--disable-web-security')
    options.add_argument("--touch-events")
    # options.add_argument('auto-open-devtools-for-tabs')
    options.add_argument('X-Requested-With="com.qidian.QDReader"')
    import requests
    #proxy = requests.get("http://127.0.0.1:5010/get/").json()['proxy']
    #proxy = requests.get('http://ip.ipjldl.com/index.php/api/entry?method=proxyServer.hdtiqu_api_url&packid=7&fa=1&groupid=0&fetch_key=&time=6&qty=1&port=1&format=json&ss=5&css=&dt=&pro=&city=&usertype=4')
    #if proxy.json()['code'] == 0:
    #    ip = proxy.json()['data'][0]['IP']
    #    port = proxy.json()['data'][0]['Port']
    #proxy = '14.155.112.17:9000'
    #    options.add_argument('--proxy-server=' + str(ip) + ":" + str(port))
    options.add_argument('user-agent=' + user_agent)
    #mobile_emulation = {"deviceMetrics": {"width": 1080, "height": 1920, "pixelRatio": 3.0}, "userAgent": user_agent}
    #options.add_experimental_option("mobileEmulation", mobile_emulation)
    options.add_experimental_option('prefs', {'profile.default_content_settings.popups': 0,'intl.accept_languages': 'zh-CN,en-US;q=0.8'})
    driver = webdriver.Chrome(executable_path="/usr/bin/chromedriver", chrome_options=options)
    #driver.maximize_window()
    timeArray = time.localtime(time.time() - start)
    timeStr = time.strftime("%S", timeArray)
    #print("selenium初始化耗时：" + timeStr + "s")
    #driver.get("http://ssl.captcha.qq.com:443")
    #time.sleep(3)
    #code = driver.find_element_by_xpath('//h1').text
    #if code != '400 Bad Request':
    #    captcha['sig'] = "" 
    #    captcha['code'] = ""
    #    driver.close()
    #    return captcha
    # print(driver.get_cookies())
    #driver.add_cookie({'name': 'ywkey', 'value': ''})
    #driver.add_cookie({'name': 'ywguid', 'value': ''})
    #driver.add_cookie({'name': 'QDInfo', 'value': QDInfo})
    flag = time.time()
    driver.get(url)
    timeArray = time.localtime(time.time() - start)
    timeStr = time.strftime("%S", timeArray)
    #print("selenium http get耗时：" + timeStr + "s")
    # print(driver.get_cookies())
    captcha['sig'] = driver.execute_script('return localStorage.getItem("sig")')
    captcha['code'] = driver.execute_script('return localStorage.getItem("code")')
    # 因为QQ登录是在一个框架中又有一个框架
    # 所以需要先进框架, 再定位节点元素
    el_frame = None
    max_count = 3
    count = 0
    while (captcha['sig'] == "" or captcha['code'] == "" or captcha['sig'] == None or captcha['code'] == None) and count < max_count:
        count = count + 1
        time.sleep(1)
        # 2. 通过节点定位   如果登录成功就不需要往下。。。
        if el_frame is None:
            driver.switch_to.default_content()
            try:
                WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "tcaptcha_iframe")))
                #el_frame = driver.find_element_by_xpath('//*[@id="tcaptcha_iframe"]')
                el_frame = driver.find_element_by_id("tcaptcha_iframe")
            except Exception as e:
                print(e)
            driver.switch_to.frame(el_frame)
        try:
            #WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "slideBg")))
            bg = driver.find_element_by_id('slideBg')
        except Exception as e:
            #time.sleep(60)
            captcha['sig'] = driver.execute_script('return localStorage.getItem("ticket")')
            captcha['code'] = driver.execute_script('return localStorage.getItem("randstr")')
            if captcha['sig'] is not None:
                print("滑块验证成功")
                pass
            else:
                print("网络错误")
            driver.close()
            end = time.time()
            timeArray = time.localtime(end -start)
            timeStr = time.strftime("%S", timeArray)
            print("本次验证总耗时：" + timeStr + "s")
            return captcha
        #print("第"+ str(count)+ "次尝试...")
        bg_location = bg.location
        bg_size = bg.size
        src = bg.get_attribute('src')
        gap_pic = 'gap' + str(time.time() * 1000) + '.jpeg'
        if src is None:
            print("验证码图片链接获取失败")
            driver.close()
            return captcha
        download_image_as_jpeg(src, img_dir + gap_pic)
        timeArray = time.localtime(time.time() - start)
        timeStr = time.strftime("%S", timeArray)
        #print("到下载验证码图耗时：" + timeStr + "s")
        # 获取拖拽的圆球
        #WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "tcaptcha_drag_button")))
        slide_block = driver.find_element_by_id('tcaptcha_drag_button') #for chromium
        if slide_block is None:
            print("slide_block 不存在.")
        # 生成拖拽移动轨迹，加3是为了模拟滑过缺口位置后返回缺口的情况
        loc = 0
        #WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "slideBlock")))
        bk = driver.find_element_by_id('slideBlock')
        bk_location = bk.location
        bk_size = bk.size
        bk_left = bk_location['x'] - bg_location['x']        #滑块初始化位置
        while bk_left < 26: #滑块初始化位置一般为26
            time.sleep(0.1)
            bk_left = bk.location['x'] - bg.location['x']        #滑块初始化位置
        ActionChains(driver).click_and_hold(slide_block).perform()
        w = driver.find_element_by_id('slideBg').size['width']
        h = driver.find_element_by_id('slideBg').size['height']
        try:
            flag = time.time()
            y = get_pos1(img_dir + gap_pic)
            timeArray = time.localtime(time.time() - flag)
            timeStr = time.strftime("%S", timeArray)
            #print("获取滑动距离图像处理耗时：" + timeStr + "s")
            if y == 0:
                continue
                print("图像处理获取滑动距离失败.")
            else:
                left = bk_left + int(bk_size['width']/2)
                loc = int(y/2) - left# 原图大小和显示大小比例2:1
               # print('滑块初始化的几何中心位置横坐标：' + str(bk_left))
                #print('滑块需要滑动的距离为:' + str(loc))
        except Exception as e:
            print(e)
        track_list = get_track(loc)
        # 根据轨迹拖拽圆球
        flag = time.time()
        for track in track_list:
             ActionChains(driver).move_by_offset(xoffset=track, yoffset=0).perform()
        ActionChains(driver).pause(random.randint(6, 14) / 10).release(slide_block).perform()
        timeArray = time.localtime(time.time() - start)
        timeStr = time.strftime("%S", timeArray)
        #print("到滑动滑块结束耗时：" + timeStr + "s")
    driver.close()
    return captcha

def get_track7(distance):
    """
    根据偏移量和手动操作模拟计算移动轨迹
    :param distance: 偏移量
    :return: 移动轨迹
    """
    # 移动轨迹
    tracks = []
    # 当前位移
    current = 0
    # 减速阈值
    mid = distance * 4 / 5
    # 时间间隔
    t = 0.2
    # 初始速度
    v = 0

    while current < distance:
        if current < mid:
            a = random.uniform(2, 5)
        else:
            a = -(random.uniform(12.5, 13.5))
        v0 = v
        v = v0 + a * t
        x = v0 * t + 1 / 2 * a * t * t
        current += x

        if 0.6 < current - distance < 1:
            x = x - 0.53
            tracks.append(round(x, 2))

        elif 1 < current - distance < 1.5:
            x = x - 1.4
            tracks.append(round(x, 2))
        elif 1.5 < current - distance < 3:
            x = x - 1.8
            tracks.append(round(x, 2))

        else:
            tracks.append(round(x, 2))

    #print(sum(tracks))
    return tracks

# 滑块移动轨迹
def get_track(distance):
    track = []
    current = 0
    mid = distance*3/4
    t = random.randint(2, 3)/10
    v = 0
    while current < distance:
        if current < mid:
            a = 10
        else:
            a = -3
        v0 = v
        v = v0+a*t
        move = v0*t+1/2*a*t*t
        current += move
        track.append(round(move))
    return track
