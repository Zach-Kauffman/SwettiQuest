import json
from Rapper import Rapper
import os
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from dacite import from_dict

USER_DATA_PATH = 'userdata.json'

def saveUserData(users):
    json_dict = {key: user.to_dict() for key, user in users.items()}
    with open(USER_DATA_PATH, 'w') as f:
        # for key, user in users.items():
        #     f.write('{'+str(key)+': ' + str(user.to_dict()) + '}', f)
        json.dump(json_dict, f)

#loads dict of dicts, converts to dict of rappers
def loadUserData():
    users = json.load(open(USER_DATA_PATH, 'r'))
    rappers = {}
    for key, dic in users.items():
        rappers[int(key)] = from_dict(data_class=Rapper, data=dic)
    return rappers

def insertNewUser(users, user, save):
        if user.id not in users:
            users[user.id] = Rapper(uid=user.id, name=user.name, money=20.00, drugs={'weed':{},'stims':{},'boner':{}}, moneyPerShow=1)
            if save:
                saveUserData(users)
            return True
        return False