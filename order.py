# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 08:55:58 2019

@author: user
"""
import hardware.config as config
#read 
def orders():
    #read the orders.txt file
    f = open(config.MODirectory ,'r')
    global decoded
    message = f.read()
    message = message.split('\n')
#    message = message.split('\n')
    decoded = [0 for i in range(len(message))]
    global orderNumbers 
    orderNumbers= [0 for i in range(len(message))]
    global productNumbers 
    productNumbers =  [0 for i in range(len(message))]
    global orderAmounts 
    
    orderAmounts = [0 for i in range(len(message))]
    for i in range(0, len(message)):
        decoded[i] = message[i].split(';')
    for i in range(len(message)):
        orderNumbers[i] = decoded[i][0]
        productNumbers[i] = decoded[i][1]
        orderAmounts[i] = decoded[i][2]
    
#save the information in arays

#3 functions to return the amount, and P/MO numbers selected
def returnOrder():
    orders()
    myValue = [0 for i in range(len(decoded))]
    for i in range(len(decoded)):
        myValue[i] = decoded[i][0] + ' '+ decoded[i][1]+ ' ' + decoded[i][2]
    return(myValue) 
    

def returnProduct(MO):
    orders()
    for i in range(len(orderNumbers)):
        if(MO == returnOrder()[i]):
            return(productNumbers[i])
        
def returnAmount(MO):
    orders()
    for i in range(len(orderNumbers)):
        if (MO == returnOrder()[i]):
            return(orderAmounts[i])


