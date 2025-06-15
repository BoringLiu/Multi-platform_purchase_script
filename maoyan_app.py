# -*- coding: UTF-8 -*-
"""
__Author__ = "WECENG"
__Version__ = "1.0.0"
__Description__ = "大麦app抢票自动化"
__Created__ = 2023/10/26 10:27
"""
import msvcrt
import threading

"""REMAKE
__Author__ = "LuMing"
__Version__ = "0.0.5"
__Description__ = "猫眼小程序抢票自动化到时点击"
__Created__ = 2025/6/15 19:32
"""
import sys
import time
from datetime import datetime, timedelta
from time import sleep

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from appium.webdriver.common.touch_action import TouchAction
# from appium.webdriver.common.touch_action import TouchAction
from config import Config

# 加载配置信息
config = Config.load_config()

device_app_info = AppiumOptions()
# 操作系统
device_app_info.set_capability('platformName', 'Android')
# 操作系统版本
device_app_info.set_capability('platformVersion', '14')
# 设备名称
device_app_info.set_capability('deviceName', 'd28c095a')
# app package
device_app_info.set_capability('appPackage', '')#可以加入猫眼，但是为了方便微信内用户，不做强制要求。
# app activity name
device_app_info.set_capability('appActivity', '.launcher.splash.SplashMainActivity')
# 使用unicode输入
device_app_info.set_capability('unicodeKeyboard', True)
# 隐藏键盘
device_app_info.set_capability('resetKeyboard', True)
# 不重置app
device_app_info.set_capability('noReset', True)
# 超时时间
device_app_info.set_capability('newCommandTimeout', 6000)
# 使用uiautomator2驱动
device_app_info.set_capability('automationName', 'UiAutomator2')

# 连接appium server，server地址查看appium启动信息
driver = webdriver.Remote('http://127.0.0.1:4723/wd/hub', options=device_app_info)

sleep(0.1)

# 设置等待时间，等待1s
driver.implicitly_wait(0.1)
# 空闲时间10ms,加速
driver.update_settings({"waitForIdleTimeout": 10})

users = config.users
auto_commit = config.if_commit_order

#X:777 Y:2275 coordinates
# =================== 参数 ===================
CLICK_X, CLICK_Y = 777, 2275          # 你的坐标
TARGET_TIME_STR = config.time  # 到此时间开始点
CLICK_INTERVAL = 0.01                 # 点一次休眠（秒）

# =================== 状态控制变量 ===================
pause_flag = threading.Event()        # True = 暂停
exit_flag  = threading.Event()        # True = 退出
pause_flag.clear()                    # 默认不暂停

# ------------------- 键盘监听线程 -------------------
def keyboard_listener():
    print("\n=== 操作说明 ===")
    print("  p : 暂停 / 继续")
    print("  q : 退出脚本\n")
    while not exit_flag.is_set():
        if msvcrt.kbhit():
            key = msvcrt.getch().lower()
            if key == b'p':
                if pause_flag.is_set():
                    pause_flag.clear()
                    print("[键盘] ▶️ 继续点击")
                else:
                    pause_flag.set()
                    print("[键盘] ⏸ 已暂停点击")
            elif key == b'q':
                exit_flag.set()
                print("[键盘] ❌ 收到退出指令")
        time.sleep(0.05)

threading.Thread(target=keyboard_listener, daemon=True).start()

# =================== 等待目标时间 ===================
target_time_only = datetime.strptime(TARGET_TIME_STR, "%H:%M:%S").time()
# 用今天的日期 + 时间，得到完整的目标 datetime
target_time = datetime.combine(datetime.today(), target_time_only)
print(f"🎯 目标时间：{target_time}")
while datetime.now() < target_time and not exit_flag.is_set():
    time.sleep(0.1)
print("⌚ 已到目标时间，开始点击！")

# =================== 无限点击循环 ===================
while not exit_flag.is_set():
    if pause_flag.is_set():
        time.sleep(0.05)
        continue

    try:
        driver.tap([(CLICK_X, CLICK_Y)])
    except Exception as e:
        # Appium 有时会抛 socket 读写错误，忽略重试
        print(f"Tap 异常: {e}")

    time.sleep(CLICK_INTERVAL)

# =================== 收尾 ===================
print("🛑 脚本退出，关闭 driver")
driver.quit()
sys.exit(0)


























