## What?

Getting notified about time offs of a custom employee groups (project teams), consisted of people from different organizational departments.

## Why?

A project team is usually consisted of employees from different departments. We need a way to inform project teams and/or 
project managers about team's incoming time offs.
  
## How?

A cron job fetches time offs of each employee of each project team and sends emails to people specified.

You can either use static project team files or Tempo API.

### Team Files

Directory containing project team files can be specified with the command line parameter **--teams**.   

```
# team_xyz 
team=<comma separated employee emails for whom time offs will be fetched>  
report=<comma separated employee emails to whom reminder email will be sent to>
```

### Tempo API

By default Tempo API is used to fetch project teams, team members and project lead. 

### Configuration

```
[bamboo]
sub_domain =xyz
api_key=bamboo_hr_api_key

[tempo]
url = tempo_url
token = tempo_basic_auth_token

[smtp]
host=smtp_host
port=smtp_port
from=from_mail_address
```

