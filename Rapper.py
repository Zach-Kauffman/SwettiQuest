from typing import Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json

UserID = str
Dollars = int
Strain = str
Grams = float
LoudPack = Dict[Strain, Grams]

@dataclass_json
@dataclass
class Rapper:
    uid: UserID
    money: Dollars
    weed: LoudPack

    def addMoney(self, dollaz):
        self.money += dollaz

    def addWeed(self, strain, grams):
        if(strain in self.weed):
            self.weed[strain]+=grams
        else:
            self.weed[strain]=grams