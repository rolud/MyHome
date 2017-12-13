class Home:
    # wrap class that contains an object House and an object ToBuyList
    # useful to simplify save and load operations
    def __init__(self):
        self.house = House()
        self.lst = ToBuyList()

    def get_house(self):
        return self.house

    def get_lst(self):
        return self.lst


class House:
    garbage = 0

    def __init__(self):
        self.housemates = {}
        self.housemates_by_name = {}
        # self.garbage = 0

    def add_hsm(self, hsm_id, hsm_name):
        hsm = Housemate(hsm_id, hsm_name)
        self.housemates.update({hsm_id: hsm})
        self.housemates_by_name.update({hsm_name: hsm})

    def is_hsm(self, hsm_id):
        return hsm_id in self.housemates

    def get_hsm_by_id(self, hsm_id):
        return self.housemates[hsm_id]

    def get_hsm_by_name(self, hsm_name):
        return self.housemates_by_name[hsm_name]

    def get_hsm_all(self):
        return self.housemates_by_name.keys()

    def set_garbage(self, garbage):
        if garbage:
            self.garbage += 1
        elif not garbage:
            self.garbage = 0

    def there_is_garbage(self):
        return self.garbage


class Housemate:
    def __init__(self, hsm_id, hsm_name):
        self.id = hsm_id
        self.name = hsm_name
        self.user = None

    def update_username(self, user):
        self.user = user

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_username(self):
        return self.user


class ToBuyList:
    def __init__(self):
        self.to_buy_list = []

    def add(self, obj):
        if obj != "" and obj not in self.to_buy_list:
            self.to_buy_list.append(obj.lower())
            return True
        return False

    def get_list(self):
        lst = self.to_buy_list.copy()
        for i in range(len(lst)):
            lst[i] = str(i+1) + ") " + lst[i].capitalize()
        res = "\n"
        return res.join(lst)

    def remove_all(self):
        self.to_buy_list.clear()

    def remove(self, obj):
        deleted = ""
        if obj.isdigit():
            ind = int(obj) - 1
            if ind >= len(self.to_buy_list):
                return "Elemento non presente."
            deleted = self.to_buy_list[ind]
            del(self.to_buy_list[ind])
        elif obj == "":
            if len(self.to_buy_list) > 0:
                return self.to_buy_list.pop()
        else:
            if obj.lower() not in self.to_buy_list:
                return "Elemento non presente."
            for o in self.to_buy_list:
                if o.lower() == obj.lower():
                    deleted = o
                    ind = self.to_buy_list.index(o)
                    del(self.to_buy_list[ind])
                    break
        return deleted

    def empty_list(self):
        if len(self.to_buy_list) == 0:
            return True
        else:
            return False
