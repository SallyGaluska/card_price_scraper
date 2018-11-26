class Card:
    def __init__(self, inList):
        self.name=inList[0]
        self.setCode=inList[1]
        self.quantity=inList[2]
    def setPrice(self, price):
        self.price=price
    def addNote(self, note):
        self.note=note