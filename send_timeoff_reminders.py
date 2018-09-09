import argparse
import configparser
import os
import json
import re

from datetime import datetime
from dateutil.relativedelta import relativedelta
from rx import Observable

from bamboo_hr_api import BambooHRApi
from email_util import EmailUtil, SMTPConfig
from employee import Employee
from project_team import ProjectTeam
from tempo_api import TempoApi
from time_off_reminder import TimeOffReminder
from time_off import TimeOff
from logger import get_logger

REG_PATTERN_PROJECT_TEAM = re.compile("PT\s(.*)")
REG_PATTERN_FUNCTIONAL_TEAM = re.compile("FT\s((.+)-(\d+))")

log = get_logger()

time_off_cache = {}


def read_and_populate_project_teams(project_team_folder):
    project_teams = []

    for team in os.listdir(project_team_folder):

        project_team = ProjectTeam(team)

        with open(os.path.join(project_team_folder, team)) as f:
            for line in f:
                if line.find("=") != -1:
                    fields = line[line.index("=") + 1:].split(',')
                    if line.startswith("team"):
                        project_team.set_working_members(fields)
                    elif line.startswith("report"):
                        project_team.set_reporting_members(fields)
            project_teams.append(project_team)

    return project_teams


def append_employee_info(employee: Employee, employee_directory):
    for item in employee_directory:
        if item['workEmail'] == employee.email:
            employee.id = item['id']
            employee.fullname = item['displayName']
            employee.photoUrl = item['photoUrl']
            break


def append_employee_time_offs(employee: Employee, api: BambooHRApi):
    if employee.id != -1:

        time_offs = get_employee_time_offs(api, employee.id)

        for time_off_data in time_offs:
            employee.add_time_off(TimeOff(time_off_data, employee.photoUrl, employee.id))
    else:
        log.debug("Can't fetch timeoff data for {}; employee id not set!".format(employee.email))


def get_employee_time_offs(api: BambooHRApi, employee_id):
    if employee_id not in time_off_cache.keys():
        time_off_cache[employee_id] = fetch_employee_time_offs(api, employee_id)

    return time_off_cache.get(employee_id)


def fetch_employee_time_offs(api: BambooHRApi, employee_id):
    now = datetime.now()
    two_months_from_now_on = now + relativedelta(months=2)
    return api.get_employee_time_offs(employee_id, now, two_months_from_now_on)


def send_reminder(project_team, smtp_config):
    log.info("reminding \"{}\" timeoffs to \"{}\"".format(project_team.name, project_team.reports))
    EmailUtil.send(TimeOffReminder(project_team).as_email(), smtp_config)


def read_project_team_files_and_remind(smtp_config, bamboo_api):
    project_teams = read_and_populate_project_teams(project_team_folder)

    if project_teams:
        employee_directory = bamboo_api.get_list_of_employees()

        for team in project_teams:
            for employee in team.members:
                append_employee_info(employee, employee_directory)
                append_employee_time_offs(employee, bamboo_api)

            send_reminder(team, smtp_config)
    else:
        log.debug("No project team found.")


def is_team_member_active(member):
    return member["member"]["activeInJira"]


def get_commencis_email(member_full_name):
    return "{}@commencis.com".format(member_full_name)


def append_team_members(team: ProjectTeam, tempo_api):
    team_members = tempo_api.get_team_members(team.id)
    team_member_emails = list(filter(is_team_member_active, team_members))
    team_member_emails = list(map(lambda member: get_commencis_email(member["member"]["name"]), team_member_emails))
    team.set_working_members(team_member_emails)
    return Observable.create(lambda obs: obs.on_next(team))


def append_team_member_details(team: ProjectTeam, employee_directory):
    for employee in team.members:
        append_employee_info(employee, employee_directory)
    return team


def append_team_time_offs(team: ProjectTeam, bamboo_api):
    for employee in team.members:
        if employee.id != -1:
            time_offs = get_employee_time_offs(bamboo_api, employee.id)
            for time_off_data in time_offs:
                employee.add_time_off(TimeOff(time_off_data, employee.photoUrl, employee.id))
    return team


def filter_teams(team):
    return REG_PATTERN_FUNCTIONAL_TEAM.match(team["name"]) or REG_PATTERN_PROJECT_TEAM.match(team["name"])


def fetch_project_teams_and_remind(smtp_config, bamboo_api, tempo_api):
    employee_directory = bamboo_api.get_list_of_employees()

    Observable.from_list(tempo_api.get_all_teams()) \
        .filter(filter_teams) \
        .flat_map(lambda team: Observable.create(lambda obs: obs.on_next(ProjectTeam(team["name"],
                                                                                     get_commencis_email(team["lead"]),
                                                                                     team["id"])))) \
        .flat_map(lambda team: append_team_members(team, tempo_api)) \
        .map(lambda team: append_team_member_details(team, employee_directory)) \
        .map(lambda team: append_team_time_offs(team, bamboo_api)) \
        .subscribe(lambda team: send_reminder(team, smtp_config))


def remind_time_offs(config_smtp, config_bamboo, **kwargs):
    smtp_config = SMTPConfig(config_smtp['host'],
                             config_smtp['from'],
                             config_smtp['port'])

    bamboo_api = BambooHRApi(config_bamboo['sub_domain'],
                             config_bamboo['api_key'])

    if "tempo_api" in kwargs.keys():
        fetch_project_teams_and_remind(smtp_config, bamboo_api, TempoApi(kwargs.get("tempo_api")["url"],
                                                                         kwargs.get("tempo_api")["token"]))
    else:
        read_project_team_files_and_remind(smtp_config, bamboo_api)


def execute():
    arg_parser = argparse.ArgumentParser(description="BambooHR Time Off Reminder CLI")
    arg_parser.add_argument("--config", help="configuration file", required=True)
    arg_parser.add_argument("--teams", help="project teams folder path", required=False)
    args = arg_parser.parse_args()

    config_parser = configparser.ConfigParser()
    config_parser.read(args.config)

    if 'bamboo' not in config_parser.sections():
        raise KeyError("'bamboo' section missing. Make sure to set 'api_key' and 'sub_domain'.")

    if 'smtp' not in config_parser.sections():
        raise KeyError("'smtp' section missing. Make sure to set 'host', 'port' and 'from'.")

    if "tempo" in config_parser.sections():

        if "url" not in config_parser["tempo"]:
            raise KeyError("'url' missing under 'tempo' section. Please check configuration file.")

        if "token" not in config_parser["tempo"]:
            raise KeyError("'token' missing under 'tempo' section. Please check configuration file.")

        remind_time_offs(config_parser["smtp"],
                         config_parser["bamboo"],
                         tempo_api=config_parser["tempo"])

    else:
        remind_time_offs(config_parser['smtp'],
                         config_parser["bamboo"],
                         teams=args.teams)


if __name__ == "__main__":
    execute()
