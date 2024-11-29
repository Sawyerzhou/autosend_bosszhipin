import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 实例化Chrome浏览器
wd = webdriver.Chrome()
# 设置隐性等待时间为10秒
wd.implicitly_wait(10)

# 打开Boss直聘登录页面
wd.get('https://www.zhipin.com/web/user/?ka=header-login')
# 点击同意用户使用条例
wd.find_element(By.CSS_SELECTOR, '*[type="checkbox"]').click()
# 点击扫码登录按钮
wd.find_element(By.CLASS_NAME, 'switch-tip').click()
# 等待用户扫码登录
time.sleep(10)

# 进入首页
wd.find_element(By.CSS_SELECTOR, 'a[ka="header-home"]').click()
# 输入搜索关键词"c++"并搜索
search_input = wd.find_element(By.CSS_SELECTOR, 'input[name="query"]')
search_input.clear()
search_input.send_keys('软件测试\n')

# 等待搜索结果加载
time.sleep(10)
var = 1
while var == 1:
    # 获取当前页面所有招聘对象
    jobs = wd.find_elements(By.CLASS_NAME, 'job-card-left')
    # 循环投递
    for job in jobs:
        # 保存默认窗口句柄
        default_window = wd.current_window_handle
        # 打开职位详情页
        job.click()
        # 跳转到新标签页
        wd.switch_to.window(wd.window_handles[-1])
        # 等待沟通按钮可见
        try:
            button = WebDriverWait(wd, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="btn btn-startchat"]'))
            )
            b_text = button.text
            # 岗位为未投递则进行投递
            if b_text == "立即沟通":
                button.click()
                # 等待关闭按钮可见
                try:
                    close_button = WebDriverWait(wd, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="icon-close"]'))
                    )
                    close_button.click()
                # 关闭按钮不可见
                except Exception as e:
                    print('close_button未找到', e)

                print(wd.title, "————投递完成")
                wd.close()
                # 确保在关闭窗口之前切换回默认窗口
                wd.switch_to.window(default_window)
            # 岗位已投递
            else:
                wd.close()
                # 确保在关闭窗口之前切换回默认窗口
                wd.switch_to.window(default_window)
        # 其他错误
        except Exception as e:
            print('未找到沟通按钮', e)
    # 切换下一页
    try:
        last_button = WebDriverWait(wd, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ui-icon-arrow-right'))
        )
        last_button.click()
    # 下一页按钮不可见
    except Exception as e:
        print('close_button未找到', e)
