import argparse
import configparser
from datetime import datetime

from dateutil.relativedelta import relativedelta

from bamboo_hr_api import API
from email_util import EmailUtil
from employee import Employee
import os
import re
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from project_team import ProjectTeam
from time_off_reminder import TimeOffReminder
from time_off import TimeOff

COMMA_DELIMITER = re.compile(''',(?=(?:[^"]*"[^"]*")*[^"]*$)''')


def fetch_project_teams():
    project_teams = []

    for team in os.listdir("teams"):

        project_team = ProjectTeam(team)

        with open(os.path.join("teams", team)) as f:
            for line in f:
                if not line.startswith("#") and line.find("=") != -1:
                    fields = COMMA_DELIMITER.split(line[line.index("=") + 1:])
                    # fields = line[line.index("=") + 1:].split(",")
                    if line.startswith("team"):
                        project_team.set_working_members(fields)
                    elif line.startswith("report"):
                        project_team.set_reporting_members(fields)
            project_teams.append(project_team)

    return project_teams


def update_employee_info(employee: Employee, employee_directory):
    for item in employee_directory:
        if item['workEmail'] == employee.email:
            employee.id = item['id']
            employee.fullname = item['displayName']


def format_date(datetime: datetime):
    return datetime.strftime("%Y-%m-%d")


def get_employee_timeoffs(api: API, employee_id):
    now = datetime.now()
    two_months_from_now_on = now + relativedelta(months=2)
    return api.get_employee_time_offs(employee_id, format_date(now), format_date(two_months_from_now_on))


def fetch_timeoff(api: API, employee: Employee):
    if employee.id:
        timeoffs = get_employee_timeoffs(api, employee.id)

        for data in timeoffs:
            employee.add_time_off(TimeOff(data))
    else:
        print("Can't fetch timeoff data for {}; employee id not set!".format(employee.email))


def send_reminder(project_team):
    EmailUtil.send(TimeOffReminder(project_team).as_email())


def remind_timeoffs(sub_domain, api_key):
    print(sub_domain)
    print(api_key)
    project_teams = fetch_project_teams()

    if project_teams:

        bamboo_api = API(sub_domain, api_key)
        employee_directory = bamboo_api.get_list_of_employees()

        for team in project_teams:
            for employee in team.members:
                update_employee_info(employee, employee_directory)
                fetch_timeoff(bamboo_api, employee)

            send_reminder(team)
    else:
        print("No project team found!")


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Timeoff Reminder CLI")
    arg_parser.add_argument("--config", help="configuration file", required=True)
    args = arg_parser.parse_args()

    config_parser = configparser.ConfigParser()
    config_parser.read(args.config)

    if 'bamboo' not in config_parser.sections():
        raise ValueError("No 'bamboo' configuration found. Make sure to set 'API_KEY' and 'SUBDOMAIN' in your "
                         "'bambbo' section of your configuration.")

    remind_timeoffs(config_parser['bamboo']['SUB_DOMAIN'], config_parser['bamboo']['API_KEY'])
