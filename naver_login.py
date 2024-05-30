# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time, json
import pyautogui
import pyperclip
import os, sys
import re

current_directory = os.path.dirname(os.path.abspath(__file__))


def get_absolute_path(file_path):
    return os.path.join(current_directory, file_path)


def site_login():
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920x1080")

    driver = webdriver.Chrome()
    # 크롬 드라이버에 url 주소 넣고 실행
    driver.get("https://www.allin42.com/notice")
    driver.maximize_window()
    # 페이지가 완전히 로딩되도록 3초동안 기다림

    id_input = driver.find_element(
        By.CSS_SELECTOR,
        "body > div.gpe_allcon_wrap0 > div > div.gpe_side_contents_R > div:nth-child(1) > div > div > div > form > fieldset > div.idpwWrap > span.idpw > input[type=text]:nth-child(1)",
    )
    id_put.cli
    time.sleep(20)

    _cookies = driver.get_cookies()
    with open(get_absolute_path("cookies.json"), "w") as file:
        json.dump(_cookies, file)
    # cookie_dict = {}
    # for cookie in _cookies:
    #     cookie_dict[cookie['name']] = cookie['value']
    # print(cookie_dict)

    driver.quit()


def auto_blog_comment(blogUrl: str, comment="blog 잘보고 갑니다."):
    blog_no = blogUrl.split("/")[-1]
    print(blog_no)
    options = webdriver.ChromeOptions()
    options.add_argument("disable-blink-features=AutomationControlled")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
    )

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=options)

    cookies_file_path = get_absolute_path("cookies.json")
    with open(cookies_file_path, "r") as cookies_file:
        cookies = json.load(cookies_file)

    driver.get("https://naver.com/")
    driver.maximize_window()
    # 키를 하나씩 추가하기 전에 'sameSite' 속성 확인 및 수정
    for cookie in cookies:
        if "sameSite" in cookie and cookie["sameSite"] not in ["Strict", "Lax", "None"]:
            cookie["sameSite"] = "None"
        driver.add_cookie(cookie)

    driver.refresh()
    driver.get(blogUrl)
    time.sleep(3)

    try:
        driver.switch_to.frame("mainFrame")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-1000)")
        time.sleep(3)
        driver.execute_script("window.scrollTo(0,200)")
        time.sleep(3)
        driver.find_element(
            By.XPATH, '//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div[2]'
        ).click()
        driver.find_element(
            By.XPATH, '//*[@id="printPost1"]/tbody/tr/td[2]/div[3]/div[1]/div[2]'
        ).click()

        time.sleep(2)
        driver.find_element(
            By.XPATH,
            f'//*[@id="naverComment_201_{blog_no}"]/div/div[5]/div[1]/form/fieldset/div/div/div[2]/div/label',
        ).click()
        time.sleep(2)
        pyperclip.copy(comment)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(2)
        driver.find_element(
            By.XPATH,
            f'//*[@id="naverComment_201_{blog_no}"]/div/div[5]/div[1]/form/fieldset/div/div/div[6]/button',
        ).click()
        time.sleep(2)

    except Exception as e:
        print(e)
    time.sleep(3)
    driver.quit()
