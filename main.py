import customtkinter
import os
import pyautogui
import time
from tkinter import messagebox
import socket
import shutil
import subprocess
from naver_login import auto_blog_comment
from excel import excel_export, get_absolute_path, excel_read
from crawl_site import get_crawling_site, site_login
from datetime import datetime
from tkinter import messagebox
from community import get_gif_urls


class App(customtkinter.CTk):
   

    def __init__(self):
        super().__init__()
        self.message = """ """

        self.title("악마의 게임")
        self.geometry("560x780")
        self.login_button = customtkinter.CTkButton(
            master=self,
            corner_radius=0,
            height=40,
            width=240,
            border_spacing=10,
            text="글 작성하기",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=self.save_data_by_crawling_data,
        )
        self.login_button.grid(row=6, column=0, sticky="w", padx=10, pady=(10, 0))
        self.upload_button = customtkinter.CTkButton(
            master=self,
            corner_radius=0,
            height=40,
            width=240,
            border_spacing=10,
            text="----",
            fg_color="gray",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=self.find_position
            
        )
        self.upload_button.grid(row=6, column=1, sticky="e", padx=10, pady=(10, 0))

        

       
        self.title_label = customtkinter.CTkLabel(self, text="제목")
        self.title_label.grid(row=0, column=0,columnspan=2, sticky="nsew", pady=5, padx=10)
        self.title_entry = customtkinter.CTkEntry(self, fg_color="pink", text_color='black')
        self.title_entry.grid(row=1, column=0,columnspan=2, sticky="nsew", pady=2, padx=10)

        self.message_box_label = customtkinter.CTkLabel(self, text="내용 박스")
        self.message_box_label.grid(row=2, column=0,columnspan=2, sticky="nsew", pady=5, padx=10)
        self.message_box = customtkinter.CTkTextbox(self)
        self.message_box.grid(
            row=3, column=0, columnspan=2, sticky="nsew", pady=10, padx=10
        )
        self.message_box.insert("end", self.message)


        self.url_box_label = customtkinter.CTkLabel(self, text="url 박스")
        self.url_box_label.grid(row=4, column=0,columnspan=2, sticky="nsew", pady=5, padx=10)
        self.url_box = customtkinter.CTkTextbox(self)
        self.url_box.grid(
            row=5, column=0, columnspan=2, sticky="nsew", pady=10, padx=10
        )
        self.url_box.insert("end", self.message)

    # def start_blog_comment(self):
    #     self.url = self.url_text.get("1.0", "end")
    #     self.comment = self.comment_text.get("1.0", "end")
    #     print(self.url, "123")
    #     links = self.url.split("\n")

    #     for index, link in enumerate(links):
    #         if link:
    #             auto_blog_comment(link, self.comment)

    def message_to_nickname(self):
        # excel에서 데이터를 뽑아온다
        message = self.message_box.get("1.0", "end-1c")

        try:
            self.id_entry.get()
            excel_path = get_absolute_path("excel/export.xlsx")
            excel_data = excel_read(excel_path)
            id = self.id_entry.get()
            pwd = self.pwd_entry.get()
            site_login(id, pwd, message, excel_data)
            messagebox.showinfo(
                "메시지 성공", f"총 {len(excel_data)}개의 쪽지를 보냈습니다."
            )
        except Exception as e:
            messagebox.showerror("메시지 실패", "쪽지보내는데 실패했습니다.")
            print(e)

    # 로그인데 세션을 들고 싸이트에 로그인한다 

    # for문을 돌려서 껏다켯다 하지말고 하나 띄어놓고
    # 계속해서 문자를 보내는 형태로 진행한다.
    def save_data_by_crawling_data(self):
        try:
            message = self.message_box.get("1.0", "end-1c")
            messageList = message.split('\n')
            urls = self.url_box.get("1.0", "end-1c")
            urlList = urls.split('\n')
            title = self.title_entry.get()
            print(messageList, urlList, title)
            for index, key in enumerate(urlList):
                
                get_gif_urls(key,messageList, title)

            
        except Exception as e: 
            print(e)

    # 성공 및 실패했을경우에 대해서 생각해야 한다.

    def find_position(self):
        try:
            while True:
                x , y = pyautogui.position()
                print(f"현재 마우스 포인터의 좌표: ({x}, {y})", end='\r')
                time.sleep(0.1)  # 0.1초마다 업데이트
        except KeyboardInterrupt:
            print("\n프로그램 종료")





def check_single_instance():
    # 사용할 포트 번호를 선택합니다. 이 포트는 앱 전용으로 사용되어야 합니다.
    port = 3007
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(("127.0.0.1", port))
        print("app start at 3005port")
        app = App()
        app.mainloop()
    except socket.error:
        print("app already started!!")
        # 실행 중인 앱 인스턴스로 포커스를 이동하는 로직을 추가할 수 있습니다.
        # 이 예시에서는 단순히 메시지를 출력합니다.
    finally:
        sock.close()


if __name__ == "__main__":
    # command = r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_dev_session"'
    # subprocess.run을 사용하여 명령어를 실행합니다.
    # subprocess.Popen(command, shell=True)
    
    check_single_instance()
   
