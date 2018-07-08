# import re
# from urllib import request
#
# response = request.urlopen("https://car.autohome.com.cn/price/brand-15.html")
# html = response.read().decode("gb18030")
# url = re.findall('href="//(k.autohome.com.cn/[\w\W]+?)"', html)[0: 10]
# for line in url:
#     response1 = request.urlopen("https://" + line)
#     html1 = response1.read().decode("gb18030")
#     urls1 = re.findall(
#         "href=\"//k.autohome.com.cn/detail/view_[\w\W]+?\"",
#         html1
#     )
#     for url1 in urls1:
#         print(url1)
#     break
# from tkinter import font
#
# str1 = '''<div class="dianPing clearfix" id="table_text_10448">
#
#
#
#
# 									<div class="conLit youdian"><b>'''
#
# print(re.findall('class="dianPing[\w\W]+?>([\w\W]+?)</div', str1))
