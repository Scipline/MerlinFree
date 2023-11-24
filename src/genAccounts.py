from DrissionPage import ChromiumPage

import random
import string
import time


def get_random_string(length=10):
    # 生成由大小写字母和数字构成的随机字符串
    letters = string.ascii_letters + string.digits
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


user = get_random_string()
passwd = "123456789"
password = "input#password"
# 创建页面对象，并启动或接管浏览器
page = ChromiumPage()
if page.tabs_count < 2:
    page.get(url='https://www.linshiyouxiang.net/')
page0 = page.tabs[-1]
page.to_tab(page0)
page.ele('@class:fa-random').click()


def get_email():
    email = page.ele('.form-control').attr('data-clipboard-text')
    if email:
        return email
    time.sleep(1)
    return get_email()


email = get_email()

page.to_tab(page.tabs[0], activate=True)
# 跳转到登录页面,主标签页仍然第一个，焦点改变为当前
if page.tabs_count < 2:
    page1 = page.new_tab(url='https://app.getmerlin.in/register', switch_to=True)
# 定位到密码文本框并输入密码
page.ele('#name').input(user)
page.ele('#password').input(passwd)
page.ele('#email').input(email)
page.ele('@@type=submit@@class:primary-btn').click()
page.ele('@@tag=h3@@class:res-large-text')
page.to_tab(page0)

def get_email_content():
    title = page.ele('@@tag=a@@class:title-subject').text()
    if title=='Verify your email for Merlin':
        return True
    time.sleep(1)
    return get_email_content()
get_email_content()
page.ele('@@tag=a@@class:title-subject').click()
# 等待新标签页出现
page.wait.new_tab()
# 获取新标签页对象
new_tab = page.get_tab(page.latest_tab)
# 等待新标签页加载
new_tab.wait.load_start()
print(new_tab)
