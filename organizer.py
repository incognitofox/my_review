# -*- coding: utf-8 -*-
"""
Created on Mon May 10 08:13:18 2021

@author: Will
"""
import pickle
import copy

organized = {}
'''try: 
    organized = pickle.load(open('database3.pkl', "rb"))
except:
    pass'''
evals = {}
try: 
    evals = pickle.load(open('database2.pkl', "rb"))
except:
    pass
courses = set()
try: 
    courses = pickle.load(open('courses.pkl', "rb"))
except:
    pass

#if(len(organized) < 3000):
for course in courses:
    organized[course] = {}
    print(course)
    for section in evals:
        stripped = section.replace('U Chicago Prod', '')
        if course[0] in stripped and course[1] in stripped:
            quarter = ""
            year = ""
            spring = stripped.lower().find("spring")
            autumn = stripped.lower().find("autumn")
            winter = stripped.lower().find("winter")
            summer = stripped.lower().find("summer")
            if spring != -1:
                quarter = "spring"
                year = stripped[spring + len("spring"): [spring + len("spring") + 4]
            elif autumn != -1:
                quarter = "autumn"
            elif winter != -1:
                quarter = "winter"
            elif summer != -1:
                quarter = "summer"
            year = 0
            instructor = ""
            ind = stripped.find('Instructor(s)')
            instructor = stripped[ind + 14:].strip()
        
            organized[course][(instructor, quarter + year, stripped)] = evals[section]
    pickle.dump(organized, open("database3.pkl", "wb+"))
