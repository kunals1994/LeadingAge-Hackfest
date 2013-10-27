from operator import itemgetter, attrgetter
import datetime
import time
import urllib2
#from twilio.rest import TwilioRestClient

s = "http://svellore.com/HackFest2.php?fname_user=Damara&lname_user=Ross&phone_user=3122599744&fname_resp=Brett&lname_resp=Jeffery&phone_resp=+19177204135&alt_phone_resp=&email=aepofj%40ajeg.com&alt_email=&message=message+content&time=9%3A35&Language=English&Monday=on&Tuesday=on&Wednesday=on&Sunday=on"
s1 = s.split("?")[1]
#print(s1)
s2 = s1.split("&")
#print(s2)
#print(s2[0])
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
DAYSON = ["Monday=on", "Tuesday=on", "Wednesday=on", "Thursday=on", "Friday=on", "Saturday=on","Sunday=on"]

class queuedMessage():
    def __init__(self, message, day): 
        self.day = int(day)
        self.hour = int(message.time[0])
        self.minute = int(message.time[1])
        self.message = message.content
        self.client = message.client
        self.time = (self.day, self.hour, self.minute)
        self.flag = 0 # success/fail code?

class messageQueue():
    def __init__(self):
        self.queue = []

    def enqueue(self, message):
        self.queue.append(message)
        messageQueue.sortQueue()

    def sortQueue(self):
        self.queue.sort(key=lambda x: x.time)
        print(self.queue)

    def __getitem__(self, i):
        return self.queue[i]

    def removeFirst(self):
        print("Removed item 0")
        self.queue = self.queue[1:]
        
        
clientList = []
messageQueue = messageQueue()

def parser(L):
    #Passed a split list containing only the variables
    #client_name = L[0].split("=")[1]
    clientFirstName = getVariable(L[0])
    clientGivenName = getVariable(L[1])
    clientNumber = getVariable(L[2])
    clientList.append(Client(clientFirstName,
                             clientGivenName,
                             "+1"+clientNumber))
    index = 3
    while index < len(L)-1:
        if L[index].startswith("fname_resp"):
            clientList[-1].responders.append(Responder(getVariable(L[index]),
                                                       getVariable(L[index + 1]),
                                                       getVariable(L[index + 2]),
                                                       getVariable(L[index + 3]),
                                                       getVariable(L[index + 4]),
                                                       getVariable(L[index + 5]),
                                                       clientList[-1]))
            
            
            index += 6
            
        if L[index].startswith("message"):
            clientList[-1].messages.append(Message(getVariable(L[index]),
                                                   getVariable(L[index + 1]),
                                                   getVariable(L[index + 2]),
                                                   clientList[-1]))
            index += 3

            
            while (L[index] in DAYSON) and (index < len(L) - 1):
                clientList[-1].messages[-1].repeats.append(dayToNum(L[index]))
                index += 1

            
            
                                                                   

        #print(L[index])
    clientList[-1].messages[-1].repeats.append(dayToNum(L[-1]))
    tempList = []
    for i in clientList[-1].messages[-1].repeats:
        if i not in tempList:
            tempList.append(i)
    clientList[-1].messages[-1].repeats = []
    for i in tempList:
        clientList[-1].messages[-1].repeats.append(i)

    for r in clientList[-1].messages[-1].repeats:
            print(r, clientList[-1].messages[-1].time)
            messageQueue.enqueue(queuedMessage(clientList[-1].messages[-1], r))

def dayToNum(s):
    return (DAYSON.index(s))

        

class Client():
    def __init__(self,
                 firstName,
                 givenName,
                 number):
        self.firstName = firstName
        self.givenName = givenName
        self.number = number
        self.responders = []
        self.messages = []

class Responder():
    def __init__(self,
                 firstName,
                 givenName,
                 number,
                 altNumber,
                 email,
                 altEmail,
                 client):
        self.firstName = firstName
        self.givenName = givenName
        self.number = number
        self.altNumber = altNumber
        self.email = email.replace("%40", "@")
        self.altEmail = altEmail.replace("%40", "@")
        self.client = client

class Message():
    def __init__(self,
                 messageContent,
                 time,
                 language,
                 client):
        self.content = messageContent.replace("+", " ")
        self.time = time.split("%3A")
        self.language = language
        self.repeats = []
        self.client = client
        me = self

        
    #add to message queue for every day it exists
#        for r in self.repeats:
#            print(r, me.messageContent)
#            messageQueue.enqueue(me, r)


               
                 

def getVariable(variableString):
    split = variableString.split("=")
    #print(split)
    return split[1]

def responderCount(L):
    num = 0
    for i in L:
        if i.startswith("fname_resp"):
            print(i)
            num += 1
    return num

def printAll():
    for i in clientList:
        print(i.firstName + " " + i.givenName + " - " + i.number)
        for r in i.responders:
            print(r.firstName + " " + r.givenName)
            print(r.number)
            print(r.email)
        for m in i.messages:
            print(m.content)
            print(m.time[0] + ":" + m.time[1] + " " + m.language)
            for t in m.repeats:
                print DAYS[t] + " ",
        print(" ")
            

parser(s2)
for i in clientList:
    print(i.firstName)
responderCount(s2)
infinite = 0
printAll()
#t=(6,8,12)
#messageQueue[0].time = t


def compareTime(timeTuple):
    now=time.localtime()
    #print(timeTuple[0], now[-3])
    if timeTuple[0] != now[-3]:
#        print("No!")
        return False
    if timeTuple[1] != now[3]:
        return False
    if timeTuple[2] != now[4]:
        return False
    return True

def checkReady():
    if compareTime(messageQueue[0].time):
        print("Ready to go!")
        return True
    return False

def call(number, message, lang, flag):
    #number = ""
    #message = ""
    #lang = ""
    if(flag==0):
        flag="0"
    else:
        flag = "1"
    message = message.replace (" ", "%20")
    msg= "http://neon-carrot.appspot.com/call?msg="+message+"&num="+number+"&lang="+lang
    print(msg)
    resp = urllib2.urlopen("http://neon-carrot.appspot.com/call?msg="+message+"&num="+number+"&lang="+lang+"&flag="+flag, timeout=60).read()
    print(resp)
    if(resp == "success"):
        return True
    elif(resp == "fail"):
        return False
    #return boolean

def callStatus(stuff):
    #return true if succeeded

    #return false if failed
    pass

def respond(client, num):
    
    resp = client.responders[num]
    msg = "Hello, " + resp.firstName + ". " + client.firstName +" " + client.givenName + " did not answer their phone.   This is an automated message from Alice with Staying at Home with a Safety Net.  You are listed as  the first contact number on their no response list.  They would appreciate it if you checked in on them.  Thank you." 
    #call first in list
    print(msg)
    boo = (call(resp.number, msg, "en-US", 1))
    print(boo)
    return boo
    

def checkIn():
    i = 0
    clientMessage = messageQueue[0]
    client = messageQueue[0].client
    resp = call(client.number, clientMessage.message, 'en-US', 0)
    print(resp)
    if resp:
        messageQueue.removeFirst()
    else:
        while i < len(client.responders):
           if respond(client, i):
               i = 100
               messageQueue.removeFirst()
           else:
               respond(client, i)
               i += 1
    #call client number

    #if succeed, pop Queue[0]
    #messageQueue.removeFirst();

    #if fail, call response [0]

        #if succeed, pop Queue[0]

        #if fail, call response [n+1]

        #if no answers, pop Queue[0]
t = (6, 10, 45)
messageQueue[0].time = t
def hdd():
    while (infinite == 0):
        if checkReady():
            checkIn()



hdd()
    
