from datetime import datetime

from dateutil.relativedelta import relativedelta

import time_off


class Employee:
    def __init__(self, email):
        self.email = email
        self.id = -1
        self.time_offs = []
        self.fullname = ""

    def add_time_off(self, timeoff: time_off):
        self.time_offs.append(timeoff)

    def get_time_offs_this_month(self):
        return None if not self.time_offs else list(
            filter(lambda t: t.start.month == datetime.today().month and not t.is_passed(), self.time_offs))

    def get_time_offs_next_month(self):
        return None if not self.time_offs else list(
            filter(lambda t: t.start.month == (datetime.now() + relativedelta(months=1)).month, self.time_offs))

    def __str__(self) -> str:
        return "email={} fullname= {} id={} timeoffs={}".format(self.email, self.fullname, self.id, self.time_offs)
