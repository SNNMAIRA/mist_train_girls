from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import json
import time
import numpy as np
import cv2 as cv
import os
import requests
import urllib3
import sys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
s = requests.Session()
proxies = {
  "http": "http://127.0.0.1:7890",
  "https": "http://127.0.0.1:7890",
  "ftp": "ftp://127.0.0.1:7890"
}


def checktime(sec):
    if time.time()-start_time > sec:
        sys.exit()


def now_cards(cards):
    now_cardlist = []
    for i in range(5):
        now_cardlist.append(cards[i*2:i*2+2])
    return now_cardlist


def sort_cards(cardlist):
    cards = cardlist.copy()
    for i in range(5):
        if(cards[i][1]) == "X":
            cards[i] = cards[i][:-1]
            cards[i] = cards[i] + "10"
        if(cards[i][1]) == "J":
            cards[i] = cards[i][:-1]
            cards[i] = cards[i] + "11"
        if(cards[i][1]) == "Q":
            cards[i] = cards[i][:-1]
            cards[i] = cards[i] + "12"
        if(cards[i][1]) == "K":
            cards[i] = cards[i][:-1]
            cards[i] = cards[i] + "13"
    for i in range(5):
        for j in range(i+1):
            if(int(cards[j][1:]) > int(cards[i][1:])):
                temp = cards[i]
                cards[i] = cards[j]
                cards[j] = temp
    print("SORTED", cards)
    return cards


def suit_count(sorted_cardlist):
    {0: 'O', 1: 'S', 2: 'D', 3: 'H', 4: 'C'}

    suit_list = [0, 0, 0, 0, 0]
    for i in range(5):
        if(sorted_cardlist[i][0] == "S"):
            suit_list[1] = suit_list[1] + 1
        if(sorted_cardlist[i][0] == "D"):
            suit_list[2] = suit_list[2] + 1
        if(sorted_cardlist[i][0] == "H"):
            suit_list[3] = suit_list[3] + 1
        if(sorted_cardlist[i][0] == "C"):
            suit_list[4] = suit_list[4] + 1
        if(sorted_cardlist[i][0] == "$"):
            suit_list[0] = suit_list[0] + 1
    # 返回最大相同花色數量 和最大花色類型
    return max(suit_list) + suit_list[0], suit_list.index(max(suit_list))


def number_count(sorted_cardlist):
    number_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for i in range(5):
        number_list[int(sorted_cardlist[i][1:])] = number_list[int(sorted_cardlist[i][1:])] + 1
    # 返回最大相同數字數量
    return max(number_list) + number_list[0], number_list.index(max(number_list))


def straight_count(sorted_cardlist):
    # 啊懶得寫了 是順子就返回5 不是就返回0
    straight = 0
    if(int(sorted_cardlist[0][1:]) != 0):
        if(int(sorted_cardlist[0][1:])+4 == int(sorted_cardlist[1][1:])+3 == int(sorted_cardlist[2][1:])+2 == int(sorted_cardlist[3][1:])+1 == int(sorted_cardlist[4][1:])):
            straight = 5
    else:
        if((int(sorted_cardlist[4][1:]) - int(sorted_cardlist[1][1:]) <= 4)):
            straight = 5
    # 返回最大連續數字數量
    return straight


def execute_suit(original_cardlist, max_suit_color):
    dict = {0: 'O', 1: 'S', 2: 'D', 3: 'H', 4: 'C'}
    change_list = []
    for i in range(5):
        if(original_cardlist[i][0] != dict[max_suit_color] and original_cardlist[i][0] != '$'):
            change_list.append(i)
    return change_list


