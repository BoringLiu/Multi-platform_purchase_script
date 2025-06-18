# -*- coding: UTF-8 -*-
"""
__Author__ = "WECENG"
__Version__ = "1.0.0"
__Description__ = "大麦app抢票自动化"
__Created__ = 2023/10/26 10:27
"""
"""REMAKE
__Author__ = "LuMing"
__Version__ = "0.0.5"
__Description__ = "大麦app抢票自动化"
__Created__ = 2025/6/15 19:32
"""
import sys
from datetime import datetime, time
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
device_app_info.set_capability('appPackage', 'cn.damai')
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

# while True:
#     driver.swipe(500, 400, 500, 2000, 300)
#     sleep(0.1)
# words = config.keyword
# time_str = config.time  # "15:29:00"
# now_date = datetime.now()
# today_str = now_date.strftime("%Y-%m-%d")  # 当前年月日
# target_time = datetime.strptime(f"{today_str} {time_str}", "%Y-%m-%d %H:%M:%S")
# print(f"等待抢票时间：{target_time}")
# while True:
#         now = datetime.now()
#         if now >= target_time:
#             break
#         else:
#             driver.swipe(500, 400, 500, 2000, 300)
#             sleep(0.1)  # 控制刷新频率，防止刷新太快
#
# buy_btn = driver.find_element(by=By.XPATH,value='//android.widget.FrameLayout[@resource-id="cn.damai:id/trade_project_detail_purchase_status_bar_container_fl"]')
# buy_btn.click()

users = config.users
auto_commit = config.if_commit_order

print("等待你手动完成日期和票档选择...")

