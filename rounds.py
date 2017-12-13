import time
from house import House


class Round:
    data = {}
    t1 = ("rolud", "Bruno", "Fabrizio")
    t2 = ("Jenko😎", "rolud", "Bruno")
    t3 = ("Fabrizio", "Jenko😎", "rolud")
    t4 = ("Bruno", "Fabrizio", "Jenko😎")
    rnds = {'Tue': 1, 'Thu': 2, 'Sat': 3, 'Sun': 3,
            1: 'Bagno', 2: 'Bagno e cucina', 3: 'Casa'}

    def select_round(self, string):
        turn = ()
        if string == 'T1':
            turn = self.t1
        elif string == 'T2':
            turn = self.t2
        elif string == 'T3':
            turn = self.t3
        elif string == 'T4':
            turn = self.t4
        return turn

    def load(self):        # uploads database from a file
        if len(self.data) == 0:                # the database is saved in a dict
            for line in open("rounds.data"):  # key: tuple (int year, int week) - value: str round
                ln = line.split()
                yr, wk, rnd = ln
                self.data.update({(int(yr), int(wk)): rnd})

    @staticmethod
    def is_round_day():  # return True if today is a round day
        day = time.strftime("%a", time.gmtime())
        if day == "Tue" or day == "Thu" or day == "Sat" or day == "Sun":
            return True
        return False

    def today(self):  # return hsm_name of who have to clean today
        yr, wk = int(time.strftime('%y', time.gmtime())), int(time.strftime('%W', time.gmtime()))
        day = time.strftime("%a", time.gmtime())
        frst, scnd, thrd = self.select_round(self.data[(yr,wk)])
        res = 0
        try:
            t = self.rnds[day]
            if t == 1:
                res = frst
            elif t == 2:
                res = scnd
            elif t == 3:
                res = thrd
        except KeyError:
            res = None
        return res

    def today_round(self, hs):  # return a string with the round of today
        day = time.strftime("%a", time.gmtime())
        hsm_name = self.today()
        if hsm_name is None:
            string = time.strftime("%a, %d %b %Y", time.gmtime()) + "\n\nOggi non c'è nessun turno."
        else:
            try:
                hsm = hs.get_hsm_by_name(hsm_name)
                rnd = self.rnds[day]
                usr = hsm.get_username()
                if usr is None:
                    usr = hsm.get_name()
                string = time.strftime("%a, %d %b %Y", time.gmtime()) + "\n\n" + self.rnds[rnd] + ":\n" + usr
            except KeyError:
                rnd = self.rnds[day]
                string = time.strftime("%a, %d %b %Y", time.gmtime()) + "\n\n" + self.rnds[rnd] + ":\n" + hsm_name
        return string

    def week_round(self, hs):
        yr, wk = int(time.strftime('%y', time.gmtime())), int(time.strftime('%W', time.gmtime()))
        frst, scnd, thrd = self.select_round(self.data[(yr, wk)])
        try:
            hsm = hs.get_hsm_by_name(frst)
            if hsm.get_username() is not None: frst = hsm.get_username()
        except KeyError:
            pass
        try:
            hsm = hs.get_hsm_by_name(scnd)
            if hsm.get_username() is not None: scnd = hsm.get_username()
        except KeyError:
            pass
        try:
            hsm = hs.get_hsm_by_name(thrd)
            if hsm.get_username() is not None: thrd = hsm.get_username()
        except KeyError:
            pass
        string = (time.strftime("%a, %d %b %Y", time.gmtime()) +
                  "\n\nMartedì (bagno):\n"+frst+
                  "\n\nGiovedì (bagno e cucina):\n"+scnd+
                  "\n\nSabato o Domenica (casa):\n"+thrd)
        return string

    def next_week_round(self, hs):
        yr, wk = int(time.strftime('%y', time.gmtime())), int(time.strftime('%W', time.gmtime()))
        if wk == 52:
            wk = 0
        else:
            wk += 1
        frst, scnd, thrd = self.select_round(self.data[(yr, wk)])
        try:
            hsm = hs.get_hsm_by_name(frst)
            if hsm.get_username() is not None: frst = hsm.get_username()
        except KeyError:
            pass
        try:
            hsm = hs.get_hsm_by_name(scnd)
            if hsm.get_username() is not None: scnd = hsm.get_username()
        except KeyError:
            pass
        try:
            hsm = hs.get_hsm_by_name(thrd)
            if hsm.get_username() is not None: thrd = hsm.get_username()
        except KeyError:
            pass
        string = (time.strftime("%a, %d %b %Y", time.gmtime()) +
                  "\n\nMartedì (bagno):\n"+frst+
                  "\n\nGiovedì (bagno e cucina):\n"+scnd+
                  "\n\nSabato o Domenica (casa):\n"+thrd)
        return string
