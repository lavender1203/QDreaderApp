import random

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os
from qdReader.spiders import download
from qdReader.spiders import get_distance


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

    print(sum(tracks))
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
            a = 25
        else:
            a = -3
        v0 = v
        v = v0+a*t
        move = v0*t+1/2*a*t*t
        current += move
        track.append(round(move))
    return track

def move_slider(driver, track_list):
    bk = driver.find_element_by_id("tcaptcha_drag_button")
    actions = ActionChains(driver)
    actions.click_and_hold(bk).perform()
    for track in track_list:
        print("track:" + str(track))
        actions.move_by_offset(xoffset=track, yoffset=0).perform()
    if bk is not None:
        actions.pause(random.randint(6, 14) / 10).release(bk).perform()

def test_start():
    url = "https://007.qq.com/online.html?ADTAG=capt.slide"
    driver = webdriver.Chrome()
    driver.set_window_size(1024, 768)
    driver.implicitly_wait(10)
    driver.get(url)
    element = driver.find_element_by_css_selector("a[data-type='1']")
    element.click()
    time.sleep(2)
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "code")))
    element = driver.find_element_by_id("code")
    element.click()

    # 1. 切换到验证码窗口 获取图片和滑块信息
    # time.sleep(5)
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "tcaptcha_iframe")))
    driver.switch_to.frame("tcaptcha_iframe")
    WebDriverWait(driver, 5, 0.5).until(EC.presence_of_element_located((By.ID, "slideBg")))
    bg = driver.find_element_by_id('slideBg')
    src = bg.get_attribute('src')
    if src is None:
        time.sleep(2)
        src = bg.get_attribute('src')
    if src is None:
        time.sleep(2)
        src = bg.get_attribute('src')
    print(src)
    # 2. 获取图片
    img_path = os.path.dirname(os.path.abspath(__file__)) \
               + "/img/" + str(int(time.time())) + ".jpeg"
    if src is not None:
        download.download_image_as_jpeg(src, img_path)
        # 3. 获取移动距离
        bk = driver.find_element_by_id('slideBlock')
        bk_location = bk.location
        bg_location = bg.location
        bk_size = bk.size
        bk_left = bk_location['x'] - bg_location['x']
        distance = get_distance.get_pos1(img_path)
        print("distance:" + str(distance))
        left = bk_left + int(bk_size['width']/2)
        offset = int(distance / 2) - left
        print("offset:" + str(offset))
        # 4. 生产移动轨迹
        track_list = get_track(offset)
        # 5. 模拟滑块滑动
        # bk = driver.find_element_by_id("tcaptcha_drag_button")
        # actions = ActionChains(driver)
        # actions.click_and_hold(bk).perform()
        # actions.move_by_offset(xoffset=offset, yoffset=0).perform()
        # actions.pause(1).release(bk).perform()
        move_slider(driver, track_list)
    time.sleep(2)
    driver.close()

if __name__ == "__main__":
    test_start()
