# -*- coding: utf-8 -*-
"""
Created on Wed May 31 12:48:30 2017

@author: masonlab
"""
import numpy as np
from random import *

pvalue = []
vec = []
index = []

numIterations = int(raw_input("# of iterations: "))
fullSize = int(raw_input("What is the total size of sample? "))
bootSize = int(raw_input("What size of subset do you wish to use? "))
numDays = int(raw_input("How many days did the experiment last? "))

for val in range(1, fullSize+1):
    vec.append(val)

dataWidth = bootSize
dataHeight = numDays
data = np.zeros((dataWidth, dataHeight))

# generate random numbers for index from 1 thru fullSize 
for val in range(0,bootSize):
    index.append()