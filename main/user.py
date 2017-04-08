
'''
Created on Mar 27, 2017

@author: arno
'''

class User:

    def __init__(self, name):
        self.name = name
        return

    def buildMessage(self, command, message):
        return ''.join(['user:', self.name,
                         '\ncommand:', command, '\nmessage:',message, '\n\n' ])


# end User class

