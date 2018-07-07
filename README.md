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
```python
[bamboo]
SUB_DOMAIN = xyz
API_KEY = bamboo_hr_api_key

[smtp]
HOST = smtp_host
PORT = smtp_port
```

