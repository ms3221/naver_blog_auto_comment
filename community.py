from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
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


def get_gif_urls(url:str, messageList: list[str], title: str) -> list[str]:
    

    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1800,1000")
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        options.headless = True
        options.add_experimental_option("debuggerAddress", "localhost:9222")

        driver = webdriver.Chrome(options=options)

        driver.get('https://gall.dcinside.com/board/lists?id=sh_new')
        driver.maximize_window()
        # 일정 시간동안 대기 (예: 2초)
       
        time.sleep(5)

        write_btn = driver.find_element(By.CSS_SELECTOR, "#container > section.left_content > article:nth-child(3) > div.list_array_option.clear > div.right_box > div > div.switch_btnbox")
        write_btn.click()

        time.sleep(2)

        input_element = driver.find_element(By.CSS_SELECTOR, "#password")
        input_element.send_keys("1234")
        time.sleep(2)

        title_input = driver.find_element(By.CSS_SELECTOR, "#subject")
        title_input.send_keys(title)

        time.sleep(2)

        pyautogui.click(1298, 798)

        time.sleep(10)

        pyautogui.scroll(-10000)

        # iframe = driver.find_element(By.ID, "tx_canvas_wysiwyg")
        # driver.switch_to.frame(iframe)
        # iframe.click()

        
        script = """
var messageList = arguments[0];
messageList.forEach(function(text) {
    if (text === "") {
        // 빈 문자열일 경우 <br> 태그를 생성하여 문서에 추가합니다.
        var br = document.createElement('br');
        document.body.appendChild(br);
    } else {
        // 빈 문자열이 아닐 경우 <p> 태그를 생성하여 문서에 추가합니다.
        var p = document.createElement('p');
        p.textContent = text;
        document.body.appendChild(p);
    }
});
"""
        # driver.execute_script(script, messageList)
#         driver.switch_to.default_content()
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(10)

        # button = find_position_by_image("image/a.png")
        # pyautogui.moveTo(button["x"], button["y"], 1)
        pyautogui.click( 1298, 798)

      
        # save_btn = driver.find_element(By.CSS_SELECTOR, "#write > div.btn_box.write.fr > button.btn_blue.btn_svc.write")
        # driver.execute_script("arguments[0].click();", save_btn)
        

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
