# MailMan to Google Group Migrator [![Code Climate](https://codeclimate.com/github/burningmantech/mailman_group_migrator/badges/gpa.svg)](https://codeclimate.com/github/burningmantech/mailman_group_migrator)

Command line tool to migrate Mailman mbox archives to Google Groups.

## Requirements
### Requires the google python API client
```
sudo pip install -U google-api-python-client
```

### Setup

The Google API libraries require some setup, per https://developers.google.com/api-client-library/python/start/get_started.

If the Domain Administrator has already setup the API, the ``client_secrets.json`` file is required.

## Usage

```
usage: group_migrate.py [-h] [--auth_host_name AUTH_HOST_NAME]
                        [--noauth_local_webserver]
                        [--auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]]
                        [--logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}]
                        -m MAILBOX -g GROUP [-f FAILED] [-v] [-a AFTER]
                        [-b BEFORE] [-n] [-r RESUME] [-l LABEL]

Utility to migrate an mbox mailbox (from mailman, ideally) to Google Groups

optional arguments:
  -h, --help            show this help message and exit
  --auth_host_name AUTH_HOST_NAME
                        Hostname when running a local web server.
  --noauth_local_webserver
                        Do not run a local web server.
  --auth_host_port [AUTH_HOST_PORT [AUTH_HOST_PORT ...]]
                        Port web server should listen on.
  --logging_level {DEBUG,INFO,WARNING,ERROR,CRITICAL}
                        Set the logging level of detail.
  -m MAILBOX, --mailbox MAILBOX
                        The mailbox file containing the messages to be
                        migrated.
  -g GROUP, --group GROUP
                        The email address of the group to receive the migrated
                        messages.
  -f FAILED, --failed FAILED
                        The mailbox file containing the messages that failed
                        to be migrated.
  -v, --verbose         Show progress
  -a AFTER, --after AFTER
                        Only import after date
  -b BEFORE, --before BEFORE
                        Only import before date
  -n, --dryrun          Dry-run
  -r RESUME, --resume RESUME
                        resume with message #
  -l LABEL, --label LABEL
                        import matching label (X-Gmail-Labels)

```


## Notes

It appears that Google will not permit duplicate messages, so this can be rerun safely.
