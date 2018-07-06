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


def fetch_project_teams(project_team_folder):
    project_teams = []

    for team in os.listdir(project_team_folder):

        project_team = ProjectTeam(team)

        with open(os.path.join(project_team_folder, team)) as f:
            for line in f:
                if line.find("=") != -1:
                    fields = COMMA_DELIMITER.split(line[line.index("=") + 1:])
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


def get_employee_time_offs(api: API, employee_id):
    now = datetime.now()
    two_months_from_now_on = now + relativedelta(months=2)
    return api.get_employee_time_offs(employee_id, now, two_months_from_now_on)


def fetch_employee_time_off(api: API, employee: Employee):
    if employee.id:
        time_offs = get_employee_time_offs(api, employee.id)

        for time_off_data in time_offs:
            employee.add_time_off(TimeOff(time_off_data))
    else:
        print("Can't fetch timeoff data for {}; employee id not set!".format(employee.email))


def send_reminder(project_team):
    EmailUtil.send(TimeOffReminder(project_team).as_email())


def remind_time_offs(project_team_folder, bamboo_api):
    project_teams = fetch_project_teams(project_team_folder)

    if project_teams:
        employee_directory = bamboo_api.get_list_of_employees()

        for team in project_teams:
            for employee in team.members:
                update_employee_info(employee, employee_directory)
                fetch_employee_time_off(bamboo_api, employee)

            send_reminder(team)
    else:
        print("No project team found!")


if __name__ == "__main__":

    arg_parser = argparse.ArgumentParser(description="Timeoff Reminder CLI")
    arg_parser.add_argument("--config", help="configuration file", required=True)
    arg_parser.add_argument("--teams", help="project teams folder", required=True)
    args = arg_parser.parse_args()

    config_parser = configparser.ConfigParser()
    config_parser.read(args.config)

    if 'bamboo' not in config_parser.sections():
        raise ValueError("No 'bamboo' configuration found. Make sure to set 'API_KEY' and 'SUBDOMAIN' in your "
                         "'bambbo' section of your configuration.")

    remind_time_offs(args.teams, API(config_parser['bamboo']['SUB_DOMAIN'], config_parser['bamboo']['API_KEY']))
