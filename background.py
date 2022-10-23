from colorama import Fore, init, Back
from datetime import datetime
from threading import Thread
import hashlib
import random
import socket


def decyprion(arg):
    word = arg.split(": ")[-1]
    print("the hash :",arg)
    key = "ddcf"
    alphabet = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]

    binary_list = []
    print("\nbinary alphabet list :")
    for i in alphabet:
        h = '\n'.join(format(ord(x), 'b') for x in i)
        print(h)
        binary_list.append(h)

    count = 0
    max_length = 55
    hash_latter = []
    hash_colection = []
    for i in word:
        hash_latter.append(i)
        if count == max_length :
            x = ''.join(hash_latter)
            hash_colection.append(x)
            hash_latter = []
            max_length+=56
        count +=1
    print("\n56 latter = hash :",hash_colection)

    world = []
    for test in hash_colection:
        #print(test)
        for i in binary_list:
            g = hashlib.sha224(f"{i}".encode('utf-8')).hexdigest()
            #print("eyshakat ta era")
            #print(g == test)
            if g == test:
                index = binary_list.index(i)
                #print ("winer winer chiken dinar")
                print ("\n\nthe hash is :"+ g + " Binary is :"+str(binary_list[index])+" Latter :"+ alphabet[index])
                world.append(alphabet[index])
                #print(len(g))
    result = ''.join(world)
    print ("\ncipher : ",result)


    word_index = []
    key_index = []

    for i in result:
        if i.isalpha():
            word_index.append(alphabet.index(i))
    for i in key:
        if i.isalpha():
            key_index.append(alphabet.index(i))

    #print ("word_index : ",word_index)
    #print ("key_index : ",key_index)

    reverse_key = 0
    deter_key = (key_index[0]*key_index[3]) - (key_index[1]*key_index[2])
    #print(deter_key)
    for rev in range(0,deter_key):
        check = (deter_key * rev)/26
        mod = (check - int(check)) * 26
        if round(mod) == 1 :
            reverse_key = rev 
    #print (reverse_key)

    adj_key = [key_index[3]*reverse_key,((key_index[1]*-1)+26)*reverse_key,((key_index[2]*-1)+26)*reverse_key,key_index[0]*reverse_key]
    #print(adj_key)

    full_key = []
    for mod in adj_key:
        if mod >26 :
            num = mod/26
            mod = (num - int(num))*26
        full_key.append(round(mod))
    #print("reverse_key(full) :",full_key)

    partetion_of_wordIndex = [] # we must split the entier word to the 2 alphabet per list or per part
    def two(paramet):
        x = 0
        y = 2
        index_length = len(paramet)
        if index_length % 2 == 0 :   # if this stattment be ture then taht men it is even else it is be odd
            z = index_length/2
            for part in range(0,int(z)):                               #chonyate lekdanaka
                partetion_of_wordIndex.append(paramet[x:y])         #[------>]    [ bo xwarawa]
                encodeing(full_key, partetion_of_wordIndex[part])  #[ 2   3 ]    [ 4 ]
                x += 2                                              #[ 55 24 ]    [ 5 ]
                y += 2                                              # wata [2*4 + 3*5]
            #print("word_index_two :",partetion_of_wordIndex)        # wata [55*4 + 24*5]
        else :
            print("you need extra latter")

    altire_word = []
    def encodeing(list1,list2):
        keyword = list1
        latter = list2
        w = list1[0] * list2[0]
        g = list1[1] * list2[1]
        if (w+g)>26:
            new_latter = (w+g)/26
        else:
            new_latter = (w+g)
        first = round((new_latter - int(new_latter)) *26) 
        hg = list1[2] * list2[0]
        hj = list1[3] * list2[1]
        if (hg+hj)>26:
            new_latter2 = (hg+hj)/26
        else:
            new_latter2 = (hg+hj)
        secound = round((new_latter2 - int(new_latter2)) *26)
        #print(first)
        #print(alphabet[first])
        altire_word.append(alphabet[first])
        altire_word.append(alphabet[secound])
        #print(secound)
        #print(alphabet[secound])

    two(word_index)
    #print("\n")
    #print("the plain text : " , end="") 
    res = ''.join(altire_word)
    #print("\nres :"+ res +"\n")
    #print("[+]Note: sometime we have an extra (a) in the end!")
    return (arg.split(": ")[0]+ " :" + res)
    

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
SERVER_HOST = "127.0.0.3"
SERVER_PORT = 5002 # server's port
separator_token = "<SEP>" # we will use this to separate the client name & message

# initialize TCP socket
s = socket.socket()
print(f"[*] Connecting to {SERVER_HOST}:{SERVER_PORT}...")
# connect to the server
s.connect((SERVER_HOST, SERVER_PORT))
print("[+] Connected.")
# prompt the client for a name
name = "display"

def listen_for_messages():
    while True:
        message = s.recv(1024).decode()
        #print(message)
        message = decyprion(message)
        print("\n" + message)

# make a thread that listens for messages to this client & print them
t = Thread(target=listen_for_messages)
# make the thread daemon so it ends whenever the main thread ends
t.daemon = True
# start the thread
t.start()

while True:
    # input message we want to send to the server
    to_send =  input(colors[-3])
    # a way to exit the program
    if to_send.lower() == 'q':
        break
    # add the datetime, name & the color of the sender
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
    to_send = f"{client_color}[{date_now}] {name}{separator_token}{to_send}{Fore.RESET}"
    # finally, send the message
    s.send(to_send.encode())

# close the socket
s.close()