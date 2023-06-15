import tkinter as tk
from tkinter import messagebox
import sql_link
import zeropage
import onepage
import twopage


class LoginGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("登录")
        self.root.geometry("400x200")
        self.root.resizable(0, 0)

        tk.Label(self.root, text="用户名：").grid(row=0, column=0, padx=10, pady=5)
        self.username_entry = tk.Entry(self.root)
        self.username_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.root, text="密码：").grid(row=1, column=0, padx=10, pady=5)
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=5)

        self.user_type = tk.IntVar()
        self.user_type.set(0)  # 默认选择学生
        tk.Label(self.root, text="用户类型：").grid(row=2, column=0, padx=10, pady=5)
        tk.Radiobutton(self.root, text="学生", variable=self.user_type, value=0).grid(row=2, column=1, padx=10, pady=5)
        tk.Radiobutton(self.root, text="老师", variable=self.user_type, value=1).grid(row=2, column=2, padx=10, pady=5)
        tk.Radiobutton(self.root, text="管理员", variable=self.user_type, value=2).grid(row=2, column=3, padx=10,
                                                                                        pady=5)

        tk.Button(self.root, text="登录", command=self.login).grid(row=3, column=0, columnspan=3, padx=10, pady=10)
        tk.Button(self.root, text="初始化数据库", command=self.fresh_sql).grid(row=3, column=1, columnspan=3, padx=10,
                                                                               pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_type = self.user_type.get()

        db = sql_link.Database()
        sql = "select * from user where (username=%s or stu_id=%s or tea_id=%s) and password=%s and user_type=%s"
        values = (username, username, username, password, user_type)

        query = db.execute(sql, values)
        if query:
            # query[0][3]表示第一条记录的数据库中第四个字段的值user_type，也就是用户类型（0表示学生，1表示老师，2表示管理员）。
            # 数据库下标是从0开始
            user_type = query[0][3]
            if user_type == 0:
                self.zerowindow = zeropage.zeroWindow(user_type)
                self.zerowindow.mainloop()
                self.root.destroy()  # 销毁登录窗口
            elif user_type == 1:
                print(123)
                self.onewindow = onepage.oneWindow(user_type)
                self.onewindow.mainloop()
                self.root.destroy()  # 销毁登录窗口
            elif user_type == 2:
                # self.new_window(user_type)
                self.twowindow = twopage.twoWindow(user_type)
                self.twowindow.mainloop()
                self.root.destroy()  # 销毁登录窗口

        else:
            messagebox.showerror("错误", "用户名或密码错误！")
            self.password_entry.delete(0, tk.END)  # 输入错误时隐藏密码

    def fresh_sql(self):
        sql_link.DatabaseChecker()


if __name__ == "__main__":
    root = tk.Tk()
    LoginGUI(root)
    root.mainloop()
