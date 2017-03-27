from user import User
import socket
import re
import datetime as dt
'''
Created on Mar 27, 2017

@author: arno
'''

PORT = 1025
DEST_IP = "127.0.0.1"



def udpSocket():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return s

def sender():
    user = User(raw_input("Enter your name: "))
    s = udpSocket()
    
    while True:
        message = user.buildMessage(raw_input())
        print(message)
        s.sendto(message, (DEST_IP, PORT))
        
def receiver():
    s = udpSocket()
    s.bind((DEST_IP, PORT))
    
    while True:
        message = s.recvfrom(2048)
        
def displayMessage(userName, message):
    curDate = dt.datetime.now()
    print(''.join([re.sub('T', ' ', curDate.isoformat()), ' [', str(userName), ']: ', message]))
        
    
    
    
    
    
    