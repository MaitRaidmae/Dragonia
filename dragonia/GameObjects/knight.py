class Knight:

    def __init__(self, knight_dict):
        self.knight_dict = knight_dict

    @property
    def name(self):
        return self.knight_dict['name']

    @property
    def armor(self):
        return self.knight_dict['armor']

    @property
    def attack(self):
        return self.knight_dict['attack']

    @property
    def agility(self):
        return self.knight_dict['agility']

    @property
    def endurance(self):
        return self.knight_dict['endurance']

    @property
    def description(self):
        if self.armor > 7:
            return "The knight looks to be heavily armoured."
        elif self.attack > 7:
            return "The knight looks to be well armed."
        elif self.agility > 7:
            return "The knight looks to be quick on his/her feet."
        elif self.endurance > 7:
            return "The knight looks to be very well built."
        else:
            return "The knight looks to be well rounded."

