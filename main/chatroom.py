'''
Created on Apr 8, 2017

@author: arno
'''
        
class Room:
    def __init__(self, currentUser):
        self.participants = {}
        self.participants['currentUser.name']=