# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 12:40:14 2015

@author: jon
"""

import numpy as np
from pandas import Series, DataFrame
import pandas as pd

outcome = pd.read_csv("outcome-of-care-measures.csv")

outcome[:5]
outcome.shape
outcome.head(1)
outcome.index
outcome.columns[:11]
outcome.ix[:2,:11]
Q1 = outcome.ix[:,10]
Q1a = Q1.convert_objects(convert_numeric=True)
Q1a.hist()


# 2
StateList = list(outcome['State'])  #Turn outcome.State into a list
StateSeries = Series(outcome['State'])

def best(state, condition):    
    print state
    print condition
    if (state in StateList) == False: # Need to make state not a string
        print('Invalid State')
    elif condition == "heart attack":
        disease = 11
    elif condition == "heart failure":
        disease = 17
    elif condition == "pneumonia":
        disease = 23
    else:
        print('Invalid outcome')
    
    s = outcome[outcome['State'] == state] #New df only for the state of interest
    print disease
    disease_column = s.columns[disease - 1]
    print disease_column
    StateData = s.ix[:,('State','Hospital Name',disease_column)]
    StateData[disease_column] = StateData[disease_column].convert_objects(convert_numeric = True)
    print StateData[:2]
    HospitalSorted = StateData.sort([disease_column]).reset_index()
    print HospitalSorted.shape
    print HospitalSorted
    print HospitalSorted.ix[0,2]
best("TX", "heart attack")
best("TX", "heart failure")  
best("MD", "heart attack")
best("MD", "pneumonia")

# 3
def rankhospital(state, outcomeName, num = 'best'):
    print state
    print outcomeName
    print num
    if outcomeName == "heart attack":
        disease = 11
    elif outcomeName == "heart failure":
        disease = 17
    elif outcomeName == "pneumonia":
        disease = 23
    else:
        print('Invalid outcome')
    
    s = outcome[outcome['State'] == state] #New df only for the state of interest
    print disease
    disease_column = s.columns[disease - 1]
    print disease_column
    StateData = s.ix[:,('State','Hospital Name',disease_column)]
    StateData[disease_column] = StateData[disease_column].convert_objects(convert_numeric = True)
    HospitalSorted = StateData.sort([disease_column,'Hospital Name']).reset_index().dropna()
    
    if num == 'best':
        num = 1
        hospital = HospitalSorted.ix[0,2]
    elif num == 'worst':
        hospital = HospitalSorted.ix[:,2].tail(1)
    elif num > len(HospitalSorted):
        hospital = 'NA'
    else:
        hospital = HospitalSorted.ix[num-1,2]
    print hospital
rankhospital("TX", "heart failure", 4)        
rankhospital("MD", "heart attack", "worst")
rankhospital("MN", "heart attack", 5000)   

# 4
def rankall(outcomeName, num = 'best'):
    print outcomeName
    print num
    if outcomeName == "heart attack":
        disease = 11
    elif outcomeName == "heart failure":
        disease = 17
    elif outcomeName == "pneumonia":
        disease = 23
    else:
        print('Invalid outcome')
    
    # Generate character list of states
    statelist = []
    hospitalList = []
    for i in outcome['State']:
        if (i in statelist) == False:
            statelist.append(i)
    statelist.sort()
    
    for i in statelist:
        #New df only for the state of interest
        s = []
        disease_column = outcome.columns[disease - 1]
        s = outcome.ix[:,('State','Hospital Name',disease_column)][outcome['State'] == i]
        # sort df by disease column
        s[disease_column] = s[disease_column].convert_objects(convert_numeric = True)
        sSorted = s.sort([disease_column,'Hospital Name']).reset_index().dropna()

        if num == 'best':
            num = 1
            hospital = sSorted.ix[0,2]
        elif num == 'worst':
            hospital = sSorted.ix[:,2].tail(1)
        elif num > len(sSorted):
            hospital = 'NA'
        else:
            hospital = sSorted.ix[num-1,2]
        hospitalList.append(hospital)
    data = {'State':statelist,
            'Hospital':hospitalList}
    RankedDF = pd.DataFrame(data)
    print RankedDF    
rankall("heart attack", 20)    
rankall("pneumonia", "worst")
rankall("heart failure")