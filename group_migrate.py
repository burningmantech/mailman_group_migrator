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

from apiclient.errors import HttpError
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

    # Authenticate and construct service
    scope = ("https://www.googleapis.com/auth/apps.groups.migration")

    service, flags = sample_tools.init(
        argv, 'groupsmigration', 'v1', __doc__, __file__, parents=[argparser],
        scope=scope
        )

    mbox = mailbox.mbox(flags.mailbox, create=False)
    # create a new mbox with failed messages, to make reruns shorter
    if flags.failed:
        failbox = mailbox.mbox(flags.failed, create=True)
        failbox.lock()
    try:
        for message in mbox:
            # pprint.pprint(message)
            print message['message-id']
            print message['subject']
            media = MediaInMemoryUpload(str(message), mimetype='message/rfc822')
            request = service.archive().insert(groupId=flags.group,
                                               media_body=media)
            result = request.execute()
            print 'Response code was: %s' % result['responseCode']
            if flags.failed and result['responseCode'] != 'SUCCESS':
                failbox.add(message)
    except AccessTokenRefreshError:
        print ('The credentials have been revoked or expired, please re-run the '
               'application to re-authorize')
    if flags.failed:
        failbox.flush()
        failbox.unlock()



if __name__ == '__main__':
    main(sys.argv)
