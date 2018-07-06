from validate_email import validate_email

from employee import Employee


class ProjectTeam:
    def __init__(self, name):
        self.name = name
        self.members = []
        self.reports = []

    def set_working_members(self, emails):
        self.__add_employee(emails, self.members)

    def set_reporting_members(self, emails):
        self.__add_employee(emails, self.reports)

    def __add_employee(self, employee_emails, employee_list):
        for email in employee_emails:
            email = email.strip(' \t\n\r')
            if validate_email(email):
                employee_list.append(Employee(email))

    def __str__(self) -> str:
        return "name={}, members={}, reports={}".format(self.name, self.members, self.reports)
