#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import request
from flask import render_template
import os

from approximate import approximate_match 

app = Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


@app.route("/", methods=['POST'])
def index():
    f = open('words.txt', "r")
    t = f.readline()
    t = t.replace('�', "")
    t = t.replace("'", "")
    t += " "

    missed = {}
    #p = input("Enter the search keyword : ")
    p = request.form.get('keyword')
    p = p.lower()
    print(p)
    indexes = approximate_match(p, t, 2, missed)

    wordlist = []
    indexlist = []
    correct=0
    for i in indexes:
        if(t[i-1]==" " and t[i+len(p)]==" "):
            if t[i:i+len(p)] not in wordlist:
                if(t[i:i+len(p)] == p):
                    correct=1
                else:
                    wordlist.append(t[i:i+len(p)])
                    indexlist.append(i)
        else:
            del missed[i]

    print("Did you mean ", end=" ")
    for word in wordlist:
        print(word, end=" ")
    print("?")

    isEmpty = False
    if(len(wordlist)<1):
        isEmpty = True

    return render_template('index.html', missed=missed, words=wordlist, indexlist=indexlist, correct=correct, typed=p, isEmpty=isEmpty)


@app.route("/", methods=['GET'])
def index2():
    return render_template("index.html", correct=2)


if __name__ == "__main__":
    app.run(debug=True)
