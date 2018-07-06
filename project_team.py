from employee import Employee


class ProjectTeam:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.reports = []

    def set_working_members(self, members):
        for email in members:
            self.members.append(Employee(email))

    def set_reporting_members(self, reporting_members):
        for email in reporting_members:
            self.reports.append(Employee(email))

    def __str__(self) -> str:
        return "name={}, members={}, reports={}".format(self.name, self.members, self.reports)