while True:
    try:
        # ======= 确认按钮是否激活 =======
        confirm_btn = driver.find_element(By.XPATH, '//android.widget.LinearLayout[@resource-id="cn.damai:id/btn_buy_view"][@index="0"]')

        # 读取当前票数
        ticket_text = driver.find_element(By.ID, "cn.damai:id/tv_num").text  # 比如 "2张"
        ticket_count = int(ticket_text.replace("张", ""))

        # 目标张数来自 config.json 中的用户人数
        target_count = len(users)

        # 自动点击加号按钮直到达到目标数量
        while ticket_count < target_count:
            driver.find_element(By.ID, "cn.damai:id/img_jia").click()
            ticket_text = driver.find_element(By.ID, "cn.damai:id/tv_num").text
            ticket_count = int(ticket_text.replace("张", ""))

        # ======= 点击确认 =======
        confirm_btn.click()
        print("已点击确认购票")

        # # 点击确认后检测是否进入了只有继续尝试的页面（可能是“重新尝试”）努力刷新页面如果返回到票价重新点击确定的操作循环。
        # try:
        #     only_continue_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("努力刷新")')
        #     if only_continue_btn.is_displayed():
        #         only_continue_btn.click()
        #         print("⚠️ 出现了‘努力刷新’页面，已点击一次准备返回")
        #         # 再次回到票价页面，重新点击确认按钮
        #         confirm_btn = driver.find_element(By.XPATH,
        #                                           '//android.widget.LinearLayout[@resource-id="cn.damai:id/btn_buy_view"][@index="0"]')
        #         confirm_btn.click()
        #         print("🔁 回到票价页面并重新点击了确认按钮")
        # except Exception:
        #     pass  # 如果不是这个页面，正常继续执行

        #循环点击努力刷新直至进入购票人页面并拿到购票人卡片
        while True:
            try:
                recycler = driver.find_element(AppiumBy.ID, "cn.damai:id/recycler_main")
                print("✅ 购票人列表已加载")
                break  # 找到recycler了，跳出循环
            except :
                # 没找到recycler，检测是否有继续尝试按钮
                try:
                    refresh_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                       'new UiSelector().text("努力刷新")')
                    if refresh_btn.is_displayed() and refresh_btn.is_enabled():
                        refresh_btn.click()
                        print("点击了努力刷新按钮")
                        time.sleep(0.05)  # 小等待避免过快
                        try:
                            confirm_btn = driver.find_element(By.XPATH, '//android.widget.LinearLayout[@resource-id="cn.damai:id/btn_buy_view"][@index="0"]')
                            if confirm_btn.is_displayed() and confirm_btn.is_enabled():
                                confirm_btn.click()
                                print("点击了确定按钮")
                        except :
                            print("未找到确定按钮")
                    else:
                        print("努力刷新按钮不可用，继续等待")
                except :
                    print("努力刷新按钮不存在，继续等待")

        # 获取所有购票人卡片
        # Step 1: 拿到 RecyclerView
        # recycler = driver.find_element(AppiumBy.ID, "cn.damai:id/recycler_main")
        # recycler = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((AppiumBy.ID, "cn.damai:id/recycler_main"))
        # )
        # print("✅ 购票人列表已加载")

        # Step 2: 拿到所有购票人 ViewGroup（注意：再用 ID 会重复混淆）
        user_cards = recycler.find_elements(AppiumBy.CLASS_NAME, "android.view.ViewGroup")
        print(f"找到 {len(user_cards)} 个购票人卡片")

        # Step 3: 遍历每个卡片，取出 text_name 内容
        target_names = config.users
        checked_count = 0
        for card in user_cards:
            try:
                name_element = card.find_element(AppiumBy.ID, "cn.damai:id/text_name")
                name = name_element.text
                print(f"找到购票人: {name}")

                if name in target_names:
                    checkbox = card.find_element(AppiumBy.ID, "cn.damai:id/checkbox")
                    if not checkbox.get_attribute("checked") == "true":
                        checkbox.click()
                        print(f"勾选了购票人: {name}")
                        checked_count += 1
                    else:
                        print(f"已勾选: {name}")
                        checked_count += 1
            except Exception as e:
                print(f"解析购票人卡片失败: {e}")
        # 提交订单

        ############################################
        if checked_count > 0:
            print("✅ 所有购票人已勾选，准备提交")
            pay_detect_count = 0  # 初始化锁计数器
            PAY_DETECT_THRESHOLD = 3  # 连续检测到3次再确认进入支付页面

            while True:

                # ✅检测是否进入支付页面
                try:
                    pay_hint = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                                                   'new UiSelector().textContains("请输入支付密码")')
                    if pay_hint.is_displayed():
                        pay_detect_count += 1
                        print(f"检测到支付提示（第{pay_detect_count}次）")
                        if pay_detect_count >= PAY_DETECT_THRESHOLD:
                            print("🎉 成功稳定进入支付页面，抢票完成！")
                            driver.save_screenshot("支付成功页面.png")
                            driver.quit()
                            sys.exit(0)
                    else:
                        pay_detect_count = 0  # 如果一帧未检测到就重置
                except Exception as e:
                        # 排除 SystemExit, KeyboardInterrupt
                    import sys

                    if isinstance(e, (SystemExit, KeyboardInterrupt)):
                        raise
                    pay_detect_count = 0

                try:
                    submit_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("立即提交")')
                    submit_btn.click()
                    print("✅ 已点击立即提交")

                    # 等待弹窗出现
                    # sleep(0.03)  # 等待弹窗稳定

                    # 判断弹窗按钮
                    try:
                        # continue_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                        #                                    'new UiSelector().text("继续尝试")')
                        #
                        # if continue_btn.is_displayed() and continue_btn.is_enabled():
                        #     print(f"找到继续尝试按钮，位置：{continue_btn.location}, 大小：{continue_btn.size}")
                        #     continue_btn.click()
                        #     print("🔄 点击‘继续尝试’，继续留在购票人页面重新提交")
                        #     sleep(0.03)
                        #     continue  # 继续循环，重新点击立即提交
                        wait = WebDriverWait(driver, 1)  # 最多等1秒即可
                        retry_btn = wait.until(
                            EC.element_to_be_clickable((AppiumBy.ID, "cn.damai:id/damai_theme_dialog_confirm_btn"))
                        )
                        print("找到 ‘继续尝试’ 按钮，点击！")
                        retry_btn.click()
                        touch_tap(driver, retry_btn)
                        # TouchAction(driver).tap(retry_btn).perform()
                        # sleep(0.03)
                        continue  # 回到抢票循环
                    except:
                        print("未找到‘继续尝试’按钮")

                    # try:
                    #     cancel_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR,
                    #                                      'new UiSelector().text("返回重新选购")')
                    #     if cancel_btn.is_displayed():
                    #         print("⚠️ 出现‘返回重新选购’，票已售罄或不可购买，跳出循环")
                    #         break  # 退出循环，可能回到选票价页重新操作
                    # except:
                    #     print("未找到‘返回重新选购’按钮")

                    # print("未检测到继续尝试或返回重新选购按钮，退出提交循环")
                    # break


                except Exception as e:

                    import sys

                    if isinstance(e, (SystemExit, KeyboardInterrupt)):
                        raise

                    print(f"点击立即提交异常：{e}")
        ########################################################
        # 3. 检查是否全部成功勾选   == len(target_names)
        # if checked_count > 0 :
        #     print("✅ 所有购票人已勾选，准备提交")
        #     # 4. 点击立即提交
        #     try:
        #         submit_btn = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("立即提交")')
        #         submit_btn.click()
        #         print("✅ 已点击立即提交")
        #         driver.quit()
        #         print("✅ 驱动已关闭。")
        #         sys.exit(0)
        #     except Exception as e:
        #         print(f"❌ 未找到立即提交按钮: {e}")

        # if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR,
        #                         value='new UiSelector().text("提交订单")') and config.if_commit_order:
        #        driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("提交订单")').click()

    except Exception as e:
        print(f"未准备好，继续等待中...（{e}）")
        sleep(0.1)



























