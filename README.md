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


Usage: ``group_migrate.py [-h] -m MAILBOX -g GROUP [-f FAILED]``

Options:

* -m | --mailbox: The mailbox to take messages from
* -f | --failed: The mailbox to write failed messages to (Optional)
* -g | --group: The Google Group to write messages to

## Notes

It appears that Google will not permit duplicate messages, so this can be rerun safely.
