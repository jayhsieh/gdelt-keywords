# gdelt-keywords

Compilation for GDELT daily top 100 Keywords


## Set daily job on ubuntu16.04
1. Use `crontab -e` to add crontab job description below

```
# set shell script
SHELL=/bin/bash

# execute at 07:00 and 19:00 everyday
00 07,19 * * * sh /home/deploy/GDELT/gdelt-keywords/wrapper_for_crontab.sh
```

2. Use `sudo cat /var/log/syslog | grep --color 'CRON'` to show logs 
