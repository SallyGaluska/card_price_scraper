#!/usr/bin/python
#TODO: add logic that checks for the presence of a fourth row after color for "Printing." If such a row exists, it checks only the price
#for that particular printing, and adds that to the spreadsheet. If no such row exists, it does what it does now, which is to just
#check the most recent printing of the card.

import requests, csv, sys, time, json
from SimplifiedCardObject import Card

def checkProperArgsExist():
    if len(sys.argv)<2:
        print ("usage: python3 getprices.py input.csv(name, setcode, quantity.)")
        sys.exit()

def getCardList():
    cardList=[]
    with open(sys.argv[1]) as csvfile:
        cardreader=csv.reader(csvfile, delimiter=",")
        for row in cardreader:
            cardList.append(Card(row))
    del cardList[0]
    return cardList

def getPriceFromScryfall(CardList):
    r=requests.get("https://api.scryfall.com/cards/named?exact="+card.name+"&set="+card.setCode)
    if r.status_code==200:
        ScryfallData=(json.loads(r.text))
        if "usd" in ScryfallData:
            return float(ScryfallData["usd"])
        else:
            print("usd not listed for "+card.setCode+" "+card.name+", adding price as 0")
            return 0
    else:
        print("couldn't find "+card.setCode+" "+card.name+" online, check that you spelled it correctly")
        return 0

def createCSVWithPrices(CardList):
    with open("prices_of_"+sys.argv[1], "w") as csvfile:
        cardwriter=csv.writer(csvfile)
        cardwriter.writerow(["name", "set", "quantity", "price", "notes"])
        for card in CardList:
            out=createOutputList(card)
            cardwriter.writerow(out)

def createOutputList(card):
    if hasattr(card, 'note'):
        return [card.name, card.setCode, card.quantity, card.price, card.note]
    else:
        return [card.name, card.setCode, card.quantity, card.price]


if __name__=="__main__":
    checkProperArgsExist()
    CardList=getCardList()
    for card in CardList:
        card.setPrice(getPriceFromScryfall(card))
        print(card.name+" : "+str(card.price))
    createCSVWithPrices(CardList)
