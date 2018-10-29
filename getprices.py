#!/usr/bin/python
#TODO: add logic that checks for the presence of a fourth row after color for "Printing." If such a row exists, it checks only the price
#for that particular printing, and adds that to the spreadsheet. If no such row exists, it does what it does now, which is to just
#check the most recent printing of the card.

import requests, csv, sys, time, json

#print usage if i fuck up
if len(sys.argv)<2:
    print ("usage: python3 getprices.py input.csv(three columns, names, quantity, color. color can be in whatever format you like.)")
    sys.exit()

#declaring variables
cardlist=[]
cardquantity=[]
cardcolor=[]
cardprices={}
total=[]
notes={}


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
    if r.status_code==200:
        #This only gets the price of the most recent printing of the card. If the most recent printing of the card was online-only, there won't be a USD value listed.
        #This could be fixed by adding logic to get only the specific printing of the card.
        if "usd" in json.loads(requests.get("https://api.scryfall.com/cards/search?q="+cardname).text)["data"][0]:
            cardprices[cardname] = float(json.loads(r.text)["data"][0]["usd"])
        else:
            print("usd not listed for "+cardname+", adding price as 0")
            cardprices[cardname]=0
            notes[cardname]="USD was not listed for this card."
    else:
        print("couldn't find "+cardname+"online, check that you spelled it correctly")
        cardprices[cardname]=0
        notes[cardname]="We couldn't find this card online. Check spelling."
    print(cardname+" : "+str(cardprices[cardname]))
    time.sleep(.1)


#spit out updated csv.
with open("prices_of_"+sys.argv[1], "w") as csvfile:
    cardwriter=csv.writer(csvfile)
    cardwriter.writerow(["name", "quantity", "color", "price", "total"])
    for i in range(len(cardlist)):
        #Check if there aree any notes for the key. if so, write them. If not, don't try to write something that doesn't exist.
        if cardlist[i] in notes.keys():
            cardwriter.writerow([cardlist[i], cardquantity[i], cardcolor[i], cardprices[cardlist[i]], cardprices[cardlist[i]]*float(cardquantity[i]), notes[cardlist[i]]])
        else:
            cardwriter.writerow([cardlist[i], cardquantity[i], cardcolor[i], cardprices[cardlist[i]], cardprices[cardlist[i]]*float(cardquantity[i])])
        total.append(cardprices[cardlist[i]]*float(cardquantity[i]))
    cardwriter.writerow(["", "", "", "", str(sum(total))])

#print out total value of collection.
print(str(sum(total)))
