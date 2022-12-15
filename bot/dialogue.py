import datetime

import openai
import requests
from flask import Flask, redirect, url_for, request, render_template
import pymysql

openai.api_key = "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"

db = pymysql.connect(
    host="localhost",
    user="root",
    password="root",
    database="ai",
    port=3306,
    charset="utf8"
)  # 获取连接server, user, password, database="ai"


def QA(text, userID):
    try:
        db.ping(reconnect=True)
        curses = db.cursor()
        num = curses.execute("select * from ai_msg where user_id=" + str(userID))
    except:
        db.rollback()

    if num != 0:
        fetchall = curses.fetchall()[0]
        str(fetchall).replace("[nc]", "\n")
        Human = fetchall[2] + "\n" + "Human: " + text + "\n" + "AI:"
    else:
        Human = "Human: " + text + "\n" + "AI:"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=Human,
        temperature=0.9,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    msg = Human + response.choices[0].text + "\n"
    print(msg)
    if num == 0:
        sql = "INSERT INTO ai_msg(id,user_id,text) VALUE (%s, %s, %s)"
        value = (0, str(userID), msg.replace("\n", "[nc]"))
        curses.execute(sql, value)
        db.commit()
    else:
        sqls = "UPDATE ai_msg SET text=%s WHERE user_id=%s"
        values = (msg.replace("\n", "[nc]"), fetchall[1])
        curses.execute(sqls, values)
        db.commit()
        db.close()
    return response.choices[0].text


def friendQA(text, userID):
    curses = db.cursor()
    try:
        db.ping(reconnect=True)
        # 查询ai和你的对话
        num = curses.execute("select * from ai_msg where user_id=" + str(userID))
        cursess_fetchalls = curses.fetchall()
        # 查询ai的设定
        userNum = curses.execute("select * from character_setting where user_id=" + str(userID))
        curses_fetchall = curses.fetchall()

    except:
        db.rollback()
    msgs = ""
    if num != 0:
        fetchalls_ = cursess_fetchalls[0]
        print(len(fetchalls_[2]))
        if len(fetchalls_[2]) > 1000:

            split = str(fetchalls_[2]).split("AI", 5)
            msgs = split[len(split) - 1]
        else:
            msgs = fetchalls_[2]
        if userNum != 0:
            # ai的设定
            fetchalls = curses_fetchall[0]
            # ai和你的对话
            fetchall = msgs
            str(fetchall).replace("[nc]", "\n")
            Human = fetchalls[2] + "\n" + fetchall + "\n" + "Human: " + text + "\n" + "AI:"
        else:
            fetchall = msgs
            str(fetchall).replace("[nc]", "\n")
            Human = fetchall[2] + "\n" + "Human: " + text + "\n" + "AI:"
    else:
        if userNum != 0:
            fetchalls = curses_fetchall[0]
            Human = fetchalls[2] + "\n" + "Human: " + text + "\n" + "AI:"
        else:
            Human = "Human: " + text + "\n" + "AI:"
    replace = str(Human).replace("[nc]", "\n")
    # print(replace)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=replace,
        temperature=0.9,
        max_tokens=300,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    if userNum == 0:
        msg = Human + response.choices[0].text + "\n"
    else:
        msg = str(Human).replace(fetchalls[2], "") + response.choices[0].text + "\n"
    # print(msg)
    if num == 0:
        sql = "INSERT INTO ai_msg(id,user_id,text) VALUE (%s, %s, %s)"
        value = (0, str(userID), str(msg.replace("\n", "[nc]")))
        curses.execute(sql, value)
        db.commit()
    else:
        sqls = "UPDATE ai_msg SET text=%s WHERE user_id=%s"
        values = (str(msg.replace("\n", "[nc]")), fetchalls_[1])
        curses.execute(sqls, values)
        db.commit()
    db.close()
    return response.choices[0].text


def insertTAG(msg, userID):
    count = str(msg).count("<情感设定>")
    try:
        db.ping(reconnect=True)
        curses = db.cursor()
        userNum = curses.execute("select * from character_setting where user_id=" + str(userID))
    except:
        db.rollback()

    str(msg).replace("<情感设定>", "")
    if count != 0:
        if userNum != 0:
            sqls = "UPDATE character_setting SET assistant_setting=%s WHERE user_id=%s"
            values = (str(msg), userID)
            curses.execute(sqls, values)
            db.commit()
            db.close()
        else:
            sql = "INSERT INTO character_setting(id,user_id,assistant_setting) VALUE (%s, %s, %s)"
            value = (0, userID, str(msg))
            curses.execute(sql, value)
            db.commit()
    return "修改成功！这是我和主人的小秘密哦~"
