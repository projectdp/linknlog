#!/usr/bin/python

import socket
import re
import os
import sys
import sqlite3 as lite

bot_owner = "projectdp"
nickname = "bot_name"
personNick = ""
channels = ["#freenode", "#party"]
sock = socket.socket()
server = "irc.freenode.net"
verified = [] 
port = 6667 

def send(msg):
    sock.send(msg + "\r\n")

sock.connect((server, port))
send("USER " + nickname + " USING CUSTOM BOT")
send("NICK " + nickname)

con = lite.connect('linknlog.db')
with con:        
    cur = con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS linknlog(Id INTEGER PRIMARY KEY, URL TEXT)")
while 1:
    data = sock.recv(512)
    print data
    if data[0:4] == "PING":
        send(data.replace("PING", "PONG"))
#        send("MODE " + nickname + "+B")
        for channel in channels:
            send("JOIN " + channel)
    links = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', data) 
    print links
    for link in links: 
        cur.execute('SELECT * FROM linknlog WHERE URL=?;', [link])
        dupecheck = cur.fetchone() 
        if dupecheck is None:  
            cur.execute('INSERT INTO linknlog VALUES(NULL,?);', [link])
            con.commit()
        else:
            print "Duplicate"
