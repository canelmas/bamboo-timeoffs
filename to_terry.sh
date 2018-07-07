#!/usr/bin/env bash

scp *.py terryadmin@terry.vm.pozitron.com:/home/terryadmin/can/bamboo-timeoff-reminder/
scp config/config-prod.ini setup.sh requirements.txt terryadmin@terry.vm.pozitron.com:/home/terryadmin/can/