# #############################################################################################
# # 点击搜索框
# # driver.find_element(by=By.ID, value='homepage_header_search_btn').click()
#
# ############################################################
# # 点击搜索框
# search_box = driver.find_element(AppiumBy.ID, "cn.damai:id/channel_search_text")
# search_box.click()
#
# # 等待搜索框弹出后，输入关键词（如果有独立输入框的话）
# # 假设输入框的id是 cn.damai:id/search_src_text （示例，需要确认）
# input_box = driver.find_element(AppiumBy.ID, "cn.damai:id/header_search_v2_input")
# input_box.send_keys(config.keyword)
#
# driver.press_keycode(66)
# driver.press_keycode(66)
# # driver.find_element(by=By.ID, value='homepage_header_search_btn').click()
# #######################################################################
#
#
# # # 输入搜索关键词
# # driver.find_element(by=By.ID, value='header_search_v2_input').send_keys(config.keyword)
# # 点击第一个搜索结果
# # driver.find_element(by=By.XPATH,
# #                     value='//androidx.recyclerview.widget.RecyclerView[@resource-id="cn.damai:id/search_v2_suggest_recycler"]/android.widget.RelativeLayout[1]').click()
# ########点击目标城市窗口
# # city = config.city
# # element = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, f'new UiSelector().textContains("{city}")')
# # element.click()
# # 点击结果列表的第一个
# driver.find_element(by=By.XPATH,
#                     value='(//android.widget.LinearLayout[@resource-id="cn.damai:id/ll_search_item"])[1]').click()
#
# # if driver.find_elements(by=By.XPATH,
# #                         value='//android.widget.FrameLayout[@resource-id="cn.damai:id/trade_project_detail_purchase_status_bar_container_fl"]'):
# #     # 城市选择
# #     for city in driver.find_elements(by=By.ID, value='tv_tour_city'):
# #         if config.city in city.text:
# #             city.click()
# #             break
# #     # 日期选择
# #     for date in driver.find_elements(by=By.ID, value='tv_tour_time'):
# #         if config.date in date.text:
# #             date.click()
# #             break
# ####################################
#
# ####################################
#
# while driver.find_elements(by=By.XPATH,
#                            value='//android.widget.FrameLayout[@resource-id="cn.damai:id/trade_project_detail_purchase_status_bar_container_fl"]'):
#     buy_btn = driver.find_element(by=By.XPATH,
#                                   value='//android.widget.TextView[@resource-id="cn.damai:id/tv_left_main_text"]').text
#     if buy_btn == '立即预定':
#         # 点击立即购买
#         driver.find_element(by=By.XPATH,
#                             value='//android.widget.FrameLayout[@resource-id="cn.damai:id/trade_project_detail_purchase_status_bar_container_fl"]/android.widget.LinearLayout').click()
#         # 票价选择
#         if driver.find_elements(by=By.ID, value='project_detail_perform_price_flowlayout'):
#             for price in driver.find_elements(by=By.XPATH,
#                                               value='//android.widget.TextView[@resource-id="cn.damai:id/item_text"]'):
#                 if config.price in price.text:
#                     price.click()
#         # 数量选择
#         if driver.find_elements(by=By.ID, value='layout_num') and config.users is not None:
#             for i in range(len(config.users) - 1):
#                 driver.find_element(by=By.ID, value='img_jia').click()
#         # 确认
#         if driver.find_elements(by=By.ID, value='btn_buy'):
#             driver.find_element(by=By.ID, value='btn_buy').click()
#         # 选择人员
#         if driver.find_elements(by=By.ID, value='recycler_main') and config.users is not None:
#             identity_elements = driver.find_elements(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("身份证")')
#             parent_elements = [element.parent for element in identity_elements]
#             for user in config.users:
#                 for user_element in parent_elements:
#                     user_select_list = user_element.find_elements(AppiumBy.ANDROID_UIAUTOMATOR,
#                                                                   'new UiSelector().textContains("' + str(user) + '")')
#                     for user_select in user_select_list:
#                         user_select.click()
#                         break
#                     break
#         # 提交订单
#         if driver.find_elements(by=AppiumBy.ANDROID_UIAUTOMATOR,
#                                 value='new UiSelector().text("提交订单")') and config.if_commit_order:
#             driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value='new UiSelector().text("提交订单")').click()
#     if buy_btn == '预约抢票':
#         # 预约购票
#         driver.find_element(by=By.XPATH,
#                             value='//android.widget.FrameLayout[@resource-id="cn.damai:id/trade_project_detail_purchase_status_bar_container_fl"]/android.widget.LinearLayout').click()
#
#         # 日期选择
#         if driver.find_elements(by=By.ID, value='project_detail_perform_flowlayout'):
#             for date in driver.find_elements(by=By.XPATH,
#                                               value='//android.widget.TextView[@resource-id="cn.damai:id/item_text"]'):
#                 if config.date in date.text:
#                     date.click()
#                     break
#
#         # 票价选择
#         if driver.find_elements(by=By.ID, value='project_detail_perform_price_flowlayout'):
#             for price in driver.find_elements(by=By.XPATH,
#                                               value='//android.widget.TextView[@resource-id="cn.damai:id/item_text"]'):
#                 if config.price in price.text:
#                     price.click()
#                     break
#         # 提交
#         if driver.find_elements(by=By.ID, value='btn_buy_bottom_div_line'):
#             driver.find_element(by=By.XPATH,
#                                 value='//android.view.View[@resource-id="cn.damai:id/btn_buy_bottom_div_line"]/..').click()
#     if buy_btn == '已预约':
#         break
#     else:
#         # 模拟下拉刷新
#         driver.swipe(500, 400, 500, 2000, 300)
#         sleep(0.1)
#
# driver.quit()
