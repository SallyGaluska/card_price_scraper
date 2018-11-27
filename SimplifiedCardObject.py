class Card:
    def __init__(self, name, setCode, quantity=1):
        self.name=name
        self.setCode=setCode
        self.quantity=quantity
    def setPrice(self, price):
        self.price=price
    def setNote(self, note):
        self.note=note