def execute_number(original_cardlist, max_number_digital):
    dict1 = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'X', 11: 'J', 12: 'Q', 13: 'K'}
    dict2 = {'0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0, 'X': 0, 'J': 0, 'Q': 0, 'K': 0}
    change_list = []
    for i in range(5):
        dict2[original_cardlist[i][1]] = dict2[original_cardlist[i][1]] + 1
    for i in range(1, 13):
        if(dict2[dict1[i]] < 2):
            for j in range(5):
                if(dict1[i] == original_cardlist[j][1]):
                    change_list.append(j)
    return change_list


def execute_straight(original_cardlist):
    change_list = []
    return change_list


def execute_single(original_cardlist):
    change_list = []
    for i in range(5):
        if(original_cardlist[i][0] != "$"):
            change_list.append(i)
    return change_list


def get_login(url):
    checktime(120)
    # 當前時間超過起始時間60秒就退出 ~~但看代碼應該不可能會有超過60秒的情況~~
    try:
        driver.delete_all_cookies()
        time.sleep(1)
        # 清除所有cookies再打開url
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginbutton_script_on"]/span/input')))
        time.sleep(1)
        # 如果cookie目錄下沒有對應郵箱地址的txt文件
        driver.find_element(By.ID, 'login_id').send_keys("braveteen@outlook.com")
        driver.find_element(By.ID, "password").send_keys("10252000LZZLZZ")
        driver.find_element(By.XPATH, '//*[@id="loginbutton_script_on"]/span/input').click()
        time.sleep(1)
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ntgnavi-item')))
        print("login success")
        time.sleep(1)
    except Exception:
        time.sleep(1)
        print('getlogin again Error:')
        # 除了cookies加不进的错误和最开始的动态网页加载10秒钟找不到抛出异常之外 其他情况下应该都不需要重新登陆吧
        get_login(url)


# 这里这个函数可能是写Bug了 本意可能是前十条读取不到就再get一次
def get_makeRequest(count=0):
    # 还是同一个邮箱所以起始时间还是一样 所以这里再多六十秒加到了一百二十秒
    checktime(200)
    # 读取出所有发送过的请求
    allrequest = driver.requests
    # 查找所有request中是否有对'https://osapi.dmm.com/gadgets/makeRequest'发起 同时有返回的request
    for i in allrequest:
        if i.url == 'https://osapi.dmm.com/gadgets/makeRequest':
            if i.response is not None:
                # 返回的i就是第一个对request发起 同时有返回内容的request
                return i
    # for-else语法 for的循环执行完成的时候 再去执行else的语句
    else:
        # 如果执行到了这里 就意味着for循环没有找出合适的request
        time.sleep(2)
        count += 1
        if count > 10:
            del driver.requests
            driver.get('https://pc-play.games.dmm.co.jp/play/MistTrainGirlsX/')
        # 这里直接再调用了一次get_makeRequest() 尝试再driver在读取一次符合条件的request
        return get_makeRequest(count)


def post_req(url):
    try:
        time.sleep(0.5)
        # 不知道這個c_url是啥 也許是current url 後面加上了當前時間
        # 這裏設置了path參數 但並不是每個請求都需要用到 
        headers['Referer'] = 'https://assets.mist-train-girls.com/'
        # 這個token是全局變量
        headers['Authorization'] = "Bearer "+token
        # Referer 请求头包含了当前请求页面的来源页面的地址，即表示当前页面是通过此来源页面里的链接进入的。
        headers['Origin'] = 'https://assets.mist-train-girls.com'
        try:
            headers.pop('Content-type')
        except Exception:
            pass
        r = s.post(url, headers=headers, verify=False, proxies=proxies)
        if(r.status_code == 200):
            body = json.loads(r.content)
            # 如果沒有錯誤 就把獲取到的JSON格式數據返回 注意到是body全部返回而不是只返回data
            return body
        else:
            print('post_req error: ', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
    except Exception:
        time.sleep(3)
        print('post_req again:', url)
        # 除了cookies加不进的错误忽略之外 其他情况下应该都会重新登陆吧
        post_req(url)


def post_jsonstring(url, json_string):
    try:
        time.sleep(0.5)
        # 不知道這個c_url是啥 也許是current url 後面加上了當前時間
        # 這裏設置了path參數 但並不是每個請求都需要用到 
        headers['Referer'] = 'https://assets.mist-train-girls.com/'
        # 這個token是全局變量
        headers['Authorization'] = "Bearer "+token
        # Referer 请求头包含了当前请求页面的来源页面的地址，即表示当前页面是通过此来源页面里的链接进入的。
        headers['Origin'] = 'https://assets.mist-train-girls.com'
        headers['Content-type'] = r'application/json'
        r = s.post(url, headers=headers, verify=False, proxies=proxies, json=json_string)
        if(r.status_code == 200):
            body = json.loads(r.content)
            # 如果沒有錯誤 就把獲取到的JSON格式數據返回 注意到是body全部返回而不是只返回data
            return body
        else:
            print('post_jsonstring json error: ', end=" ")
            print(r.status_code, url)
            # raise Exception("訪問失敗")
    except Exception:
        time.sleep(3)
        print('post_jsonstring again:', url)
        # 除了cookies加不进的错误忽略之外 其他情况下应该都会重新登陆吧
        post_jsonstring(url, json_string)


def get_req(url):
    try:
        time.sleep(0.5)
        # 不知道這個c_url是啥 也許是current url 後面加上了當前時間
        # 這裏設置了path參數 但並不是每個請求都需要用到 
        headers['Referer'] = 'https://assets.mist-train-girls.com/'
        # 這個token是全局變量
        headers['Authorization'] = "Bearer "+token
        # Referer 请求头包含了当前请求页面的来源页面的地址，即表示当前页面是通过此来源页面里的链接进入的。
        headers['Origin'] = 'https://assets.mist-train-girls.com'
        try:
            headers.pop('Content-type')
        except Exception:
            pass
        r = s.get(url, headers=headers, verify=False, proxies=proxies)
        if(r.status_code == 200):
            body = json.loads(r.content)
            # 如果沒有錯誤 就把獲取到的JSON格式數據返回 注意到是body全部返回而不是只返回data
            return body
        else:
            print('get_req error:', end=" ")
            print(r.status_code, url)
            raise Exception("訪問失敗")
    except Exception:
        time.sleep(3)
        print('get_req again:', url)
        # 除了cookies加不进的错误忽略之外 其他情况下应该都会重新登陆吧
        get_req(url)


# 從這裏開始執行
# DesiredCapabilities 快速初始化浏览器参数
capa = DesiredCapabilities.CHROME
# 浏览器不会等待资源的加载
capa["pageLoadStrategy"] = "none"
options = webdriver.ChromeOptions()
options.add_argument('--mute-audio')
# 禁用信息欄
options.add_argument("disable-infobars")
# 禁用拓展
options.add_argument("--disable-extensions")
# 使用 /tmp 而非 /dev/shm 作為暫存區 在某些VM环境中，/dev/shm分区太小，导致Chrome发生故障或崩溃（请参阅）。 使用此标志解决此问题（临时目录将始终用于创建匿名共享内存文件）。
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
# 無頭模式 是無界面的的狀態
options.add_argument("--headless")
# 禁用圖形 但有headless这个可能没必要
options.add_argument("--disable-gpu")
# 禁用光柵化
options.add_argument("--disable-software-rasterizer")
# 忽視證書錯誤
options.add_argument('--ignore-certificate-errors')
# close the notifiction of automatic test
options.add_experimental_option("excludeSwitches", ['enable-automation'])
# 不知道为啥要设置快取
# options.add_argument('--disk-cache-dir=D:\\Program Files\\Python\\browser document\\chrome user data\\User Data\\Default\\Cache')
options.add_argument(r"user-data-dir=C:\Users\admin\AppData\Local\Google\Chrome\User Data")
seleniumwire_options = {
        'proxy': {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
            'ftp': 'http://127.0.0.1:7890',
            'snmp': 'http://127.0.0.1:7890',
            'tftp': 'http://127.0.0.1:7890',
            'pop3': 'http://127.0.0.1:7890'
        }
        # 'proxy': {
        #     'http': 'http://127.0.0.1:8888',
        #     'https': 'http://127.0.0.1:8888',
        #     'ftp': 'http://127.0.0.1:8888',
        #     'snmp': 'http://127.0.0.1:8888',
        #     'tftp': 'http://127.0.0.1:8888',
        #     'pop3': 'http://127.0.0.1:8888'
        # }
    }


driver = webdriver.Chrome(options=options, desired_capabilities=capa, seleniumwire_options=seleniumwire_options)
# 原来无头模式也需要设置窗口大小吗...
driver.set_window_size(1200, 900)
driver.set_window_position(0, 0)

# 這裏暫時沒用上 但之後會在函數里被修改
headers = {
    'host': r"mist-production-api-001.mist-train-girls.com",
    'accept': r'*/*',
    'accept-encoding': 'gzip, deflate, br',
    'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    # 虽然我浏览器的默认语言是英语
    'accept-language': 'zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': r'https://assets.mist-train-girls.com/',
    # 原来`是转义字符的意思
    'sec-ch-ua': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': r'Windows',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-site',
}
# 設置了起始時間就是當前時間 之後函數判斷超時會用
start_time = time.time()

# 从这里开始真正执行
get_login('https://pc-play.games.dmm.co.jp/play/MistTrainGirlsX/')
my_request = get_makeRequest()
token = str(my_request.response.body).split(r'{\\"r\\":\\"')[1].split(r'\\",\\"t\\":null')[0]
print("token is = ", token)
del driver.requests
get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Users/Me")
get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Users/MyPreferences")
post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Login")
# print(login_status['r']['ConvertGachaMedalResult']['ResultMistPeiceQuantity'])
get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Home")
# true表示禮物有時間限制

get_req(r"https://mist-production-api-001.mist-train-girls.com/api/UGiftBoxes/true")

def casio_poker():
    current_casio_status = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/GetCasinoTop")
    if(current_casio_status['r']["TodayCasinoCoinStatus"]["IsLockCoin"] is not False):
        file.write('今天贏麻了')
        sys.exit(0)
    bet_begin = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/Bet?type=2&betCoin=5000")
    original_cardlist = now_cards(str(bet_begin['r']))
    file.write(str(original_cardlist)+'起始手牌 \n')
    sorted_cardlist = sort_cards(original_cardlist)

    max_suit_count, max_suit_color = suit_count(sorted_cardlist)
    max_number_count, max_number_digital = number_count(sorted_cardlist)
    max_straight_count = straight_count(sorted_cardlist)
    discard_list = []
    if(max_suit_count == 5):
        discard_list = execute_suit(original_cardlist, max_suit_color)
    elif(max_straight_count == 5):
        discard_list = execute_straight(original_cardlist)
    elif(max_number_count >= 3):
        discard_list = execute_number(original_cardlist, max_number_digital)
    elif(max_suit_count == 4):
        discard_list = execute_suit(original_cardlist, max_suit_color)
    elif(max_number_count == 2):
        discard_list = execute_number(original_cardlist, max_number_digital)
    else:
        discard_list = execute_single(original_cardlist)

    poker_url = "https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/ChangeHand"
    if (len(discard_list) != 0):
        poker_url = "https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/ChangeHand?"
    for i in range(len(discard_list)):
        poker_url = poker_url + "&changeIndexes={}".format(discard_list[i])
    changed_cards_result = post_req(poker_url)
    file.write(str(now_cards(str(changed_cards_result['r']["Cards"])))+'改良手牌 \n')

    # 如果是上一次換牌后中了
    dict = {'0': 0, '1': 14, 'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'X': 10, 'J': 11, 'Q': 12, 'K': 13}
    if(changed_cards_result['r']['RewardCoinCount'] != 0):
        reward_coin = 5000
        guess_card = dict[post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/DoubleUp/Start")['r'][1]]
        while (reward_coin != 0):
            file.write(str(guess_card)+'猜測的牌 \n')
            if(guess_card <= 8):
                guess_result = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/DoubleUp/Choose?choice=1")
            else:
                guess_result = post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/Poker/DoubleUp/Choose?choice=2")
            if(int(guess_result['r']["RewardCoinCount"]) > 0 and int(guess_result['r']["RewardCoinCount"]) < 1000000):
                guess_card = dict[guess_result['r']["DrawCard"][1]]
            elif(int(guess_result['r']["RewardCoinCount"]) > 1000000):
                file.write(str(int(guess_result['r']["RewardCoinCount"]))+'贏得賭幣 \n')
                reward_coin = 0
            else:
                reward_coin = 0
        current_casio_status = get_req(r"https://mist-production-api-001.mist-train-girls.com/api/Casino/GetCasinoTop")
        if(current_casio_status['r']["TodayCasinoCoinStatus"]["IsLockCoin"] is False):
            casio_poker()
        else:
            # casio_poker()
            file.write('今天贏麻了')
            sys.exit(0)
    else:
        casio_poker()


file = open("./casino_log.txt", 'a')
# casio_poker()
# print(login_status['r']['ConvertGachaMedalResult']['ResultMistPeiceQuantity'])


result = post_jsonstring(r"https://mist-production-api-001.mist-train-girls.com/api/Battle/surrender",
                         r'''{"BattleAutoSetting":3,"BattleSpeed":2,"BattleSpecialSkillAnimation":0,"IsAutoSpecialSkill":false,"IsAutoOverDrive":false,"EnableConnect":false}"''')
print(post_req(r"https://mist-production-api-001.mist-train-girls.com/api/Training/updateCheckPoint")['r']['TrainingInfoEnergyLeft'])
time.sleep(180)
