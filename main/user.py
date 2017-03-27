import datetime as dt
import re

'''
Created on Mar 27, 2017

@author: arno
'''

class User:

    def __init__(self, name):
        self.name = name
        return

    def buildMessage(self, message):
        curDate = dt.datetime.now()

        return ''.join([re.sub('T', ' ', curDate.isoformat()), ' [', str(self.name), ']: ', message])




# end User class

