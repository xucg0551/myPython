import hashlib

def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()

def get_cookie(cookie_str):
    cookie_dict = {}
    items = cookie_str.split(';')
    for item in items:
        key = item.split('=')[0].replace(' ', '')
        value = item.split('=')[1]
        cookie_dict[key] = value
    return cookie_dict



if __name__ == '__main__':
    print(get_md5('http://www.baidu.com'))