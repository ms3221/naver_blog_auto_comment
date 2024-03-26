import customtkinter
import os
from tkinter import messagebox
import socket
import win32gui
import win32con
from naver_login import login,auto_blog_comment



class App(customtkinter.CTk):
    
        def __init__(self):
            super().__init__()
           
           
        
            self.title("룰루레몬")
            self.geometry("560x780")
            self.login_button = customtkinter.CTkButton(master=self, corner_radius=0, height=40,width=240, border_spacing=10, text="로그인",
                                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30")
                                                        , command=login
            )
            self.login_button.grid(row=0, column=0, sticky="w",padx=10)
            self.upload_button = customtkinter.CTkButton(master=self, corner_radius=0, height=40, width=240,border_spacing=10, text="댓글 달기",
                                                        fg_color="gray", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30")
                                                        , command=self.start_blog_comment
            )
            self.upload_button.grid(row=0, column=1, sticky="e",padx=10)
            
            
            self.url_label =customtkinter.CTkLabel(self, text="블로그 url")
            self.url_label.grid(row=1, column=0,columnspan=2, sticky="nsew", pady=(50,20), padx=10)
            self.url_text = customtkinter.CTkTextbox(self,fg_color="lightgray")
            self.url_text.grid(row=2, column=0,columnspan=2, sticky="nsew", pady=2, padx=10)
            
            self.comment_label =customtkinter.CTkLabel(self, text="댓글")
            self.comment_label.grid(row=3, column=0,columnspan=2, sticky="nsew", pady=(20,20), padx=10)
            self.comment_text = customtkinter.CTkTextbox(self,fg_color="lightgray")
            self.comment_text.grid(row=4, column=0,columnspan=2, sticky="nsew", pady=2, padx=10)
        def start_blog_comment(self):
            self.url = self.url_text.get("1.0", "end")
            self.comment = self.comment_text.get("1.0", "end")
            print(self.url,"123")
            links = self.url.split('\n')
            
            for index,link in enumerate(links):
                if link:
                    auto_blog_comment(link,self.comment)
                

def bring_to_front(window_title):
    def enum_windows_callback(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd) and window_title in win32gui.GetWindowText(hwnd):
            titles.append(hwnd)

    titles = []
    win32gui.EnumWindows(enum_windows_callback, titles)
    if titles:
        hwnd = titles[0]  # 가장 첫 번째 찾은 윈도우의 핸들을 가져옵니다.
        win32gui.SetForegroundWindow(hwnd)
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
def check_single_instance():
    # 사용할 포트 번호를 선택합니다. 이 포트는 앱 전용으로 사용되어야 합니다.
    port = 3007
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('127.0.0.1', port))
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
   check_single_instance()