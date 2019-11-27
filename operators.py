# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 13:35:35 2019

@author: user
"""


def operator():
    f = open('configurations\operators.txt','r')
    message = f.read()
    user = message.split('\n')
    return user
    
operator()