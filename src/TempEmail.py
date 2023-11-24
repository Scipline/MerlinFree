from DrissionPage import ChromiumPage

# 创建页面对象，并启动或接管浏览器
page = ChromiumPage()
# 跳转到登录页面
page.get('https://www.linshiyouxiang.net/')

# 输入对文本框输入账号
# ele.input('您的账号')
# 定位到密码文本框并输入密码
page.ele('#active-mail').click()
page.get('https://app.getmerlin.in/register')
# # 点击登录按钮
# page.ele('@value=登 录').click()
