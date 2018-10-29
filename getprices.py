#!/usr/bin/python

import requests, csv, sys, time, json

#print usage if i fuck up
if len(sys.argv)<2:
    print ("usage: python3 getprices.py input.csv")
    sys.exit()

#declaring variables
cardlist=[]
cardquantity=[]
cardcolor=[]
cardprices={}
total=[]

#read in the .csv
with open(sys.argv[1]) as csvfile:
    cardreader=csv.reader(csvfile, delimiter=",")
    for row in cardreader:
        cardlist.append(row[0])
        cardquantity.append(row[1])
        cardcolor.append(row[2])
cardlist=cardlist[1:]
cardquantity=cardquantity[1:]
cardcolor=cardcolor[1:]

#fetch prices from Scryfall
for cardname in cardlist:
    r=requests.get("https://api.scryfall.com/cards/search?q="+cardname)
    if "usd" in json.loads(requests.get("https://api.scryfall.com/cards/search?q="+cardname).text)["data"][0]:
        cardprices[cardname] = float(json.loads(r.text)["data"][0]["usd"])
    else:
        print("usd not listed for "+cardname+", adding price as 0")
        cardprices[cardname]=0
    print(cardname+" : "+str(cardprices[cardname]))
    time.sleep(.1)

#print("usd" in json.loads(requests.get("https://api.scryfall.com/cards/search?q=Spike Feeder").text)["data"][0])


#spit out updated csv.
with open("prices_of_"+sys.argv[1], "w") as csvfile:
    cardwriter=csv.writer(csvfile)
    cardwriter.writerow(["name", "quantity", "color", "price", "total"])
    for i in range(len(cardlist)):
        cardwriter.writerow([cardlist[i], cardquantity[i], cardcolor[i], cardprices[cardlist[i]], cardprices[cardlist[i]]*float(cardquantity[i])])
        total.append(cardprices[cardlist[i]]*float(cardquantity[i]))
    cardwriter.writerow(["", "", "", "", str(sum(total))])

print(str(sum(total)))
