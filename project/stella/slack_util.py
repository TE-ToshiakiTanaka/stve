import os
import sys

from stve.log import Log
from stve.exception import *

from slacker import Slacker

L = Log("Slack.Library.STVE")

class Slack(object):
    def __init__(self, token):
        try:
            self.slack = Slacker(token)
        except Exception as e:
            L.warning(str(e))
            raise SlackError("%s is not exists." % token)

    def message(self, message, channels):
        try:
            result = self.slack.chat.post_message(
                channels,
                message,
                as_user=True)
            if result.successful:
                return result.body
            else:
                L.warning("Slack Error : %s" % result.error)
                raise SlackError(result.error)
        except Exception as e:
            L.warning(str(e))
            raise SlackError("%s is not exists." % channels)


    def upload(self, filepath, channels,
               content=None,
               filetype=None,
               filename=None,
               title=None,
               initial_comment=None):
        try:
            result = self.slack.files.upload(
                filepath,
                content=content,
                filetype=filetype,
                filename=filename,
                title=title,
                initial_comment=initial_comment,
                channels=channels)
            if result.successful:
                return result.body
            else:
                L.warning("Slack Error : %s" % result.error)
                raise SlackError(result.error)
        except Exception as e:
            L.warning(str(e))
            raise SlackError("%s is not exists." % channels)

    def list(self, channels):
        try:
            result = self.slack.files.list()
            for r in result:
                L.info(r)
        except Exception as e:
            L.warning(str(e))
            raise SlackError("%s is not exists." % channels)

if __name__ == "__main__":
    #sl.message("Test", ["kancolle2"])
    sl.list("kancolle")
