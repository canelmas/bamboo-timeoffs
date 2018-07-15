## What?

Getting notified about time offs of a custom employee groups (project teams), consisted of people from different organizational departments.

## Why?

A project team is usually consisted of employees from different departments. We need a way to inform project teams and/or 
project managers about team's incoming time offs.
  
## How?

A cron job fetches time offs of each employee listed in a team file and sends emails to people specified.  

#### Team File Structure
```
# sample  team file
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

