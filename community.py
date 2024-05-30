from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time, os, sys, cv2
import pyautogui

import numpy as np

current_directory = os.path.dirname(os.path.abspath(__file__))


def get_absolute_path(file_path):
    return os.path.join(current_directory, file_path)


def change_path(img_path):
    n = np.fromfile(get_absolute_path(img_path), np.uint8)
    return [cv2.imdecode(n, cv2.IMREAD_GRAYSCALE), img_path]


def find_position_by_image(img_path, max_attempts=10):
    print(img_path, "1")
    [byte_path, img_path] = img_path
    print(byte_path)

    current_attempt = 0

    # 대기 시간 설정 (초)
    wait_time = 2

    while current_attempt < max_attempts:
        print(current_attempt)
        try:
            print(img_path)
            # 이미지를 찾고    좌표를 가져옵니다.
            button_png = pyautogui.locateOnScreen(
                image=img_path, grayscale=True, confidence=0.8
            )
            # button_png = pyautogui.locateOnScreen(img_path, region=(2000, 0, 500, 500), grayscale=True)
            print(f"button_png::{button_png}")
            print("이미지를 찾았습니다. 좌표:", button_png)
            center_position = pyautogui.center(button_png)
            return {"x": center_position.x, "y": center_position.y}
        except pyautogui.ImageNotFoundException as e:
            print(e)
            print(f"{img_path}의 이미지를 찾을 수 없습니다. 대기 후 다시 시도합니다.")
            time.sleep(wait_time)
            current_attempt += 1

    # 반복이 끝나고도 이미지를 찾지 못한 경우

    print("지정된 횟수 내에 이미지를 찾지 못했습니다.")


def get_gif_urls() -> list[str]:
    print("here ")

    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1800,1000")
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        driver = webdriver.Chrome(options=options)

        driver.get("https://gall.dcinside.com/board/write/?id=sh_new")
        driver.maximize_window()
        # 일정 시간동안 대기 (예: 2초)
        time.sleep(5)

        input_element = driver.find_element(By.CSS_SELECTOR, "#password")
        input_element.send_keys("1234")
        time.sleep(5)

        title_input = driver.find_element(By.CSS_SELECTOR, "#subject")
        title_input.send_keys("이거 맞나?")

        time.sleep(5)

        iframe = driver.find_element(By.ID, "tx_canvas_wysiwyg")
        driver.switch_to.frame(iframe)
        texts = [
            "❤️첫충전 입금 PLUS❤️",
            "5+2 10+3 20+4 or 10%",
            "📌 스포츠 / 미니게임 / 카지노 (미니게임 다수보유)",
            "📌스포츠.카지노.미니게임 롤링 100% 입니다",
            "📌1회 최대환전 4000만원",
            "📌1시간 텀으로 환전가능 합니다",
            "📌블랙승인ok",
            "📌환전사고 절대 X / 승전 x",
            "📌-실시간연승 이벤트/게시판 작성 이벤트/출석 이벤트/다폴더 이벤트/삼치기 연승 이벤트",
            "📌-루틴.마틴.양빵.밸런스o/찍먹o/삼치기o/충환전 5분컷",
            "",
            "✅-롤링-✅",
            "[스포츠.카지노.미니게임  롤링100%]첫충시: 스포츠100%/ 미니게임.카지노300%",
            "",
            "가입문의",
            "@ssrr119",
        ]
        script = """
var texts = arguments[0];
texts.forEach(function(text) {
    var p = document.createElement('p');
    p.textContent = text;
    document.body.appendChild(p);
});
"""
        driver.execute_script(script, texts)
        driver.switch_to.default_content()
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

        button = find_position_by_image(change_path("image/submit.png"))
        pyautogui.moveTo(button["x"], button["y"], 1)
        pyautogui.click(button["x"], button["y"])
        time.sleep(3)

        # 4가지 행동을 해야함

        # 1. 비밀번호 입력

        # 2. 제목 입력

        # 3. 내용 입력

        # 4. 확인 버튼 클릭
        print(1)
    except Exception as e:
        print(e)
    finally:
        driver.quit()


if __name__ == "__main__":
    get_gif_urls()
