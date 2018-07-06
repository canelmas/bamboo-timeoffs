from datetime import datetime


class TimeOff:
    def __init__(self, data):
        self.start = datetime.strptime(data['start'], "%Y-%m-%d")
        self.end = datetime.strptime(data['end'], "%Y-%m-%d")
        self.dates = data['dates']
        self.status = data['status']['status']
        self.amount = int(data['amount']['amount'])
        self.employee = data['name']

    def to_html(self):
        return "<td>{} day</td><td>{}</td>".format(self.amount, self.start) \
            if self.amount < 1 else "<td>{} days</td><td>{} -> {}</td>".format(self.amount, self.start, self.end)

    def __str__(self) -> str:
        return "name={}, amount={}, status={} start={} end={}".format(self.employee, self.amount, self.status,
                                                                      self.start,
                                                                      self.end)
