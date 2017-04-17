#!/usr/local/bin/python2.7

# Replace the above string with your !/path/to/python
# Test environment is on OpenBSD using python 2.7

import socket
import re
import os
import sys
import sqlite3 as lite
from ConfigParser import SafeConfigParser

sock = socket.socket()

def srv_conn(server, port, nickname, password):
    # Main IRC connection / exception handling
    try:
        sock.connect((server, port))
        send("USER " + nickname + " USING CUSTOM BOT")
        send("NICK " + nickname)
        #send("NICKSERV IDENTIFY " + password)
        print "CONNECT " + server, port
        print "NICK " + nickname
        print "/MSG NICKSERV IDENTIFY " + password
    except socket.error, exc:
        print "Caught exception socket.error : %s" % exc

def send(msg):
    sock.send(msg + "\r\n")

# Find all PRIVMSG
def check():
    # Remove the colon character from the string.
    no_colon = data.strip(':')
    #print no_colon

    # Create an entry for the user by removing the first colon
    # and splitting at the first exclamation point.

    user_split = re.split('!', no_colon)
    discovery_user = user_split[0]
    if len(discovery_user) > 16:
        return
    #print "User is", discovery_user,"\n"

    # Split with spaces into a list.

    data_list = re.split(' ', no_colon)
    #print data_list

    # Remove the long user location string.

    data_list.pop(0)
    #print data_list

    # Remove garbage items less than 2 characters
    for check in data_list:
        if len(check) < 2:
            data_list.remove(check)

    # Find a list of the current channels in the data stream

    chan_check = []
    for check in data_list:
        for channel in channels:
            chan_check.append(re.findall(channel, check))
    chan_check = filter(None, chan_check)  
    #print chan_check

    # Insert the user string into the data_list.
    data_list.insert(0,discovery_user)
    #print data_list

    discovery_channel = chan_check[0]
    #print discovery_channel

    links = []
    for link in data_list:
        links.append(re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', link))
    links = filter(None, links)

    #print links
    counter = 0
    for link in links:
        query_ready = discovery_user, discovery_channel[0], link[counter]
        counter + 1
        cur.execute('SELECT * FROM linknlog WHERE URL=?;', link)
        dupecheck = cur.fetchone()

        # Check for duplicate links:
        if dupecheck is None: 
            cur.execute('INSERT INTO linknlog VALUES(NULL,?,?,?);', query_ready)
            con.commit()
            print "STATUS: Committed Link:", str(query_ready)
        else:
            print "STATUS: Duplicate Link."
            return

def main():
    global data

    # Parse configuration file

    parser = SafeConfigParser()
    parser.read('config/config.txt')

    bot_owner = parser.get('Bot_config','bot_owner')
    nickname = parser.get('Bot_config','nickname')
    sections = []
    for section_name in parser.sections():
        sections.append(section_name)
        #print sections
        #print '  Options:', parser.options(section_name)
        if section_name != "Bot_config":
            var = []
            for name, value in parser.items(section_name):
            #print '  %s = %s' % (name, value)
                c = 0
                var.append(value)
                c + 1
            #print var
            server = var[0]
            port = int(var[1])
            nickname = var[2]
            password = var[3]
            clean = var[4].replace(' ','')
            channels = clean.split(",")
            print server, port, nickname, password, channels
            srv_conn(server, port, nickname, password)

    # Sqlite3 Database creation/connection

    global con
    con = lite.connect('linknlog.db')
    with con:
        global cur
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS linknlog(Id INTEGER PRIMARY KEY, USER, CHANNEL, URL TEXT)")

    while 1:
        data = sock.recv(1024)
        print data
        # Keepalive connection
        if data[0:4] == "PING":
            send(data.replace("PING", "PONG"))
            #send("MODE " + nickname + "+B")
            for channel in channels:
                send("JOIN " + channel)

        if data.find("PRIVMSG") > 0:
            #print(data.find("PRIVMSG"))
            for channel in channels:
                if data.find(channel) > 0:
                    check()

main()
