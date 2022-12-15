from flask import Flask, request
import requests
import dialogue
import botApi
app = Flask(__name__)


@app.route('/', methods=["POST"])
def post_data():
    json = request.get_json()
    if json.get("sub_type") == "friend":
        botApi.friendQAMSG(json)
    if json.get("sub_type") == "normal":
        botApi.QAMSG(json)
    return 'OK'


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5701)  # 此处的 host和 port对应上面 yml文件的设置
