import datetime

import openai
import requests
from flask import Flask, redirect, url_for, request, render_template
import pymysql
# 问答api
app = Flask(__name__)


@app.route('/text/<text>')
def text(text):
    now = datetime.datetime.now()
    openai.api_key = "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"
    print(str(now))
    print(text)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=text + str(now),
        temperature=0,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=[str(now)]
    )
    return response.choices[0].text


# 问答api


@app.route('/Chat', methods=['POST', 'GET'])
def texts():
    openai.api_key = "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"
    print(request.method)
    print(request.form['text'])
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=request.form['text'] + "\nAI:",
        temperature=0.9,
        max_tokens=4050,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )
    print(response)
    return response


app.run()
