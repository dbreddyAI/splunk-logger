# splunk-logger
** Custom logger for Splunk Modular Inputs **

Use the follofing to use this logger:
``` python 
log = mylogger.Logger(level='INFO')
# If you'd like to set/change Splunk Modular Input in log message:
log.source = splunk_input_name
# If you'd like to dynamically change logging level:
log.setLevel(input_item['log_level'])
```
