#!/usr/bin/python

import requests
import csv
import sys

if len(sys.argv)<2:
    print ("usage: python3 getprices.py input.csv")

cardlist=[]

with open(sys.argv[1]) as csvfile:
    cardreader=csv.reader(csvfile, delimiter=",")
    for row in cardreader:
        cardlist.append(row[0])


