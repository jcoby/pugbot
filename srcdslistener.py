#!/usr/bin/python

import config
import psycopg2
import socket
import time

database = psycopg2.connect('dbname=tf2ib host=localhost user=tf2ib password=jw8s0F4')
cursor = database.cursor()

listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listener.bind(('108.171.185.124', 27069))
listener.listen(1)
servers = ["74.91.114.227", "216.52.148.224"]
while 1:
    try:
        connection, address = listener.accept()
    except:
        listener.listen(1)
        continue
    try:
        data = connection.recv(4096)
    except:
        continue
    print data
    print address[0] 
    if data:
        print 'authorized'
        cursor.execute('INSERT INTO srcds VALUES (%s, %s)', (data, int(time.time())))
        database.commit()
        connection.close()
