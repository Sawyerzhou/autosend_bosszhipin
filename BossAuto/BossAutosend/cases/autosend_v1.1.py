from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import random

# 实例化Chrome浏览器
wd = webdriver.Chrome()
# 设置隐性等待时间为10秒
wd.implicitly_wait(10)


# 创建时停
def random_sleep(min_seconds, max_seconds):
    time.sleep(random.uniform(min_seconds, max_seconds))


# 打开Boss直聘登录页面
wd.get('https://www.zhipin.com/web/user/?ka=header-login')
# 点击同意用户使用条例
clickable = wd.find_element(By.CSS_SELECTOR, '*[type="checkbox"]')
ActionChains(wd).click(clickable).perform()
# 点击扫码登录按钮
clickable = wd.find_element(By.CLASS_NAME, 'switch-tip')
ActionChains(wd).click(clickable).perform()
# 等待用户扫码登录
wait = WebDriverWait(wd, 15).until(
    EC.text_to_be_present_in_element_attribute((
        By.CSS_SELECTOR, '[title=BOSS直聘]'
    ), 'title', 'BOSS直聘')
)
print("登录成功")

# 进入首页
hoverable = WebDriverWait(wd, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR,
                                'a[ka="header-home"]'))
)
ActionChains(wd).move_to_element(hoverable).perform()
ActionChains(wd).click(hoverable).perform()
print("进入首页")


def send_k():
    a = input()
    return a + "\n"


# 搜索岗位名称
i = 1
while i:
    try:
        search_input = WebDriverWait(wd, 10).until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, 'input[name="query"]'))
        )
        ActionChains(wd).move_to_element(search_input).perform()
        search_input.clear()
        ActionChains(wd).click(search_input).perform()
        ActionChains(wd).send_keys('自动化测试\n').perform()
        print("搜索成功")
        i = 0
    except Exception as e:
        i = 1
        print(e)

random_sleep(2, 5)

i = 1
while i:
    try:
        # 等待搜索结果加载
        WebDriverWait(wd, 10).until(EC.text_to_be_present_in_element_attribute((
            By.CSS_SELECTOR, 'li[class=active]'), 'class', 'active')
        )
        print("搜索加载完成")
        i = 0
    except Exception as e:
        i = 1
        print(e)

var = 1
while var == 1:
    # 获取当前页面所有招聘对象
    jobs = wd.find_elements(By.CLASS_NAME, 'job-card-left')
    # 循环投递
    for job in jobs:
        # 保存默认窗口句柄
        default_window = wd.current_window_handle
        # 打开职位详情页
        ActionChains(wd).move_to_element(job).perform()
        ActionChains(wd).click(job).perform()
        # 跳转到新标签页
        wd.switch_to.window(wd.window_handles[-1])
        random_sleep(1, 3)
        # 等待沟通按钮可见
        try:
            button = WebDriverWait(wd, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[class="btn btn-startchat"]'))
            )
            b_text = button.text
            # 判断岗位是否已投递
            if b_text == "立即沟通":
                ActionChains(wd).move_to_element(button).perform()
                ActionChains(wd).click(button).perform()
                random_sleep(1, 3)
                # 等待关闭按钮可见
                try:
                    close_button = WebDriverWait(wd, 10).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, '[class="icon-close"]'))
                    )
                    ActionChains(wd).move_to_element(close_button).perform()
                    ActionChains(wd).click(close_button).perform()
                    var = 1
                    random_sleep(1, 4)
                # 关闭按钮不可见
                except Exception as e:
                    print('close_button未找到', e)
                    var = 1

                print(wd.title, "————投递完成")
                random_sleep(1, 3)
                # 返回原标签页
                wd.close()
                wd.switch_to.window(default_window)
            # 岗位已投递
            elif b_text == "继续沟通":
                print('岗位已投递')
                # 返回原标签页
                wd.close()
                wd.switch_to.window(default_window)
        # 其他错误
        except Exception as e:
            print('未找到沟通按钮', e)
            var = 1
    # 切换下一页
    try:
        last_button = WebDriverWait(wd, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'ui-icon-arrow-right'))
        )
        ActionChains(wd).move_to_element(last_button).perform()
        ActionChains(wd).click(last_button).perform()
        WebDriverWait(wd, 10).until(EC.text_to_be_present_in_element_attribute((
            By.CSS_SELECTOR, 'li[class=active]'), 'class', 'active')
        )
        var = 1
        random_sleep(2, 5)
    # 下一页按钮不可见
    except Exception as e:
        print('close_button未找到', e)
        var = 1
