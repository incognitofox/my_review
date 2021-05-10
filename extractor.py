# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 00:17:50 2021

@author: Will
"""
from PIL import Image
import cv2
import pytesseract
import csv
import requests

def create_csv(questions_with_responses, filename):
    with open(filename, 'w+') as f:
        for question in questions_with_responses.keys():
            row = question
            responses = questions_with_responses[question]
            for response in responses:
                row += ' ' + str(response)
            row += '\n'
            f.write(row)
    return filename

def create_html(questions_with_responses, filename):
    html = "<table><tr><td>Questions</td></tr>"
    for question in questions_with_responses.keys():
        row = "<tr><td>" + str(question) + "</td>"
        responses = questions_with_responses[question]
        for response in responses:
            row += "<td>" + str(response) + "</td>"
        row += "</tr>"
        html += row
    return html

def parse_img(img_src, entry):
    img = Image.open(requests.get(img_src, stream=True).raw)
    string = pytesseract.image_to_string(img)
    lines = string.split("\n")
    lines = [i for i in lines if i and i != ' ']
    for i in lines:
        if '(' in i and ')' in i and '[' not in i:
            text = i[0:i.find('(') - 1] 
            value = i[i.find('(') + 1:i.find(')')]
            entry[text] = value
    #print(entry)
    #print(lines)
    return None
