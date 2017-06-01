# -*- coding: utf-8 -*-
"""
Created on Wed May 31 12:48:30 2017

@author: Camden Ko camdenko@gmail.com
"""
import numpy as np
from random import *
from Tkinter import Tk
import csv
from tkFileDialog import askopenfilename

pvalue = []
vec = []
index = []
rawInput = []
pValues = []

numIterations = int(raw_input("# of iterations: "))
fullSize = int(raw_input("What is the total size of sample? "))
bootSize = int(raw_input("What size of subset do you wish to use? "))
numDays = int(raw_input("How many days did the experiment last? "))
endTime = int(raw_input("When does the experiment end (minutes)?"))

Tk().withdraw()
filename = askopenfilename()

dataFile = open(filename, 'r')
dataReader = csv.reader(dataFile)
for row in dataReader:      # reads in data from chosen csv file
    rawInput.append(row),

dataWidth = numDays
dataHeight = bootSize
data = np.zeros((dataWidth, dataHeight))

# proccess rawInput to open/vs not open
for row_index, row in enumerate(rawInput):
    for col_index, item in enumerate(row):
        rawInput[row_index][col_index] = int(rawInput[row_index][col_index])
        if(rawInput[row_index][col_index] < endTime):
            rawInput[row_index][col_index] = 1.0
        else:
            rawInput[row_index][col_index] = 0.0

# totalOpeners is the total number of opens
totalOpeners = np.sum(rawInput)

inputArray = np.array(rawInput)
# calculate probability between days
dayProb = inputArray.sum(axis = 0)

# calculate probability between rats
ratProb = inputArray.sum(axis = 1)

for row_index, row in enumerate(ratProb):
    ratProb[row_index] = (ratProb[row_index]) / totalOpeners

for row_index, row in enumerate(dayProb):
    dayProb[row_index] = (dayProb[row_index]) / totalOpeners

for rawIt in range(0,numIterations):
    # generate random numbers for index from 1 thru fullSize w/out replacement
    choices = np.random.choice(fullSize - 1, bootSize, replace=False)
    for rowNum in range(0, bootSize):
        for x in range(0, dataWidth):
            data[x][rowNum] = rawInput[x][rowNum]
            
    # data is now full of random rows of information from raw data
    
    iterationsOnEach = 5000
    probDist = []
    # iterating
    for iteration in range(0, iterationsOnEach):
        randArr = np.random.rand(len(ratProb), len(dayProb))
        numSequent = 0.0
        numOpens = 0.0
        for row_index, row in enumerate(randArr):
            for col_index, item in enumerate(row):
                if(randArr[row_index][col_index] >= dayProb[col_index] * ratProb[row_index] * totalOpeners):
                    randArr[row_index][col_index] = 0
                else:
                    randArr[row_index][col_index] = 1
        for row_index in range(0, len(ratProb) - 1):
            for col_index in range(0, len(dayProb)):
                if(randArr[row_index][col_index] == 1):
                    numOpens += 1.0
                    if(randArr[row_index+1][col_index] ==1):
                        numSequent += 1.0
        probDist.append(numSequent / numOpens)
    averageProbDist = sum(probDist) / len(probDist)
    
    # calculate the actual values
    numSequent = 0.0
    numOpens = 0.0
    for x in range(0,len(ratProb)-1):
        for y in range(0,len(dayProb)):
            if(inputArray[x][y] == 1):
                numOpens += 1
                if(rawInput[x+1][y] == 1):
                    numSequent += 1
    actualProb = numSequent / numOpens
    
    numDeviate = 0.0
    for iteration in range(0,iterationsOnEach):
        if abs(probDist[iteration] - averageProbDist) >= abs(actualProb - averageProbDist):
            numDeviate += 1
    pvalue.append(numDeviate/iterationsOnEach)