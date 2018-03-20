#__author__ = ‘Shane‘
# -*- coding: utf-8 -*-

student_name = 'steven'
student_scores = [95, 85, 75, 65, 55]
ddd = {'k1': 'v1', 'k2': 'v2', 'k3': 'v3'}

def change(scores):
    #global student_name
    student_name = 'alex'
    student_scores[0] = 99
    scores[3] = 100
    ddd['k2'] = 'vvvvvv'

change(scores=student_scores)
print(student_name)
print(student_scores)
print(ddd)