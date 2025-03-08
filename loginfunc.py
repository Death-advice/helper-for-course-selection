import requests
import execjs
from bs4 import BeautifulSoup

url = 'https://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fbkjw.chd.edu.cn%2Feams%2FstdElectCourse.action'
headers1 = {
    'Referer': 'https://ids.chd.edu.cn/authserver/login?service=http%3A%2F%2Fbkjw.chd.edu.cn%2Feams%2FstdElectCourse.action',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36'
}

def getexecution():
    session = requests.Session()
    response = session.post(url, headers=headers1)
    soup = BeautifulSoup(response.text, 'html.parser')
    execution = soup.find('input', {'name': 'execution'}).get('value')
    return execution

def getsaltvalue():
    session = requests.Session()
    response = session.post(url, headers=headers1)
    soup = BeautifulSoup(response.text, 'html.parser')
    pwdEncryptSalt = soup.find('input', {'id': 'pwdEncryptSalt'}).get('value')
    return pwdEncryptSalt

def getencryptpwd(password):
    with open('encryptpwd.js', 'r') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    encryptedPwd = ctx.call('getpwd', password, getsaltvalue())
    return encryptedPwd

def login(account,password):
    response1 = requests.get(url, headers=headers1)
    cookies = response1.cookies
    strs = str(requests.utils.dict_from_cookiejar(cookies))
    strs = strs[1:-1]
    for ch in strs:
        if ch == ':':
            strs = strs.replace(ch, '=')
        elif ch == '\'':
            strs = strs.replace(ch, '')
        elif ch == ',':
            strs = strs.replace(ch, ';')
    headers1['Cookie'] = strs + ';' + ' org.springframework.web.servlet.i18n.CookieLocaleResolver.LOCALE=zh_CN'
    data = {
        'username': account,
        'password': getencryptpwd(password),
        'captcha': '',
        '_eventId': 'submit',
        'cllt': 'userNameLogin',
        'dllt': 'generalLogin',
        'lt': '',
        'execution': getexecution(),
    }
    session2 = requests.Session()
    response = session2.post(url, headers=headers1, data=data, allow_redirects=True)
    return response.url

if __name__ == '__main__':
    print(login('',''))
