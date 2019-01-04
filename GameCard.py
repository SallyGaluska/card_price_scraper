class GameCard:
    def __init__(self, layout, name):
        self.layout=layout
        self.name=name
class UnaryCard(GameCard):
    def __init__(self, layout, name, CMC, manaCost, oracleText, typeLine, power="", toughness=""):
        GameCard.__init__(self, layout, name)
        self.CMC=CMC
        self.manaCost=manaCost
        self.oracleText=oracleText
        self.typeLine=typeLine
        if power=="":
            self.isCreature=False
        else:
            self.isCreature=True
            self.power=power
            self.toughness=toughness
class BinaryCard(GameCard):
    def __init__(self, layout, name, name0, CMC, manaCost, oracleText, typeLine, name1, CMC1, manaCost1, oracleText1, typeLine1, power="", toughness="", power1="", toughness1=""):
        GameCard.__init__(self, layout, name)
        self.faces=[]
        self.faces.append(UnaryCard("normal", name0, CMC, manaCost, oracleText, typeLine, power, toughness))
        self.faces.append(UnaryCard("normal", name1, CMC1, manaCost1, oracleText1, typeLine1, power1, toughness1))
    def __getitem__(self, key):
        return self.faces[key]

LightningBolt=UnaryCard("normal", "Lightning Bolt", 1, "R", "Lightning Bolt deals 3 damage to any target.", "Instant")
print(LightningBolt.oracleText)
DuskwatchRecruiter=BinaryCard("transform", "Duskwatch Recruiter//Krallenhorde Howler", "Duskwatch Recruiter", 2, "1G", "humanduder", "Creature - Human Warrior Werewolf", "Krallenhorde Howler", 2, "1G", "werewolfshit", "Creature - Werewolf", 2, 2, 3, 3)
print(DuskwatchRecruiter[0].typeLine)
