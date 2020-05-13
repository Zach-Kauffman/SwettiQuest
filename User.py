class User:
    id = None
    money = 0

    def __init__(self, id, user = None):
        self.id = id
        if(user):
            self.money = user.money
