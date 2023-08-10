#!/usr/bin/env python3
#coding=utf-8
"""
pwdgen api
"""

import json
import math
from flask import Flask, Response, request
from flask_cors import CORS, cross_origin
from string import ascii_letters 
from string import digits
from string import punctuation 
from random import choice

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


def entropy_calculation(chars, length):
    return round(math.log(len(chars) ** length, 2))

def generate_passwords(length, amount, chars, omit):
    for char_to_remove in "01IOl" + omit:
        chars = chars.replace(char_to_remove, "")
    result = []
    for _ in range(amount):
        password = ''.join(choice(chars) for i in range(length))
        result.append({
            "entropy": entropy_calculation(chars, length), 
            "password": password.replace('"', '&quot;')
        })
    return result

def generate_passphrases(length, amount, separator):
    file_in = "./words"
    DICT = []
    with open(file_in, encoding = "utf-8") as dict:
        DICT_ENG = dict.read().splitlines()
        for word in DICT_ENG:
            if "'" not in set(word).difference(ascii_letters) and \
            "é" not in set(word).difference(ascii_letters):
                DICT.append(word)
    result = []
    for _ in range(amount):
        passphrase = ("".join(separator)).join(choice(DICT) for i in range(length));
        result.append({
            "entropy": entropy_calculation(set(list(ascii_letters) + list(separator)), len(passphrase)),
            "password": passphrase.replace('"', '&quot;')
        })
    return result

@app.route("/api/v1/digits/<int:length>/", defaults={"amount": 1})
@app.route("/api/v1/digits/<int:length>/<int:amount>")
@cross_origin()
def get_digits(length, amount):
    chars = digits
    omit = request.args.get('omit', default = "", type = str)
    generated = generate_passwords(length, amount, chars, omit)
    res = Response(json.dumps(generated))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/v1/lower/<int:length>/", defaults={"amount": 1})
@app.route("/api/v1/lower/<int:length>/<int:amount>")
@cross_origin()
def get_lower(length, amount):
    chars = ascii_letters[:26]
    omit = request.args.get('omit', default = "", type = str)
    generated = generate_passwords(length, amount, chars, omit)
    res = Response(json.dumps(generated))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/v1/upper/<int:length>/", defaults={"amount": 1})
@app.route("/api/v1/upper/<int:length>/<int:amount>")
@cross_origin()
def get_upper(length, amount):
    chars = ascii_letters[26:]
    omit = request.args.get('omit', default = "", type = str)
    generated = generate_passwords(length, amount, chars, omit)
    res = Response(json.dumps(generated))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/v1/letters/<int:length>/", defaults={"amount": 1})
@app.route("/api/v1/letters/<int:length>/<int:amount>")
@cross_origin()
def get_letters(length, amount):
    chars = ascii_letters
    omit = request.args.get('omit', default = "", type = str)
    generated = generate_passwords(length, amount, chars, omit)
    res = Response(json.dumps(generated))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/v1/alphanum/<int:length>/", defaults={"amount": 1})
@app.route("/api/v1/alphanum/<int:length>/<int:amount>")
@cross_origin()
def get_alphanum(length, amount):
    chars = digits + ascii_letters
    omit = request.args.get('omit', default = "", type = str)
    generated = generate_passwords(length, amount, chars, omit)
    res = Response(json.dumps(generated))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/v1/special/<int:length>/", defaults={"amount": 1})
@app.route("/api/v1/special/<int:length>/<int:amount>")
@cross_origin()
def get_special(length, amount):
    chars = punctuation
    omit = request.args.get('omit', default = "", type = str)
    generated = generate_passwords(length, amount, chars, omit)
    res = Response(json.dumps(generated))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/v1/all/<int:length>/", defaults={"amount": 1})
@app.route("/api/v1/all/<int:length>/<int:amount>")
@cross_origin()
def get_all(length, amount):
    chars = digits + ascii_letters + punctuation + " "
    omit = request.args.get('omit', default = "", type = str)
    generated = generate_passwords(length, amount, chars, omit)
    res = Response(json.dumps(generated))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res

@app.route("/api/v1/words/<int:length>/", defaults={"amount": 1})
@app.route("/api/v1/words/<int:length>/<int:amount>")
@cross_origin()
def get_words(length, amount):
    separator = request.args.get('separator', default = "", type = str)
    generated = generate_passphrases(length, amount, separator)
    res = Response(json.dumps(generated))
    res.headers["Access-Control-Allow-Origin"] = "*"
    res.headers["Content-Type"] = "application/json"
    return res


if __name__ == "__main__":
    app.run("0.0.0.0")
