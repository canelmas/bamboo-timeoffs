import datetime
from datetime import datetime
from dateutil.relativedelta import *

from project_team import ProjectTeam

SUBJECT = "Time Off Reminder for the project team '{}'"
FROM = "timeoffreminder@commencis.com"
TIME_OFF_MONTH = "in {}"


class TimeOffReminder:

    def __init__(self, project_team: ProjectTeam) -> None:
        self.subject = SUBJECT.format(project_team.name)
        self.fromm = FROM
        self.to = [report_to for report_to in project_team.reports]
        self.members = [member for member in project_team.members]

    def as_email(self):
        return self.subject, self.fromm, self.to, self.__format_timeoffs(self.members)

    def __format_timeoffs(self, members):

        content_this_month = self.start_a_month(datetime.now())
        content_next_month = self.start_a_month(datetime.now() + relativedelta(months=1))

        for member in members:

            if member.time_offs:
                time_offs_this_month = member.get_time_offs_this_month()

                if time_offs_this_month:
                    self.has_time_off(content_this_month, member)

                    for t in time_offs_this_month:
                        self.add_time_off(content_this_month, t)
                else:
                    self.no_time_off(content_this_month, member)

                time_offs_next_month = member.get_time_offs_next_month()

                if time_offs_next_month:
                    self.has_time_off(content_next_month, member)

                    for t in time_offs_next_month:
                        self.add_time_off(content_next_month, t)
                else:
                    self.no_time_off(content_next_month, member)

            else:
                self.no_time_off(content_this_month, member)
                self.no_time_off(content_next_month, member)

        self.end_a_month(content_this_month)
        self.end_a_month(content_next_month)

        return ''.join(content_this_month)

    @staticmethod
    def no_time_off(content, employee):
        content.append("<tr><td>{}</td><td> - </td><td>{}</td></tr>".format(
            employee.fullname if employee.fullname else employee.email, "None"))

    @staticmethod
    def start_a_month(datetime):
        return ["<table><tr><th>{}</th><th></th><th></th><th></th></tr>".format(
            TIME_OFF_MONTH.format(datetime.strftime("%B")))]

    @staticmethod
    def end_a_month(content):
        content.append("</table>")

    @staticmethod
    def add_time_off(content, time_off):
        content.append("<tr><td></td><td></td>{}</tr>".format(time_off.to_html()))

    @staticmethod
    def has_time_off(content, employee):
        content.append(
            "<tr><td>{}</td><td></td><td></td></tr>".format(employee.fullname if employee.fullname else employee.email))
