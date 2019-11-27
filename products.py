# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 14:22:15 2019

@author: user
"""


def products():
    counter = 0
    f = open('configurations\products.txt','r')
    message = f.read()
    message = message.replace(" ", '')
    message = message.replace('\t', '')
    amount = message.split('\n')
    global product
    product = [0] * len(amount)
    names = [0] * len(amount)

    for i in range(len(amount)):

        product[i] = amount[i].split(';')
        names[i] = str(product[i][0])
        if names[i] == '':
            counter += 1
    
      
      
    for i in range(counter):
        names.remove('')
    return names
    
    
def defaultValues(name):
    products()
    for i in range(len(product)):
        if name == product[i][0]:
            return product[i]
            print(product[i])
    
