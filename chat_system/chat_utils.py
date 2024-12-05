import socket
import time
import json

# use local loop back address by default
CHAT_IP = ""
# CHAT_IP = socket.gethostbyname(socket.gethostname())
# CHAT_IP = socket.gethostbyname(socket.gethostname())
import os
CHAT_PORT = 1112
SERVER = (CHAT_IP, CHAT_PORT)

menu = "\n++++ Choose one of the following commands\n \
        time: calendar time in the system\n \
        who: to find out who else are there\n \
        k _key_: to use the key encode the chat messages\n  \
        c _peer_: to connect to the _peer_ and chat\n \
        ? _term_: to search your chat logs where _term_ appears\n \
        p _#_: to get number <#> sonnet\n \
        q: to leave the chat system\n\n"

S_OFFLINE   = 0
S_CONNECTED = 1
S_LOGGEDIN  = 2
S_CHATTING  = 3

SIZE_SPEC = 5

CHAT_WAIT = 0.2
def encrypt_message(key, plaintext):
    encrypted_list = []
    key_list = [ord(char) for char in key]
    for i in range(len(plaintext)):
        seq = i % len(key_list)
        encrypted_list.append(ord(plaintext[i]) * int(key_list[seq]))
    ciphertext = json.dumps(encrypted_list)
    return ciphertext

def decrypt_message(key, ciphertext):
    encrypted_list = json.loads(ciphertext)
    key_list = [ord(char) for char in key]
    plaintext = ''
    for i in range(len(encrypted_list)):
        seq = i % len(key_list)
        plaintext += chr(int(encrypted_list[i]) // int(key_list[seq]))
    return plaintext

def print_state(state):
    print('**** State *****::::: ')
    if state == S_OFFLINE:
        print('Offline')
    elif state == S_CONNECTED:
        print('Connected')
    elif state == S_LOGGEDIN:
        print('Logged in')
    elif state == S_CHATTING:
        print('Chatting')
    else:
        print('Error: wrong state')

def mysend(s, msg,key=None):
    #append size to message and send it
    #print('key',key)
    #if key:
    #    msg = encrypt_message( key,msg)
    #    print('sending '+msg)
    msg = ('0' * SIZE_SPEC + str(len(msg)))[-SIZE_SPEC:] + str(msg)
    msg = msg.encode()
    
    total_sent = 0
    while total_sent < len(msg) :
        sent = s.send(msg[total_sent:])
        if sent==0:
            print('server disconnected')
            break
        total_sent += sent

def myrecv(s,key=None):
    #receive size first
    size = ''
    while len(size) < SIZE_SPEC:
        text = s.recv(SIZE_SPEC - len(size)).decode()
    #    print('receivedtext '+text)
        if not text:
            print('disconnected')
            return('')
        size += text
    size = int(size)
    #now receive message
    msg = ''
    while len(msg) < size:
        
        text = s.recv(size-len(msg)).decode()
        if text == b'':
            print('disconnected')
            break
        msg += text
    #    print('receivedmsg '+msg)
    #if key:
    #    print('key',key)
    #    msg = decrypt_message(key,msg)
    #    print('receivedmsg2 '+msg)
    #print ('received '+message)
    return (msg)

def text_proc(text, user):
    ctime = time.strftime('%d.%m.%y,%H:%M', time.localtime())
    return('(' + ctime + ') ' + user + ' : ' + text) # message goes directly to screen
