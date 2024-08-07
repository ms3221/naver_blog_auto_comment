from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time, os, sys, cv2
import pyautogui
import pyclip

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


def get_gif_urls( message:str, title: str) -> list[str]:
    
    idList = ["m_entertainer_new1","ib_new2","baseball_new11","binsenjo","stream_new1","leagueoflegends6","grsgills"]
   
    try:
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1800,1000")
        options.add_argument("disable-blink-features=AutomationControlled")
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )
        options.add_argument('--log-level=3') 
        options.headless = True
        #options.add_experimental_option("debuggerAddress", "localhost:9222")

        driver = webdriver.Chrome(options=options)
        for index, id in enumerate(idList):
            driver.get(f'https://gall.dcinside.com/board/write?id={id}')
            driver.maximize_window()
            # 일정 시간동안 대기 (예: 2초)
            pyclip.copy(message)

        

        
            # 사용 가능한 write 갤러리인지 확인이 필요 
            # 처음 인자를 찾지못하면 못찾는 걸로 인지해서 종료 
            try:
                input_element = driver.find_element(By.CSS_SELECTOR, "#password")
                input_element.send_keys("1234")
                print("비밀번호 입력 완료")
                time.sleep(2)

            except Exception as e:
                print(f"https://gall.dcinside.com/board/write?id={id}", "사용가능한 싸이트인지 확인이 필요합니다.")
                print("==================================================")
                return
            
            
            
            try:
                title_input = driver.find_element(By.CSS_SELECTOR, "#subject")
                title_input.send_keys(title)
                print("제목 입력 완료")
                time.sleep(2)

            except Exception as e:
                print("제목을 입력하지 못했습니다.")
                print("==================================================")
                return
        
            

            

            pyautogui.scroll(-10000)
            
            
            try:
                iframe = driver.find_element(By.ID, "tx_canvas_wysiwyg")
                driver.switch_to.frame(iframe)
                body = driver.find_element(By.CSS_SELECTOR,"body")
                body.click()
                time.sleep(1)
                pyautogui.hotkey("ctrl","v")
                time.sleep(2)
                print("본문 입력 완료")
            except Exception as e:
                print("ifrmae 혹은 다른이유로 본문에 작성에 문제가 생겼습니다.")
                print("==================================================")
                return

        
            
            pyautogui.moveTo(2121, 1473,3)
            pyautogui.click( 2121, 1473)
        
            
            
            
            
            #작성이 완료되었으면 list에서 가져오는 작업이 필요 
            try:
                write_no = ""
                wait = WebDriverWait(driver, 10)
                
                
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child(6) > td.gall_num')))
                for i in range(20):
                    try:
                        write_title = driver.find_element(By.CSS_SELECTOR,f"#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child({i}) > td.gall_tit.ub-word > a").text
                
                        if(title == write_title):
                            write_no = driver.find_element(By.CSS_SELECTOR,f"#container > section.left_content > article:nth-child(3) > div.gall_listwrap.list > table > tbody > tr:nth-child({i}) > td.gall_num").text
                            break
                        else:   
                            continue  
                    except:
                        print(i,"번째는 해당사항 없음")
                
                        
                print(f"""
    title: {title}
    확인 : https://gall.dcinside.com/board/view/?id={id}&no={write_no}&page=1
                """)
            
            except Exception as e:
                
                print("작성한 NO를 얻는데 문제가 생겼습니다.")
                print(e)
                print("==================================================")
                return

        
      
     
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    
      


if __name__ == "__main__":
    get_gif_urls()
