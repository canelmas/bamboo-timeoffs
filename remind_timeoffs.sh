#!/usr/bin/env bash

# read team structures from file
#python3 ~/bamboo-timeoff-reminder/send_timeoff_reminders.py --config ~/bamboo-timeoff-reminder/config-prod.ini --teams ~/bamboo-timeoff-reminder/teams/

# use tempo api to fetch project teams
python3 ~/bamboo-timeoff-reminder/send_timeoff_reminders.py --config ~/bamboo-timeoff-reminder/config-prod.ini --recipients ~/bamboo-timeoff-reminder/recipients-prod.json