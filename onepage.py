import tkinter as tk
from search import SearchWindow
from change_password import ChangePasswordWindow
from insert_update import InsertWindow
from delete import DeleteWindow
from print_grade import ExcelWriter

class oneWindow(tk.Tk):
    def __init__(self, user_type):

        global idcard
        idcard = user_type
        # print(user_type)
        print(f"身份类别是：{idcard}")
        tk.Tk.__init__(self)
        self.title("教师页面")
        self.geometry("400x500")

        # 创建标题标签
        self.title_label = tk.Label(self, text="教师页面", font=("Arial", 24))
        self.title_label.pack(pady=20)

        # 创建查询成绩按钮
        self.search_scores_btn = tk.Button(self, text="查询学生成绩", command=self.open_search_window)
        self.search_scores_btn.pack(pady=20)

        # 创建修改密码按钮
        self.change_password_btn = tk.Button(self, text="修改个人密码", command=self.open_change_password_window)
        self.change_password_btn.pack(pady=20)
        #删除学生
        self.search_scores_btn = tk.Button(self, text="删除信息", command=self.open_delete_window)
        self.search_scores_btn.pack(pady=20)

        self.search_scores_btn = tk.Button(self, text="打印学生成绩", command=self.open_print_window)
        self.search_scores_btn.pack(pady=20)
        # 新增学生
        self.search_scores_btn = tk.Button(self, text="新增或修改学生信息", command=self.open_insert_window)
        self.search_scores_btn.pack(pady=20)
        # 创建退出登录按钮
        self.logout_btn = tk.Button(self, text="退出登录", command=self.logout_btn_click)
        self.logout_btn.pack(pady=20)

    def open_search_window(self):
        SearchWindow(idcard)

    def open_change_password_window(self):
        ChangePasswordWindow(idcard)

    def open_insert_window(self):
        InsertWindow(idcard)

    def open_delete_window(self):
        DeleteWindow(idcard)

    def open_print_window(self):
        ew = ExcelWriter()
        ew.get_data()
        # 写入Excel文件并打印
        ew.write_excel()
    def logout_btn_click(self):
        self.destroy()

if __name__ == '__main__':
    window = oneWindow(1)
    window.mainloop()
