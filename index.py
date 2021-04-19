# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:47:15 2021

@author: Will
"""

from flask import Flask, render_template, request, jsonify
import os, io, sys
import pandas as pd
import myReviewScraper

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/scrape")
def scrape():
    print('scraping')
    html = myReviewScraper.test()
    return jsonify(result=html)

if __name__ == '__main__':
    app.run(threaded=True, port=8080)
