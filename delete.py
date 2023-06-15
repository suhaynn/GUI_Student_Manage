import tkinter as tk
from tkinter import messagebox
import sql_link


class DeleteWindow(tk.Toplevel):
    def __init__(self, user_type):
        tk.Toplevel.__init__(self)
        self.idcoad = user_type
        print(self.idcoad)
        self.title("删除用户")
        self.geometry("300x250")
        # 创建学号、旧密码、新密码标签和输入框
        self.user_id_entry = tk.Label(self, text="学号或工号：")
        self.user_id_entry.grid(column=0, row=0, padx=10, pady=10)
        self.user_id_entry = tk.Entry(self)
        self.user_id_entry.grid(column=1, row=0, padx=10, pady=10)

        self.username_entry = tk.Label(self, text="姓名：")
        self.username_entry.grid(column=0, row=1, padx=10, pady=10)
        self.username_entry = tk.Entry(self)
        self.username_entry.grid(column=1, row=1, padx=10, pady=10)


        # 创建确认和取消按钮
        self.confirm_btn = tk.Button(self, text="确认", command=self.delete_one)
        self.confirm_btn.grid(column=0, row=3, padx=10, pady=10)

        self.cancel_btn = tk.Button(self, text="取消", command=self.destroy)
        self.cancel_btn.grid(column=1, row=3, padx=10, pady=10)

    # 点击确认按钮时执行的函数
    def delete_one(self):

        #教师删除学生
        if self.idcoad == 1:
        # 获取输入的学号、姓名、语数英成绩
            stu_id = self.user_id_entry.get()
            stu_name = self.username_entry.get()
            # 判断是否全部都填了
            db = sql_link.Database()
            if stu_id:
                # 如果输入的是学号，根据学号删除信息
                sql = "DELETE FROM user WHERE stu_id=%s"
                values = (stu_id)
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
                    sql = "DELETE FROM user WHERE username=%s"
                    values = (stu_name)
                else:
                    # 如果找到多条记录，弹窗提示输入学号继续在当前窗口中修改
                    stu_ids = [str(x[0]) for x in result]
                    messagebox.showinfo("提示", f"根据姓名查询到多条记录，请同时输入要修改学生{stu_name}的姓名和学号")
                    return

            result = db.execute(sql, values)
            if result is not None:
                if self.winfo_exists():
                    messagebox.showinfo("提示", "该生已删除成功！")
                    self.destroy()
                else:
                    # 窗口已被销毁，无需再弹出提示框
                    pass
            else:
                messagebox.showerror("错误", "学生信息修改失败！")

         #管理员删除教师
        else:
            tea_id = self.user_id_entry.get()
            tea_name = self.username_entry.get()
            # 判断是否全部都填了
            db = sql_link.Database()
            if tea_id:
                # 如果输入的是学号，根据学号删除信息
                sql = "DELETE FROM user WHERE tea_id=%s"
                values = (tea_id)
            else:
                # 如果输入的是姓名，根据姓名更新学生信息
                sql = "SELECT * FROM user WHERE username=%s"
                values = (tea_name,)
                result = db.execute(sql, values)
                if result is None:
                    messagebox.showerror("错误", "该姓名不存在，请重新输入！")
                    return
                elif len(result) == 1:
                    # 如果找到一条记录，直接根据姓名更新学生信息
                    sql = "DELETE FROM user WHERE username=%s"
                    values = (tea_name)
                else:
                    # 如果找到多条记录，弹窗提示输入学号继续在当前窗口中修改
                    stu_ids = [str(x[0]) for x in result]
                    messagebox.showinfo("提示", f"根据姓名查询到多条记录，请同时输入要修改学生({tea_name})的姓名和学号")
                    return

            result = db.execute(sql, values)
            if result is not None:
                if self.winfo_exists():
                    messagebox.showinfo("提示", "该生已删除成功！")
                    self.destroy()
                else:
                    # 窗口已被销毁，无需再弹出提示框
                    pass
            else:
                messagebox.showerror("错误", "学生信息修改失败！")