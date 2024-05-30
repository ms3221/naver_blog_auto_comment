import customtkinter
import os
from tkinter import messagebox
import socket
import win32gui, shutil
import win32con
from naver_login import auto_blog_comment
from excel import excel_export, get_absolute_path, excel_read
from crawl_site import get_crawling_site, site_login
from datetime import datetime
from tkinter import messagebox


class App(customtkinter.CTk):

    def __init__(self):
        super().__init__()
        self.message = """
    안녕하세요 지치신 사장님 위해서 
    연락드렸습니다.
    대화한번 해보시죠
    텔@ssrr119 연락주세요
                """

        self.title("악마의 게임")
        self.geometry("560x780")
        self.login_button = customtkinter.CTkButton(
            master=self,
            corner_radius=0,
            height=40,
            width=240,
            border_spacing=10,
            text="닉네임 데이터 추출",
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
            text="쪽지 보내기",
            fg_color="gray",
            text_color=("gray10", "gray90"),
            hover_color=("gray70", "gray30"),
            command=self.message_to_nickname,
        )
        self.upload_button.grid(row=6, column=1, sticky="e", padx=10, pady=(10, 0))

        self.url_label = customtkinter.CTkLabel(self, text="ID")
        self.url_label.grid(
            row=0, column=0, columnspan=2, sticky="nsew", pady=5, padx=10
        )
        self.id_entry = customtkinter.CTkEntry(self, fg_color="lightgray")
        self.id_entry.grid(
            row=1, column=0, columnspan=2, sticky="nsew", pady=2, padx=10
        )

        self.comment_label = customtkinter.CTkLabel(self, text="PWD")
        self.comment_label.grid(
            row=2, column=0, columnspan=2, sticky="nsew", pady=5, padx=10
        )
        self.pwd_entry = customtkinter.CTkEntry(self, fg_color="lightgray")
        self.pwd_entry.grid(
            row=3, column=0, columnspan=2, sticky="nsew", pady=2, padx=10
        )

        self.start_index_label = customtkinter.CTkLabel(self, text="시작 페이지")
        self.start_index_label.grid(row=4, column=0, sticky="w", pady=5, padx=10)
        self.start_index_entry = customtkinter.CTkEntry(self, fg_color="lightgray")
        self.start_index_entry.grid(row=5, column=0, sticky="w", pady=2, padx=10)

        self.end_index_label = customtkinter.CTkLabel(self, text="마지막 페이지")
        self.end_index_label.grid(row=4, column=1, sticky="w", pady=5, padx=10)
        self.end_index_entry = customtkinter.CTkEntry(self, fg_color="lightgray")
        self.end_index_entry.grid(row=5, column=1, sticky="w", pady=2, padx=10)

        self.message_box = customtkinter.CTkTextbox(self)
        self.message_box.grid(
            row=7, column=0, columnspan=2, sticky="nsew", pady=10, padx=10
        )
        self.message_box.insert("end", self.message)

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
            id = self.id_entry.get()
            pwd = self.pwd_entry.get()
            start_index = self.start_index_entry.get()
            end_index = self.end_index_entry.get()
            if os.path.exists(get_absolute_path("excel")):
                shutil.rmtree(get_absolute_path("excel"))
                os.mkdir(get_absolute_path("excel"))
            head = [["no", "nickname", "수집날짜"]]
            excel_path = get_absolute_path("excel/export.xlsx")
            nickname_list = get_crawling_site(id, pwd, start_index, end_index)
            for index, nickname in enumerate(nickname_list, start=1):
                head.append([index, nickname, datetime.today().strftime("%Y/%m/%d")])
            excel_export(head)
            messagebox.showinfo(
                "추출 성공 메시지", f"데이터 추출에 성공했습니다.총{len(head)}개"
            )
        except Exception as e:
            messagebox.showerror("추출 실패 메시지", "데이터 추출에 실패했습니다.")
            print(e)

    # 성공 및 실패했을경우에 대해서 생각해야 한다.


def bring_to_front(window_title):
    def enum_windows_callback(hwnd, titles):
        if win32gui.IsWindowVisible(hwnd) and window_title in win32gui.GetWindowText(
            hwnd
        ):
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
    check_single_instance()
