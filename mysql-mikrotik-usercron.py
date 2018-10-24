#!/usr/bin/python

import pymysql

import base64
import getpass
import os
import socket
import sys
import traceback
from paramiko.py3compat import input
from paramiko.ssh_exception import BadHostKeyException, AuthenticationException, SSHException

import paramiko

conn = pymysql.connect(
    db='db_name',
    user='username',
    passwd='password',
    host='mysql_host_address')
c = conn.cursor()
print("*** Connected to database...")

c.execute("SELECT adm_no.admission_id, student.fname FROM adm_no, student WHERE student.student_id = adm_no.student_id;")

print("*** starting ssh...")
client = paramiko.SSHClient()
print("*** 1 ssh client loaded...")
client.load_system_host_keys()
print("*** 2 loading system host keys...")
client.set_missing_host_key_policy(paramiko.WarningPolicy())
print("*** 3 loading missing host key policy (WarningPolicy)...")
client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
print("*** 3a loading missong host key policy (AutoAddPolicy)...")
client.load_system_host_keys()
client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
print("*** 3b Connecting to Mikrotik router...")
client.connect("host_address",port=22, username="username", password="password" )
print("*** 4 Connected and Writing...")

for row in c:
	print (row[0].lower())
	print (row[1].lower())
	client.exec_command('ip hotspot user add name='+row[0].lower()+' password='+row[1].lower()+' profile=student')

print("*** 5...")
print("*** All Good Donw!...")
