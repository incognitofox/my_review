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

@app.route('/database', methods=["POST"]) #displays database (?) in databaes tab
def database():
    csv = pd.read_csv("course_database-1.csv")
    csv = csv.round(3)
    return jsonify(csv=csv.to_csv())

if __name__ == '__main__':
    app.run()
