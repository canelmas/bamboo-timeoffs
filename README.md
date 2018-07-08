BambooHR is limited with a notification system based only with the organizational structure that you provide at the very beginning, while
setting up your instance i.e. you only get notified about your direct team's approaching time offs, requests, approvals etc. 

If getting notified about time offs of a custom employee groups (project teams), consisted of people from different organizational departments 
is a requirement, this repo may deliver that basically, with a cron job fetching data from bambooHR api and sending emails for each manually created 
project team.    

#### Team File Structure
```
# Sample
team=<comma separated employee emails for whom time offs will be fetched>  
report=<comma separated employee emails to whom reminder email will be sent to>
```

#### Config.ini
```
[bamboo]
sub_domain =xyz
api_key=bamboo_hr_api_key

[smtp]
host=smtp_host
port=smtp_port
from=from_mail_address
```

