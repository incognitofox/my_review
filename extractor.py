# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 00:17:50 2021

@author: Will
"""

import csv

def create_csv(questions_with_responses):
    with open('test.csv', 'w+') as f:
        for question in questions_with_responses.keys():
            row = question
            responses = questions_with_responses[question]
            for response in responses:
                row += ' ' + str(response)
            row += '\n'
            f.write(row)
    return
    