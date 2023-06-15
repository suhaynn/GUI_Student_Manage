import tkinter as tk
from tkinter import messagebox
import sql_link


class ChangePasswordWindow(tk.Toplevel):
    def __init__(self, user_type):
        tk.Toplevel.__init__(self)
        self.idcoad = user_type
        print(self.idcoad)
        self.title("修改密码")
        self.geometry("300x250")

        # 创建学号、旧密码、新密码标签和输入框
        self.stu_id_label = tk.Label(self, text="学号或工号：")
        self.stu_id_label.grid(column=0, row=0, padx=10, pady=10)
        self.stu_id_entry = tk.Entry(self)
        self.stu_id_entry.grid(column=1, row=0, padx=10, pady=10)

        self.old_password_label = tk.Label(self, text="旧密码：")
        self.old_password_label.grid(column=0, row=1, padx=10, pady=10)
        self.old_password_entry = tk.Entry(self, show="*")
        self.old_password_entry.grid(column=1, row=1, padx=10, pady=10)

        self.new_password_label = tk.Label(self, text="新密码：")
        self.new_password_label.grid(column=0, row=2, padx=10, pady=10)
        self.new_password_entry = tk.Entry(self, show="*")
        self.new_password_entry.grid(column=1, row=2, padx=10, pady=10)

        # 创建确认和取消按钮
        self.confirm_btn = tk.Button(self, text="确认", command=self.confirm_btn_click)
        self.confirm_btn.grid(column=0, row=3, padx=10, pady=10)

        self.cancel_btn = tk.Button(self, text="取消", command=self.destroy)
        self.cancel_btn.grid(column=1, row=3, padx=10, pady=10)

    # 点击确认按钮时执行的函数
    def confirm_btn_click(self):
        # 获取输入的学号、旧密码和新密码


        if self.idcoad == 0:
        # 修改密码并提示结果
            stu_id = self.stu_id_entry.get()
            old_password = self.old_password_entry.get()
            new_password = self.new_password_entry.get()
            db = sql_link.Database()
            sql = "SELECT * FROM user WHERE stu_id=%s AND password=%s"
            values = (stu_id, old_password)
            student_info = db.fetchone(sql, values)
            if student_info is None:
                messagebox.showerror("警告", "学号或密码错误！")
            else:
                sql = "UPDATE user SET password=%s WHERE stu_id=%s"
                values = (new_password, stu_id)
                db.execute(sql, values)
                db.close()
                messagebox.showinfo("提示", "密码修改成功！")
                self.destroy()
        else:
            tea_id = self.stu_id_entry.get()
            old_password = self.old_password_entry.get()
            new_password = self.new_password_entry.get()
            db = sql_link.Database()
            sql = "SELECT * FROM user WHERE tea_id=%s AND password=%s"
            values = (tea_id, old_password)
            student_info = db.fetchone(sql, values)
            if student_info is None:
                messagebox.showerror("警告", "工号或密码错误！")
            else:
                sql = "UPDATE user SET password=%s WHERE tea_id=%s"
                values = (new_password, tea_id)
                db.execute(sql, values)
                db.close()
                messagebox.showinfo("提示", "密码修改成功！")
                self.destroy()