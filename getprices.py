#!/usr/bin/python
import requests, csv, sys, time, json
from SimplifiedCardObject import Card

def main():

    checkProperArgsExist()
    CardList=getCardList()
    for card in CardList:
        card.setPrice(getPriceFromScryfall(card))
        print(card.name+" : "+str(card.price))
    createCSVWithPrices(CardList)

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

def getPriceFromScryfall(card):
    r=requests.get("https://api.scryfall.com/cards/named?exact="+card.name+"&set="+card.setCode)
    if r.status_code==200:
        ScryfallJSON=r.text
        return extractPriceFromScryfallJSON(ScryfallJSON)
    else:
        card.setNote("Couldn't find this card/set combination. Check that you put the right set, and check spelling.")
        return 0
        
def extractPriceFromScryfallJSON(ScryfallJSON):
    ScryfallData=(json.loads(ScryfallJSON))
    if "usd" in ScryfallData:
        return float(ScryfallData["usd"])
    else:
        card.setNote("Couldn't find USD for this card. You may have chosen an online-only printing.")
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
    main()
