# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver
import time, json
from tkinter import messagebox

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import


def login():
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920x1080")

    driver = webdriver.Chrome()
    # 크롬 드라이버에 url 주소 넣고 실행
    driver.get("https://www.naver.com")

    # 페이지가 완전히 로딩되도록 3초동안 기다림
    time.sleep(20)
    driver.quit()


def site_login(id, pwd, message, excel_data):
    try:
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
        id_input.send_keys(id)

        pwd_input = driver.find_element(
            By.CSS_SELECTOR,
            "body > div.gpe_allcon_wrap0 > div > div.gpe_side_contents_R > div:nth-child(1) > div > div > div > form > fieldset > div.idpwWrap > span.idpw > input.idpw_pass",
        )
        pwd_input.send_keys(pwd)

        login_btn = driver.find_element(
            By.CSS_SELECTOR,
            "body > div.gpe_allcon_wrap0 > div > div.gpe_side_contents_R > div:nth-child(1) > div > div > div > form > fieldset > div.idpwWrap > span.loginbutton > input[type=submit]",
        )
        login_btn.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "body > div.gpe_allcon_wrap0 > div > div.gpe_side_contents_R > div:nth-child(1) > div > div > div > form > fieldset > div.userName > p > span:nth-child(3) > a",
                )
            )
        )

        for index, data in enumerate(excel_data[3:], start=1):
            [no, nickname, clock] = data
            try:
                driver.get("https://allin42.com/message/write")
                time.sleep(1)

                nickname_input = driver.find_element(
                    By.CSS_SELECTOR,
                    "body > div.gpe_allcon_wrap0 > div > div.gpe_contents_box > div > div > div > div.elasticsearch_section.elasticsearch_documents > div > form > div:nth-child(1) > ul > li > div > input",
                )

                nickname_input.send_keys(nickname)
                message_box = driver.find_element(
                    By.CSS_SELECTOR,
                    "body > div.gpe_allcon_wrap0 > div > div.gpe_contents_box > div > div > div > div.elasticsearch_section.elasticsearch_documents > div > form > div:nth-child(3) > textarea",
                )
                message_box.send_keys(message)
                write_btn = driver.find_element(
                    By.CSS_SELECTOR,
                    "body > div.gpe_allcon_wrap0 > div > div.gpe_contents_box > div > div > div > div.elasticsearch_section.elasticsearch_documents > div > form > div:nth-child(5) > ul > li.right > button",
                )
                write_btn.click()
                time.sleep(1)
                pyautogui.press("Enter")
                time.sleep(1)
                print(f"{nickname}에게 쪽지를 보냈습니다.")
            except Exception as e:
                if "차단" in str(e):
                    messagebox.showerror("메시지 실패", "차단된 회원입니다")
                    break
                print(e)
                print(f"어떤 이유로든지 {nickname}발송에 실패")

    except Exception as e:
        raise Exception("login 오류")

    finally:
        driver.quit()


def get_crawling_site(id, pwd, start, end):
    nickname_list = []
    options = webdriver.ChromeOptions()
    options.add_argument("window-size=1920x1080")

    driver = webdriver.Chrome()
    # 크롬 드라이버에 url 주소 넣고 실행
    driver.get("https://www.allin42.com/notice")
    driver.maximize_window()
    id_input = driver.find_element(
        By.CSS_SELECTOR,
        "body > div.gpe_allcon_wrap0 > div > div.gpe_side_contents_R > div:nth-child(1) > div > div > div > form > fieldset > div.idpwWrap > span.idpw > input[type=text]:nth-child(1)",
    )
    id_input.send_keys(id)

    pwd_input = driver.find_element(
        By.CSS_SELECTOR,
        "body > div.gpe_allcon_wrap0 > div > div.gpe_side_contents_R > div:nth-child(1) > div > div > div > form > fieldset > div.idpwWrap > span.idpw > input.idpw_pass",
    )
    pwd_input.send_keys(pwd)

    time.sleep(2)
    login_btn = driver.find_element(
        By.CSS_SELECTOR,
        "body > div.gpe_allcon_wrap0 > div > div.gpe_side_contents_R > div:nth-child(1) > div > div > div > form > fieldset > div.idpwWrap > span.loginbutton > input[type=submit]",
    )
    login_btn.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "body > div.gpe_allcon_wrap0 > div > div.gpe_side_contents_R > div:nth-child(1) > div > div > div > form > fieldset > div.userName > p > span:nth-child(3) > a",
            )
        )
    )
    print("login완료")
    for i in range(int(start), int(end) + 1):
        print(f"{i}페이지 수집을 시작합니다.")
        pange_no = i
        url = f"https://www.allin42.com/free?page={pange_no}"
        # 이것도 마찬가지인데 이동해서 수집하자
        # 꺼지고 키는건 상당한 리스크가 있다.

        try:
            driver.get(url)
            time.sleep(5)
            trs = driver.find_elements(
                By.CSS_SELECTOR, "#board_list > table > tbody > tr"
            )
            third_td_texts = [
                tr.find_element(By.CSS_SELECTOR, "td:nth-child(3) > a").text
                for tr in trs
            ]
            nickname_list += third_td_texts
            print(f"{i}페이지 수집이 끝났습니다.")

        except Exception as e:
            print(e)

    driver.quit()
    return nickname_list
