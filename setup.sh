#!/usr/bin/env bash

sudo apt install python3-pip

pip3 install -r requirement.txt

cmd="/home/terryadmin/bamboo-timeoff-reminder/remind_timeoffs.sh"
job="0 6 * * MON $cmd"

( crontab -l | grep -v -F "$cmd" ; echo "$job" ) | crontab -