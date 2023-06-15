import tkinter as tk
from tkinter import messagebox
import sql_link


class SearchWindow(tk.Toplevel):
    def __init__(self,user_type):
        self.idcoad = user_type
        tk.Toplevel.__init__(self)
        self.title("查询成绩")
        self.geometry("300x150")

        # 创建学号、密码标签和输入框
        self.stu_id_label = tk.Label(self, text="学号：")
        self.stu_id_label.grid(column=0, row=0, padx=10, pady=10)
        self.stu_id_entry = tk.Entry(self)
        self.stu_id_entry.grid(column=1, row=0, padx=10, pady=10)

        self.stu_password_label = tk.Label(self, text="密码：")
        self.stu_password_label.grid(column=0, row=1, padx=10, pady=10)
        self.stu_password_entry = tk.Entry(self, show="*")
        self.stu_password_entry.grid(column=1, row=1, padx=10, pady=10)

        # 创建确认和取消按钮
        self.confirm_btn = tk.Button(self, text="确认", command=self.confirm_btn_click)
        self.confirm_btn.grid(column=0, row=2, padx=10, pady=10)

        self.cancel_btn = tk.Button(self, text="取消", command=self.destroy)
        self.cancel_btn.grid(column=1, row=2, padx=10, pady=10)

    # 点击确认按钮时执行的函数
    def confirm_btn_click(self):
        # 获取输入的学号和密码
        stu_id = self.stu_id_entry.get()
        stu_password = self.stu_password_entry.get()

        # 查询成绩并提示结果
        db = sql_link.Database()
        sql = "SELECT * FROM user WHERE stu_id=%s AND password=%s"
        values = (stu_id, stu_password)
        student_info = db.fetchall(sql, values)
        if student_info is None:
            messagebox.showinfo("提示", "没有查询到成绩！")
            self.stu_password_entry.delete(0, tk.END)
        else:
            if len(student_info) > 0:
                messagebox.showinfo("成绩查询",
                                    f"姓名:       {student_info[0][1]}\n\r学号:       {student_info[0][3]}\n\r语文成绩:{student_info[0][6]}\n\r数学成绩:{student_info[0][7]}\n\r英语成绩:{student_info[0][8]}")
            else:
                messagebox.showinfo("提示", "没有查询到成绩！")
                self.stu_password_entry.delete(0, tk.END)
            # db.close()
            # self.destroy()
            # db.close()
            # self.destroy()