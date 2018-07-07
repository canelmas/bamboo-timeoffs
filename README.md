* Get list of employees
* Read list of employee emails from each different project team files listed in ```team``` section
* For each employee in the project team fetch time offs
* Format time offs
* Email time off reminder to each employee listed in ```report``` section

#### Team File
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

