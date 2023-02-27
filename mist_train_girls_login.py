from seleniumwire import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

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
# DesiredCapabilities 快速初始化浏览器参数
capa = DesiredCapabilities.CHROME
# 浏览器不会等待资源的加载
capa["pageLoadStrategy"] = "none"
options = webdriver.ChromeOptions()
# options.add_argument('--disk-cache-dir=D:\\Program Files\\Python\\browser document\\chrome user data\\User Data\\Default\\Cache')
# 设置用户文件路径
options.add_argument(r"user-data-dir=C:\Users\admin\AppData\Local\Google\Chrome\User Data")
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
driver = webdriver.Chrome(options=options, desired_capabilities=capa, seleniumwire_options=seleniumwire_options)
# 原来无头模式也需要设置窗口大小吗...
driver.set_window_size(1200, 900)
driver.set_window_position(0, 0)
start_time = time.time()


def checktime(sec):
    if time.time()-start_time > sec:
        raise Exception("password_login or get_makeRequest fall")


def password_login(url, user_name, password):
    checktime(80)
    # 當前時間超過起始時間60秒就退出 ~~但看代碼應該不可能會有超過60秒的情況~~
    try:
        driver.delete_all_cookies()
        time.sleep(1)
        # 清除所有cookies再打開url
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginbutton_script_on"]/span/input')))
        time.sleep(1)
        # 如果cookie目錄下沒有對應郵箱地址的txt文件
        driver.find_element(By.ID, 'login_id').send_keys(user_name)
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.XPATH, '//*[@id="loginbutton_script_on"]/span/input').click()
        time.sleep(1)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'ntgnavi-item')))
        print("DMM login success")
        time.sleep(10)
    except Exception:
        time.sleep(1)
        print('getlogin error, going to try again')
        # 除了cookies加不进的错误和最开始的动态网页加载10秒钟找不到抛出异常之外 其他情况下应该都不需要重新登陆吧
        password_login(url, user_name, password)


def get_makeRequest(count=0):
    # 还是同一个邮箱所以起始时间还是一样 所以这里再多六十秒加到了一百二十秒
    checktime(110)
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
        print("extract token error times", count)
        if count > 2:
            del driver.requests
            driver.get('https://pc-play.games.dmm.co.jp/play/MistTrainGirlsX/')
            time.sleep(10)
        # 这里直接再调用了一次get_makeRequest() 尝试再driver在读取一次符合条件的request
        return get_makeRequest(count)


def get_mist_trains_girls_token(user_name, password):
    password_login('https://pc-play.games.dmm.co.jp/play/MistTrainGirlsX/', user_name, password)
    my_request = get_makeRequest()
    token = str(my_request.response.body).split(r'{\\"r\\":\\"')[1].split(r'\\",\\"t\\":null')[0]
    print("token is :", token)
    return token
