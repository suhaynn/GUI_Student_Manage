import tkinter as tk
from tkinter import messagebox

import pymysql

# 定义一个包含数据库配置的字典
db_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': '123456',
    'database': 'students',
    'charset': 'utf8mb4'
}

# 定义一个包含字段类型和默认值的字典
field_type_map = {
    'id': 'INT AUTO_INCREMENT PRIMARY KEY',
    'username': 'VARCHAR(255) DEFAULT ""',
    'password': 'VARCHAR(255) DEFAULT "123456"',
    'user_type': 'INT DEFAULT NULL',
    'stu_id': 'INT DEFAULT NULL',
    'tea_id': 'INT DEFAULT NULL',
    'chinese_score': 'INT DEFAULT NULL',
    'math_score': 'INT DEFAULT NULL',
    'english_score': 'INT DEFAULT NULL'
}

field_default_map = {
    'id': 'NULL',
    'username': '""',
    'password': '"123456"',
    'user_type': 'NULL',
    'stu_id': 'NULL',
    'tea_id': 'NULL',
    'chinese_score': 'NULL',
    'math_score': 'NULL',
    'english_score': 'NULL'
}


# 定义一个Database类，用于连接MySQL数据库并执行查询操作
class Database:
    def __init__(self):
        # 创建MySQL数据库连接对象
        self.conn = pymysql.connect(**db_config)
        # 创建游标对象
        self.cursor = self.conn.cursor()

    def execute(self, sql, values=None):
        try:
            # 如果有传入参数，则使用参数执行SQL语句
            if values:
                self.cursor.execute(sql, values)
            # 否则直接执行SQL语句
            else:
                self.cursor.execute(sql)
            # 获取查询结果
            result = self.cursor.fetchall()
            return result
        except Exception as e:
            print('执行SQL语句出错：', e)
            return None

    def fetchall(self, sql, values=None):
        # 调用execute方法并返回查询结果
        return self.execute(sql, values)

    def fetchone(self, sql, values=None):
        # 调用execute方法并返回单个查询结果
        result = self.execute(sql, values)
        if result:
            return result[0]
        else:
            return None

    def close(self):
        # 提交更改并关闭游标对象和数据库连接对象
        try:
            self.conn.commit()
        except Exception as e:
            print('提交更改出错：', e)
            self.conn.rollback()
        finally:
            self.cursor.close()
            self.conn.close()


# 定义一个DatabaseChecker类
class DatabaseChecker:
    def __init__(self):
        # 实例化一个Database对象
        self.db = Database()
        # 调用check_database方法，检查数据库是否符合要求
        self.check_database()

    def check_database(self):
        # 查找students数据库
        sql = "SHOW DATABASES LIKE 'students'"
        result = self.db.fetchone(sql)
        if result:
            # 如果存在students数据库，则查找user表格
            db_config['database'] = 'students'
            db = Database()
            sql = "SHOW TABLES LIKE 'user'"
            result = db.fetchone(sql)
            if result:
                # 如果存在user表格，则检查表格中是否包含所有需要的字段
                sql = "DESCRIBE user"
                result = db.fetchall(sql)
                fields = ['id', 'username', 'password', 'user_type', 'stu_id', 'tea_id', 'chinese_score', 'math_score',
                          'english_score']
                field_names = [r[0] for r in result]
                # 缺少的字段
                missing_fields = set(fields) - set(field_names)
                if missing_fields:
                    # 创建缺少的字段
                    self.create_missing_fields(missing_fields)
                else:
                    messagebox.showinfo("提示",
                                        "本地已存在名为students的数据库，并有名为user的表格，表格中包含所有需要的字段")
            else:
                # 如果不存在user表格，则创建
                self.create_user_table()
                # 创建完user表添加一组默认数据
                self.add_data()
        else:
            # 如果不存在students数据库，则创建
            self.create_students_database()
            # 创建完stydents数据库添加一组默认数据
            self.add_data()

        # 修改字段顺序
        self.modify_field_order()

        # 关闭数据库连接
        self.db.close()

    def create_missing_fields(self, missing_fields):
        # 显示提示框，提示缺少的字段，并询问是否创建
        msg = f"本地已存在名为students的数据库，并有名为user的表格，但是表格中缺少以下必要的字段：\n{', '.join(missing_fields)}\n是否创建这些字段？"
        result = messagebox.askyesno("提示", msg)
        if result:
            db = Database()
            for missing_field in missing_fields:
                if missing_field == 'user_type':  # 如果缺少 user_type 字段，设置数据类型为 int 并默认值为 0
                    sql = "ALTER TABLE user ADD COLUMN user_type INT NOT NULL DEFAULT 0"
                else:
                    sql = f"ALTER TABLE user ADD COLUMN {missing_field} {field_type_map[missing_field]} DEFAULT {field_default_map[missing_field]}"
                db.execute(sql)
            messagebox.showinfo("提示", "成功添加缺少的字段")

    def create_user_table(self):
        # 显示提示框，提示不存在user表格，并询问是否创建
        result = messagebox.askyesno("提示", "本地已存在名为students的数据库，但是没有名为user的表格，是否创建该表格？")
        if result:
            db = Database()
            sql = "CREATE TABLE user (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255) DEFAULT '', password VARCHAR(255) DEFAULT '123456', user_type INT NOT NULL DEFAULT '0', stu_id INT DEFAULT NULL, tea_id INT DEFAULT NULL, chinese_score INT DEFAULT NULL, math_score INT DEFAULT NULL, english_score INT DEFAULT NULL)"
            db.execute(sql)
            messagebox.showinfo("提示", "成功在名为students的数据库中创建名为user的表格，并添加了所有需要的字段")

    def create_students_database(self):
        # 显示提示框，提示不存在students数据库，并询问是否创建
        result = messagebox.askyesno("提示", "本地不存在名为students的数据库，是否创建该数据库？")
        if result:
            db = Database()
            sql = "CREATE DATABASE students"
            db.execute(sql)
            messagebox.showinfo("提示", "成功创建名为students的数据库")


    def modify_field_order(self):
        # 修改数据库字段顺序的SQL语句
        sql = "ALTER TABLE user MODIFY id INT NOT NULL AUTO_INCREMENT FIRST, MODIFY username VARCHAR(50) NOT NULL AFTER id, MODIFY password VARCHAR(50) NOT NULL DEFAULT '123456' AFTER username, MODIFY user_type int NOT NULL DEFAULT '0' AFTER password, MODIFY stu_id int DEFAULT NULL AFTER user_type, MODIFY tea_id INT DEFAULT NULL AFTER stu_id, MODIFY chinese_score INT DEFAULT NULL AFTER tea_id, MODIFY math_score INT DEFAULT NULL AFTER chinese_score, MODIFY english_score INT DEFAULT NULL AFTER math_score"
        db = Database()
        db.execute(sql)
        db.close()

    def add_data(self):
        # 添加数据
        # db_config['database'] = 'students'
        db = Database()
        sql = "INSERT INTO user(username, password, user_type, tea_id) VALUES ('admin', 'admin', 2, 1)"
        db.execute(sql)
        db.close()
