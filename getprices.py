#!/usr/bin/python
import requests, sys, time, json, csv
from SimplifiedCardObject import Card

def main():
    checkProperArgsExist()
    CardList=getCardList()
    for card in CardList:
        card.setPrice(getPriceFromScryfall(card))
        print(card.name+" : "+str(card.price))
    createCSVWithPrices(CardList)
    print("Your collection is worth $"+str(getSumOfCardPrices(CardList))+".")

def checkProperArgsExist():
    if len(sys.argv)<2:
        print ("usage: python3 getprices.py input.csv(name, setcode, quantity.)")
        sys.exit()

def getCardList():
    cardList=[]
    with open(sys.argv[1]) as csvfile:
        cardreader=csv.reader(csvfile, delimiter=",")
        for row in cardreader:
            cardList.append(Card(row[0], row[1], row[2]))
    del cardList[0] #The first row just has the headers. name, set, quantity...
    return cardList

def getPriceFromScryfall(card):
    if card.setCode=="":
        getPriceForMostRecentPrinting(card)
    r=requests.get("https://api.scryfall.com/cards/named?exact="+card.name+"&set="+card.setCode)
    if r.status_code==200:
        ScryfallData=json.loads(r.text)
        return extractPriceFromScryfallData(ScryfallData)
    else:
        return getPriceForMostRecentPrinting(card)

def extractPriceFromScryfallData(ScryfallData):
    if "usd" in ScryfallData:
        return float(ScryfallData["usd"])
    else:
        card.setNote("No USD listed for "+card.setCode+" "+card.name+". If you didn't put a correct setcode, we guessed the most recent one, and it was online-only.")
        return 0

def getPriceForMostRecentPrinting(card):
    r=requests.get("https://api.scryfall.com/cards/named?exact="+card.name)
    if r.status_code==200:
        ScryfallData=json.loads(r.text)
        card.setCode=ScryfallData["set"]
        return extractPriceFromScryfallData(ScryfallData)
    else:
        card.setNote("We couldn't find "+card.name+". Check spelling.")
        return 0

def createCSVWithPrices(CardList):
    with open("prices_of_"+sys.argv[1], "w") as csvfile:
        for card in CardList:
            out=createOutputList(card)
            csvfile.write('"'+('","'.join(out))+'"\n"')

def createOutputList(card):
    if hasattr(card, 'note'):
        return [card.name, card.setCode, str(card.quantity), str(card.price), card.note]
    else:
        return [card.name, card.setCode, str(card.quantity), str(card.price)]

def getSumOfCardPrices(CardList):
    prices=0
    for card in CardList:
        prices+=int(card.price)*int(card.quantity)
    return prices

if __name__=="__main__":
    main()
