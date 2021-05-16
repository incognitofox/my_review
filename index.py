# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 10:47:15 2021

@author: Will
"""

from flask import Flask, render_template, request, jsonify
import os, io, sys
import pandas as pd
import myReviewScraper
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/scrape")
def scrape():
    print('scraping')
    html = myReviewScraper.test()
    return jsonify(result=html)

@app.route('/database', methods=["POST"]) #displays database (?) in databaes tab
def database():
    csv = pd.read_csv("course_database-1.csv")
    '''courses = csv['Course ID'].str.split(' ', n = 1, expand = True)
    csv.insert(0, 'Department', courses[0])
    csv.insert(1, 'Course #', courses[1])'''
    plt.hist(csv['Professor Score'].dropna())
    plt.show()
    csv = csv.round(3)
    
    #csv.drop(columns=['Course ID'], inplace=True)
    return jsonify(csv=csv.to_csv())

if __name__ == '__main__':
    app.run(threaded=True, port=8080)
