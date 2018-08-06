import http.cookiejar 
import urllib.request
cookie = http.cookiejar.CookieJar()
handle = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handle)
response = opener.open('https://www.baidu.com')
for item in cookie:
    print(item.name + '=' + item.value)
