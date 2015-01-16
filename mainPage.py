#!/usr/bin/python
print "Content-type: text/html"
print
print "<html><head>"
print "</head><body>"

# import module for getting day
import datetime

from utils import numMessages

# import module for connecting to mysql
import mysql.connector
cnx = mysql.connector.connect(user='root', database='delta')
cursor = cnx.cursor()


# Html part
# prints blue screen with textbox and text space with a send button
print "<center>"
print "<form method='POST' action='/cgi-bin/textSend.py'>"
print "<body style='background-color:00FFFF;'>"
print "<h1>Delta Text</h1>"
print "<p></p>"
print "<textarea name='message' rows='6' cols='50' "\
      "placeholder='Enter your message here..'></textarea>"
print "<p></p>"
print "<input type='text' name ='name' placeholder='Name'><br>"
print "<input type='submit' value='Send' />"
numMessages()
print "<p></p>"
print "<a href='/secretary.html'>Click</a> if you are the secretary"
print "<p></p>"
print "<a href='http://www.depsifounding.org/site/'>Click</a> to Return to "\
      "the Depsi Home Page"
print "<center>"
print "</form>"

print "</body></html>"
