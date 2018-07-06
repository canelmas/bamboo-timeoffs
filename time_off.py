from datetime import datetime, date

DATE_FORMAT_BAMBOO = "%Y-%m-%d"
DATE_FORMAT_EMAIL = "%d %B %A %Y"


class TimeOff:
    def __init__(self, data):
        self.start = datetime.strptime(data['start'], DATE_FORMAT_BAMBOO)
        self.end = datetime.strptime(data['end'], DATE_FORMAT_BAMBOO)
        self.dates = data['dates']
        self.status = data['status']['status']
        self.amount = float(data['amount']['amount'])
        self.employee = data['name']

    def to_html(self):
        return "<td>{} day</td><td>{}</td>".format(self.amount, self.start) \
            if self.amount < 1 else "<td>{} days</td><td>{} -> {}</td>".format(self.amount,
                                                                               datetime.strftime(self.start,
                                                                                                 DATE_FORMAT_EMAIL),
                                                                               datetime.strftime(self.end,
                                                                                                 DATE_FORMAT_EMAIL))

    def is_passed(self):
        return datetime.now() > datetime(date.today().year, date.today().month, date.today().day, 23, 59, 59)

    def __str__(self) -> str:
        return "name={}, amount={}, status={} start={} end={}".format(self.employee, self.amount, self.status,
                                                                      self.start,
                                                                      self.end)
