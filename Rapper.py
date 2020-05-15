from typing import Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json

UserID = int
Dollars = int
Tier = str
Grams = int
LoudPack = Dict[Tier, Grams]
Music = int

@dataclass_json
@dataclass
class Rapper:
    uid: UserID
    money: Dollars
    weed: LoudPack
    moneyPerShow: Music

    def addMoney(self, dollaz):
        self.money += dollaz

    def addWeed(self, tier:int, grams):
        if(tier in self.weed):
            self.weed[tier]+=grams
        else:
            self.weed[tier]=grams

    def hasWeed(self):
        for tier in self.weed:
            if self.weed[tier] > 0:
                return True
        return False

    def ownedTiersOfWeed(self):
        strains = []
        for tier in self.weed:
            if self.weed[tier] > 0:
                strains.append(tier)
        return strains


    def bestWeed(self):
        if self.hasWeed():
            bestweed = 0
            for tier in self.weed:
                if int(tier) > bestweed and self.weed[tier] > 0:
                    bestweed = int(tier)
            return bestweed
        return None

    def improveMusic(self, amount):
        self.moneyPerShow += amount