from typing import Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json

UserID = int
Dollars = float
Title = str
Tier = str
Quant = float
DrugName = str
DrugBag = Dict[DrugName, Dict[Tier, Quant]]
Music = float

@dataclass_json
@dataclass
class Rapper:
    uid: UserID
    name: Title
    money: Dollars
    drugs: DrugBag
    moneyPerShow: Music

    def addMoney(self, dollaz):
        self.money += dollaz

    def addDrug(self, category:str, tier:int, quant):
        if(self.drugs[category]):
            drug = self.drugs[category]
            if(tier in drug):
                self.drugs[category][tier]+=quant
        else:
            self.drugs[category][tier]=quant

    def hasDrug(self, category):
        for tier in self.drugs[category]:
            if self.drugs[category][tier] > 0:
                return True
        return False

    def ownedTiersOfDrug(self, category):
        tiers = []
        for tier in self.drugs[category]:
            if self.drugs[category][tier] > 0:
                tiers.append(tier)
        return tiers


    def bestTierOfDrug(self, category):
        if self.hasDrug(category):
            bestdrug = 0.0
            for tier in self.drugs[category]:
                if float(tier) > bestdrug and self.drugs[category][tier] > 0:
                    bestdrug = float(tier)
            return bestdrug
        return None

    def improveMusic(self, amount):
        self.moneyPerShow += amount