import time_off

from datetime import datetime
from dateutil.relativedelta import relativedelta


class Employee:

    def __init__(self, email) -> None:
        self.email = email
        self.id = -1
        self.time_offs = []
        self.fullname = None
        self.photoUrl = None

    def add_time_off(self, timeoff: time_off):
        self.time_offs.append(timeoff)

    def get_time_offs_this_month(self):
        return None if not self.time_offs else list(
            filter(lambda t: t.start.month == datetime.today().month
                             and not t.is_passed()
                             and t.status in time_off.STATUS_LIST_TO_DISPLAY, self.time_offs))

    def get_time_offs_next_month(self):
        return None if not self.time_offs else list(
            filter(lambda t: t.start.month == (datetime.now() + relativedelta(months=1)).month
                             and t.status in time_off.STATUS_LIST_TO_DISPLAY, self.time_offs))

    def __str__(self) -> str:
        return "email={} fullname= {} id={} timeoffs={}".format(self.email, self.fullname, self.id, self.time_offs)
