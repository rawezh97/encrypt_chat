from colorama import Fore, init, Back
from datetime import datetime
from threading import Thread
import hashjsonlib
import random
import socket
import json

def reliable_send(data):
    json_data = json.dumps(data)
    json_encode = json_data.encode()
    target.send(json_encode)

def reliable_recv():
    json_data = b""
    while True:
        try:
            json_data = json_data + target.recv(1024)
            return json.loads(json_data.decode())
        except Exception as e:
            continue

def encryption(arg,key):
    word = arg
    key = key
    #print ("the key :",key)

    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","#"]

    word_index = []
    key_index = []

    for i in word :
        if i.isalpha():
            word_index.append(alphabet.index(i))
    for k in key:
        if k.isalpha():
            key_index.append(alphabet.index(k))

    #print("word_index :" ,word_index)
    #print("key index :"+ str(key_index))

    partetion_of_wordIndex = [] # we must split the entier word to the 2 alphabet per list or per part
    def two(paramet):
        x = 0
        y = 2                                   #variable = [[2,3],]
        index_length = len(paramet)
        if index_length % 2 == 0 :   # if this stattment be ture then taht men it is even else it is be odd
            z = index_length/2
            for part in range(0,int(z)):                               #chonyate lekdanaka
                partetion_of_wordIndex.append(paramet[x:y])         #[------>]    [ bo xwarawa]
                encodeing(key_index, partetion_of_wordIndex[part])  #[ 2   3 ]    [ 4 ]
                x += 2                                              #[ 55 24 ]    [ 5 ]
                y += 2                                              # wata [2*4 + 3*5]
            #print("word_index_two :",partetion_of_wordIndex)        # wata [55*4 + 24*5]
        else :
            paramet.append(0)
            index_length = len(paramet)
            z = index_length/2
            for part in range(0,int(z)):                               #chonyate lekdanaka
                partetion_of_wordIndex.append(paramet[x:y])         #[------>]    [ bo xwarawa]
                encodeing(key_index, partetion_of_wordIndex[part])  #[ 2   3 ]    [ 4 ]
                x += 2                                              #[ 55 24 ]    [ 5 ]
                y += 2                                              # wata [2*4 + 3*5]
            #print("word_index_two :",partetion_of_wordIndex)        # wata [55*4 + 24*5]

    altire_word = []
    def encodeing(list1,list2):
        keyword = list1
        latter = list2
        w = list1[0] * list2[0]
        g = list1[1] * list2[1]
        if (w+g)>26:
            new_latter = (w+g)/26
            new_latter = round((new_latter - int(new_latter)) *26) 
        else:
            new_latter = (w+g)

        hg = list1[2] * list2[0]
        hj = list1[3] * list2[1]
        if (hg+hj)>26:
            new_latter2 = (hg+hj)/26
            new_latter2 = round((new_latter2 - int(new_latter2)) *26)
        else:
            new_latter2 = (hg+hj)

        #print(first)
        #print(alphabet[first])
        altire_word.append(alphabet[new_latter])
        altire_word.append(alphabet[new_latter2])
        #print(secound)
        #print(alphabet[secound])


    two(word_index)
    #print(altire_word)
    cipher_word = []
    for i in altire_word:
        cipher_word.append(i)
    #print (cipher_word)
    #print("\nthe cipher text :",''.join(cipher_word))
    #print("\n")

    message = ''.join(cipher_word)
    h = '\n'.join(format(ord(x), 'b') for x in message)
    #print(h) # in here we split the binary to make it easy to use
    hh = h.split("\n")
    hash_col = []
    for i in hh:
        g = hashlib.sha224(f"{i}".encode('utf-8')).hexdigest()
        hash_col.append(g)
    result = ''.join(hash_col)
    #print(result)
    #print("secret message in here :\n"+result)
    return result

# init colors
init()

# set the available colors
colors = [ 
    Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, 
    Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, 
    Fore.LIGHTYELLOW_EX , Fore.LIGHTYELLOW_EX
]

# choose a random color for the client
client_color = random.choice(colors)

# server's IP address
# if the server is not on this machine, 
# put the private (network) IP address (e.g 192.168.1.2)
SERVER_HOST = "127.0.0.2"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
sock = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
sock.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
# prompt the client for a name
name = input(colors[2] + "Enter your username: ")

def listen_for_messages():
    while True:
        message = sock.recv(1024).decode()
        #print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send =  input(colors[-3])
    to_send = encryption(to_send, 'ddcf')
    # a way to exit the program
    if to_send.lower() == 'q':

        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    sock.send(to_send.encode())

# close the socket
sock.close()