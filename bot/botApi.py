import datetime

import openai
import requests

from bot.dialogue import QA, friendQA, insertTAG


def QAMSG(json):
    group_id = json.get("group_id")
    message = json.get("message")
    user_id = json.get("user_id")
    nickname = json.get("nickname")
    if json.get("message").find("<情感设定>") != -1:
        if json.get("message").find("[CQ:at,qq=3459175708]") != -1:
            tag = insertTAG(message, user_id)
            data = {
                "group_id": group_id,
                "message": tag,
                "auto_escape": "false"
            }
            requests.post("http://127.0.0.1:5700/send_group_msg", data=data)
            return

    if json.get("message").find("[CQ:at,qq=3459175708]") != -1:
        qa = friendQA(message.lstrip("[CQ:at,qq=3459175708]"), user_id)
        data = {
            "group_id": group_id,
            "message": qa,
            "auto_escape": "false"
        }
        requests.post("http://127.0.0.1:5700/send_group_msg", data=data)
        # requests.get("http://127.0.0.1:5700/send_group_msg?group_id=%s&message=%s&auto_escape=false" % (group_id, qa))
    return


def friendQAMSG(json):
    message = json.get("message")
    user_id = json.get("user_id")
    nickname = json.get("nickname")
    if json.get("message").find("<情感设定>") != -1:
        tag = insertTAG(message, user_id)
        data = {
            "user_id": user_id,
            "message": "修改成功！这是我和主人的小秘密哦~",
            "auto_escape": "false"
        }
        requests.post("http://127.0.0.1:5700/send_msg", data=data)
        return
    qa = friendQA(message.lstrip("[CQ:at,qq=3459175708]"), user_id)
    data = {
        "user_id": user_id,
        "message": qa,
        "auto_escape": "false"
    }
    requests.post("http://127.0.0.1:5700/send_msg", data=data)
    return
