# 这是一个示例 Python 脚本。
import json


# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    import os
    import openai

import pymysql

db = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="ai",
    port=3306,
    charset="utf8"
)  # 获取连接server, user, password, database="ai"
curses = db.cursor()
sql = "INSERT INTO ai(id,username,text) VALUE (%s, %s, %s)"
value = (int(0), str(111), "11222")
curses.execute(sql,value)
db.commit()
