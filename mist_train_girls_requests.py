import time
import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
  "ftp": "ftp://127.0.0.1:7890"
}
headers = {
    'host': r"mist-production-api-001.mist-train-girls.com",
    'accept': r'*/*',
    'accept-encoding': 'gzip, deflate, br',
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    # 虽然我浏览器的默认语言是英语
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    # 原来`是转义字符的意思
    'sec-ch-ua': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': r'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
}


def post_req(url, token, count=0):
    if(count >= 10):
        raise Exception("post_req_fall")
    try:
        time.sleep(0.5)
        # 不知道這個c_url是啥 也許是current url 後面加上了當前時間
        # 這裏設置了path參數 但並不是每個請求都需要用到
        headers['Referer'] = 'https://assets.mist-train-girls.com/'
        # 這個token是全局變量
        headers['Authorization'] = "Bearer "+token
        # Referer 请求头包含了当前请求页面的来源页面的地址，即表示当前页面是通过此来源页面里的链接进入的。
        headers['Origin'] = 'https://assets.mist-train-girls.com'
        r = requests.post(url, headers=headers, verify=False, proxies=proxies)
        if(r.status_code == 200):
            body = json.loads(r.content)
            # 如果沒有錯誤 就把獲取到的JSON格式數據返回 注意到是body全部返回而不是只返回data
            return body
        elif(r.status_code == 401):
            # badrequst错误 和认证无效错误 立刻停止尝试产生异常
            count = 10
            print('post_req error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
        elif(r.status_code == 400):
            # badrequst错误 和认证无效错误 立刻停止尝试产生异常
            count = 10
            print('post_req error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
        else:
            print('post_req error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
    except Exception:
        time.sleep(3)
        print('post_req again:', url)
        # 除了cookies加不进的错误忽略之外 其他情况下应该都会重新登陆吧
        return post_req(url, token, count=count+1)


def post_jsonstring(url, token, json_string, count=0):
    if(count >= 10):
        raise Exception("post_jsonstring_fall")
    try:
        time.sleep(0.5)
        # 不知道這個c_url是啥 也許是current url 後面加上了當前時間
        # 這裏設置了path參數 但並不是每個請求都需要用到
        headers['Referer'] = 'https://assets.mist-train-girls.com/'
        # 這個token是全局變量
        headers['Authorization'] = "Bearer "+token
        # Referer 请求头包含了当前请求页面的来源页面的地址，即表示当前页面是通过此来源页面里的链接进入的。
        headers['Origin'] = 'https://assets.mist-train-girls.com'
        headers['Content-Type'] = r'application/json'
        # headers['Content-Length'] = r'2'
        r = requests.post(url, headers=headers, verify=False, proxies=proxies, data=json_string)
        if(r.status_code == 200):
            body = json.loads(r.content)
            # 如果沒有錯誤 就把獲取到的JSON格式數據返回 注意到是body全部返回而不是只返回data
            return body
        elif(r.status_code == 401):
            # badrequst错误 和认证无效错误 立刻停止尝试产生异常
            count = 10
            print('post_jsonstring json error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
        elif(r.status_code == 400):
            # badrequst错误 和认证无效错误 立刻停止尝试产生异常
            count = 10
            print('post_jsonstring json error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
        else:
            print('post_jsonstring json error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
    except Exception:
        time.sleep(3)
        print('post_jsonstring again:', url)
        # 除了cookies加不进的错误忽略之外 其他情况下应该都会重新登陆吧
        return post_jsonstring(url, token, json_string, count=count+1)


def get_req(url, token, count=0):
    if(count >= 10):
        raise Exception("get_req_fall")
    try:
        time.sleep(0.5)
        # 不知道這個c_url是啥 也許是current url 後面加上了當前時間
        # 這裏設置了path參數 但並不是每個請求都需要用到
        headers['Referer'] = 'https://assets.mist-train-girls.com/'
        # 這個token是全局變量
        headers['Authorization'] = "Bearer "+token
        # Referer 请求头包含了当前请求页面的来源页面的地址，即表示当前页面是通过此来源页面里的链接进入的。
        headers['Origin'] = 'https://assets.mist-train-girls.com'
        r = requests.get(url, headers=headers, verify=False, proxies=proxies)
        if(r.status_code == 200):
            body = json.loads(r.content)
            # 如果沒有錯誤 就把獲取到的JSON格式數據返回 注意到是body全部返回而不是只返回data
            return body
        elif(r.status_code == 401):
            # badrequst错误 和认证无效错误 立刻停止尝试产生异常
            count = 10
            print('get_req error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
        elif(r.status_code == 400):
            # badrequst错误 和认证无效错误 立刻停止尝试产生异常
            count = 10
            print('get_req error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
        else:
            print('get_req error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
    except Exception:
        time.sleep(3)
        print('get_req again:', url)
        # 除了cookies加不进的错误忽略之外 其他情况下应该都会重新登陆吧
        return get_req(url, token, count=count+1)
