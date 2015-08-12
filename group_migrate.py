#! /usr/bin/python
"""
Utility to migrate an mbox mailbox (from mailman, ideally) to Google Groups
"""

import argparse
import pprint
import sys
import mailbox
import httplib2
import os
import logging
logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',level=logging.DEBUG)
import dateutil.parser
import pytz

from apiclient.errors import HttpError,MediaUploadSizeError
from apiclient.http import BatchHttpRequest
from apiclient.http import HttpMock
from apiclient.http import MediaInMemoryUpload
from apiclient import sample_tools
from oauth2client.client import AccessTokenRefreshError


def main(argv):
    # Declare command-line flags.
    # addHelp=False here because it's added downstream in the sample_init
    argparser = argparse.ArgumentParser(add_help=False)

    argparser.add_argument(
        '-m',
        '--mailbox',
        help='The mailbox file containing the messages to be migrated.',
        required=True)
    argparser.add_argument(
        '-g',
        '--group',
        help='The email address of the group to receive the migrated messages.',
        required=True)
    argparser.add_argument(
        '-f',
        '--failed',
        help='The mailbox file containing the messages that failed to be migrated.',
        required=False)
    argparser.add_argument(
        '-v',
        '--verbose',
        help='Show progress',
        action='store_true')
    argparser.add_argument(
        '-a',
        '--after',
        help='Only import after date',
        required=False)
    argparser.add_argument(
        '-b',
        '--before',
        help='Only import before date',
        required=False)
    argparser.add_argument(
        '-n',
        '--dryrun',
        help='Dry-run',
        action='store_true')

    # Authenticate and construct service
    scope = ("https://www.googleapis.com/auth/apps.groups.migration")

    service, flags = sample_tools.init(
        argv, 'groupsmigration', 'v1', __doc__, __file__, parents=[argparser],
        scope=scope
        )

    if (flags.after):
        flags.after = pytz.timezone('US/Pacific').localize(dateutil.parser.parse(flags.after))
        logging.info("only migrating messages after date: %s" % flags.after)
    if (flags.before):
        flags.before = pytz.timezone('US/Pacific').localize(dateutil.parser.parse(flags.before))
        logging.info("only migrating messages before date: %s" % flags.before)
    mbox = mailbox.mbox(flags.mailbox, create=False)
    i, mboxLen = 0, len(mbox)
    print "mailbox size: %d messages" % mboxLen
    # create a new mbox with failed messages, to make reruns shorter
    if flags.failed:
        failbox = mailbox.mbox(flags.failed, create=True)
        failbox.lock()
    try:
        for message in mbox:
            i += 1
            message.x_date =  dateutil.parser.parse(message.get('Date'))
            if(flags.after and ( message.x_date < flags.after)):
                logging.debug("skipping: date %s is before flags.after" % message.x_date)
                continue
            if(flags.before and ( message.x_date > flags.before)):
                logging.debug("skipping: date %s is after flags.before" % message.x_date)
                continue
            logging.debug("message-id: %s" % message['message-id'] )
            logging.debug("subject: %s" % message['subject'])
            logging.debug("date: %s" % message.x_date)
            print "processing message %s / %s" % (i,mboxLen)
            if(flags.dryrun):
                continue
            media = MediaInMemoryUpload(str(message), mimetype='message/rfc822')
            try:
                request = service.archive().insert(groupId=flags.group,
                                                   media_body=media)
                result = request.execute()
                logging.debug("response: %s" % result['responseCode'])
                if flags.failed and result['responseCode'] != 'SUCCESS':
                    failbox.add(message)
            except (MediaUploadSizeError,HttpError) as e:
                if flags.failed:
                    failbox.add(message)
                logging.error( "%s: %s" % (message['message-id'],str(e)) )
    except AccessTokenRefreshError:
        logging.error('The credentials have been revoked or expired, please re-run the '
               'application to re-authorize')

    if flags.failed:
        failbox.flush()
        failbox.unlock()

if __name__ == '__main__':
    main(sys.argv)
