import tkinter as tk
from search import SearchWindow
from change_password import ChangePasswordWindow


class zeroWindow(tk.Tk):
    def __init__(self, user_type):
        global idcard
        idcard = user_type
        tk.Tk.__init__(self)
        self.title("学生页面")
        self.geometry("400x500")

        # 创建标题标签
        self.title_label = tk.Label(self, text="学生页面", font=("Arial", 24))
        self.title_label.pack(pady=20)

        # 创建查询成绩按钮
        self.search_scores_btn = tk.Button(self, text="查询成绩", command=self.open_search_window)
        self.search_scores_btn.pack(pady=20)

        # 创建修改密码按钮
        self.change_password_btn = tk.Button(self, text="修改密码", command=self.open_change_password_window)
        self.change_password_btn.pack(pady=20)

        # 创建退出登录按钮
        self.logout_btn = tk.Button(self, text="退出登录", command=self.logout_btn_click)
        self.logout_btn.pack(pady=20)



    def open_search_window(self):
        SearchWindow(idcard)

    def open_change_password_window(self):
        ChangePasswordWindow(idcard)

    def logout_btn_click(self):
        self.destroy()



if __name__ == '__main__':
    window = zeroWindow(0)
    window.mainloop()