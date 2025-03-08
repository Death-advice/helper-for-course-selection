import requests
import execjs
from bs4 import BeautifulSoup

url = 'https://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fbkjw.chd.edu.cn%2Feams%2FstdElectCourse.action'
headers1 = {
    'Referer': 'https://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fbkjw.chd.edu.cn%2Feams%2FstdElectCourse.action',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}
#第一次访问获得Cookie
response1 = requests.get(url, headers=headers1)
cookies = response1.cookies
strs = str(requests.utils.dict_from_cookiejar(cookies))
strs=strs[1:-1]
for ch in strs:
    if ch==':':
        strs=strs.replace(ch,'=')
    elif ch=='\'':
        strs=strs.replace(ch,'')
    elif ch==',':
        strs=strs.replace(ch,';')
headers1['Cookie']=strs+';'+' org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN'

#获得表单数据中的execution
session=requests.Session()
response = session.post(url, headers=headers1)
soup=BeautifulSoup(response.text,'html.parser')
execution = soup.find('input', {'name': 'execution'}).get('value')

#获得加密密码的盐值
pwdEncryptSalt=soup.find('input', {'id': 'pwdEncryptSalt'}).get('value')

#调用js获得加密后的密码
account=input("Your account:")
password=input("Your password:")
with open('encryptpwd.js', 'r') as f:
    js_code=f.read()
ctx=execjs.compile(js_code)
encryptedPwd=ctx.call('getpwd',password,pwdEncryptSalt)

#创建表单数据
data = {
    'username':account,
    'password':encryptedPwd,
    'captcha':'',
    '_eventId':'submit',
    'cllt':'userNameLogin',
    'dllt':'generalLogin',
    'lt':'',
    'execution':execution,
}

#模拟发送请求
session2=requests.Session()
response = session2.post(url, headers=headers1, data=data, allow_redirects=True)

# 检查状态码
if response.status_code == 200:
    print("登录成功，当前 URL:", response.url)
else:
    print(f"登录失败，状态码:{response.status_code}，这可能是因为过于频繁登录系统导致需要输入验证码才能登陆。")

#选课地址：http://bkjw.chd.edu.cn/eams/stdElectCourse.action
#获取cookies
#登陆系统获取cookies

'''加密密码逻辑：
    在encrypt.js中含有加密算法，其中 funtion encryptPassword(n,f)最终返回的便是加密以后的密码
    n：账号密码（明码） f：id="pwdEncryptSalt" value="盐值"
    将对应参数输入后就可以得到加密后的密码
    '''