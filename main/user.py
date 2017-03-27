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
        return ''.join(['user:'], self.name, '\nmessage:',message, '\n\n' )


# end User class

