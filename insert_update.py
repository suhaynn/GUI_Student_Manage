import tkinter as tk
from tkinter import messagebox
import sql_link


class InsertWindow(tk.Toplevel):
    def __init__(self, user_type):
        # 用idcoad接受登录页面传过来的身份信息
        self.idcoad = user_type
        tk.Toplevel.__init__(self)
        self.title("新增学生")
        self.geometry("500x400")

        self.suername_label = tk.Label(self, text="姓名：")
        self.suername_label.grid(column=0, row=1, padx=10, pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(column=1, row=1, padx=10, pady=10)

        # 创建学号、姓名、密码标签和输入框
        self.id_label = tk.Label(self, text="学号：")
        self.id_label.grid(column=0, row=0, padx=10, pady=10)
        self.id_entry = tk.Entry(self)
        self.id_entry.grid(column=1, row=0, padx=10, pady=10)



        if self.idcoad == 1:# 老师操作学生
            self.password_label = tk.Label(self, text="密码：")
            self.password_label.grid(column=0, row=2, padx=10, pady=10)
            self.password_entry = tk.Entry(self, show="*")
            self.password_entry.grid(column=1, row=2, padx=10, pady=10)

            # 创建语数英成绩标签和输入框
            self.chinese_label = tk.Label(self, text="语文成绩：")
            self.chinese_label.grid(column=0, row=3, padx=10, pady=10)
            self.chinese_entry = tk.Entry(self)
            self.chinese_entry.grid(column=1, row=3, padx=10, pady=10)

            self.math_label = tk.Label(self, text="数学成绩：")
            self.math_label.grid(column=0, row=4, padx=10, pady=10)
            self.math_entry = tk.Entry(self)
            self.math_entry.grid(column=1, row=4, padx=10, pady=10)

            self.english_label = tk.Label(self, text="英语成绩：")
            self.english_label.grid(column=0, row=5, padx=10, pady=10)
            self.english_entry = tk.Entry(self)
            self.english_entry.grid(column=1, row=5, padx=10, pady=10)

        self.txt_label_one = tk.Label(self, text="新增信息需要填全部信息")
        self.txt_label_one.grid(column=0, row=6, padx=10, pady=10)
        self.txt_label_two = tk.Label(self, text="修改信息可根据姓名或学号进行修改(修改成绩)")
        self.txt_label_two.grid(column=0, row=7, padx=10, pady=10)


        #创建确认和取消按钮
        if self.idcoad == 1:
            self.confirm_btn = tk.Button(self, text="确认新增", command=self.confirm_insert_one)
            self.confirm_btn.grid(column=0, row=8, padx=10, pady=10)
            self.confirm_btn = tk.Button(self, text="确认修改", command=self.confirm_update_one)
            self.confirm_btn.grid(column=1, row=8, padx=10, pady=10)
        elif self.idcoad == 2:
            self.confirm_btn = tk.Button(self, text="确认新增", command=self.confirm_insert_two)
            self.confirm_btn.grid(column=0, row=8, padx=10, pady=10)
        #     self.confirm_btn = tk.Button(self, text="确认修改", command=self.confirm_update_click)
        #     self.confirm_btn.grid(column=1, row=8, padx=10, pady=10)

        self.cancel_btn = tk.Button(self, text="取消", command=self.destroy)
        self.cancel_btn.grid(column=2, row=8, padx=10, pady=10)

    # 点击确认按钮时执行的函数
    def confirm_insert_one(self):
        # 获取输入的学号、姓名、密码、语数英成绩
        stu_id = self.id_entry.get()
        stu_name = self.username_entry.get()
        stu_password = self.password_entry.get()
        chinese = self.chinese_entry.get()
        math = self.math_entry.get()
        english = self.english_entry.get()
        # 判断是否全部都填了
        if not stu_id or not stu_name or not chinese or not math or not english:
            messagebox.showerror("错误", "请填写完整信息！密码置空则默认为123456")
            return
        # 插入学生信息并提示结果
        db = sql_link.Database()
        # 检查学号是否已存在
        sql_check = "SELECT * FROM user WHERE stu_id=%s"
        values_check = (stu_id,)
        result_check = db.execute(sql_check, values_check)
        if result_check:
            messagebox.showerror("错误", "该学号已存在，请重新输入！")
            return
        # 插入学生信息并提示结果
        sql_insert = "INSERT INTO user(username, password, stu_id, chinese_score, math_score, english_score) VALUES (%s, %s, %s, %s, %s, %s)"
        values_insert = (stu_name, stu_password, stu_id, chinese, math, english)
        result_insert = db.execute(sql_insert, values_insert)
        print(result_insert)
        if result_insert:
            messagebox.showerror("错误", "学生信息添加失败！")
        else:
            messagebox.showinfo("提示", "学生信息添加成功！")
            self.destroy()  # 关闭窗口

    def confirm_update_one(self):

        # 获取输入的学号、姓名、语数英成绩
        stu_id = self.id_entry.get()
        stu_name = self.username_entry.get()
        chinese = self.chinese_entry.get()
        math = self.math_entry.get()
        english = self.english_entry.get()

        # 判断是否全部都填了
        if not stu_id and not stu_name:
            messagebox.showerror("错误", "请填写学号或姓名！")
            return
        elif not chinese and not math and not english:
            messagebox.showerror("错误", "请填写至少一门成绩！")
            return

        # 更新学生信息并提示结果
        db = sql_link.Database()

        # 检查用户输入的是学号还是姓名
        is_stu_id = True
        try:
            int(stu_id)
        except ValueError:
            is_stu_id = False

        if is_stu_id:
            # 如果输入的是学号，根据学号更新学生信息
            sql = "UPDATE user SET chinese_score=%s, math_score=%s, english_score=%s WHERE stu_id=%s"
            values = (chinese, math, english, stu_id)
        else:
            # 如果输入的是姓名，根据姓名更新学生信息
            sql = "SELECT * FROM user WHERE username=%s"
            values = (stu_name,)
            result = db.execute(sql, values)
            if result is None:
                messagebox.showerror("错误", "该姓名不存在，请重新输入！")
                return
            elif len(result) == 1:
                # 如果找到一条记录，直接根据姓名更新学生信息
                sql = "UPDATE user SET chinese_score=%s, math_score=%s, english_score=%s WHERE username=%s"
                values = (chinese, math, english, stu_name)
            else:
                # 如果找到多条记录，弹窗提示输入学号继续在当前窗口中修改
                stu_ids = [str(x[0]) for x in result]
                messagebox.showinfo("提示", f"根据姓名查询到多条记录，请同时输入要修改学生{stu_name}的姓名和学号")
                return

        result = db.execute(sql, values)
        if result is not None:
            if self.winfo_exists():
                messagebox.showinfo("提示", "学生信息修改成功！")
                self.destroy()
            else:
                # 窗口已被销毁，无需再弹出提示框
                pass
        else:
            messagebox.showerror("错误", "学生信息修改失败！")

    # 新增学生（只输入姓名和学号）
    def confirm_insert_two(self):

        # 获取输入的工号、姓名
        tea_id = self.id_entry.get()
        tea_name = self.username_entry.get()
        # 判断是否全部都填了
        if not tea_id or not tea_name:
            messagebox.showerror("错误", "请填写完整信息！")
            return

        # 检查工号是否已存在
        db = sql_link.Database()
        sql_check = "SELECT * FROM user WHERE tea_id=%s"
        values_check = (tea_id,)
        result_check = db.execute(sql_check, values_check)
        if result_check:
            messagebox.showerror("错误", "该工号已存在，请重新输入！")
            return

        # 插入教师信息并提示结果
        sql_insert = "INSERT INTO user(username, tea_id, user_type) VALUES (%s, %s, %s)"
        values_insert = (tea_name, tea_id, 1)
        result_insert = db.execute(sql_insert, values_insert)
        if result_insert:
            messagebox.showerror("错误", "教师信息添加失败！")
        else:
            messagebox.showinfo("提示", "教师信息添加成功！")
            self.destroy()  # 关闭窗口