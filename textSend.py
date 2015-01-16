#!/usr/bin/python
print "Content-type: text/html"
print
print "<html><head>"
print "</head><body>"
import datetime  # for getting date

from utils import numMessages, subMessage

import smtplib  # for sending email
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

# for connecting to mysql
import mysql.connector
cnx = mysql.connector.connect(user='<your db user>',
                              database='<your db name>')
cursor = cnx.cursor()

# Logging in to server
server.login("email_address@email.com", "password")

# Taking input
import cgi
form = cgi.FieldStorage()

# If user only inputs name
if "message" not in form:
    print "<center>"
    print "<p>You need to write a message</p>"
    print "<form method='POST' action='/cgi-bin/textSend.py'>"
    print "<body style='background-color:00FFFF;'>"
    print "<textarea name='message' rows='6' cols='50' "\
          "placeholder='Enter your message here..'></textarea>"
    print "<p></p>"
    print "<input type='text' name ='name' placeholder='Name'><br>"
    print "<input type='submit' value='Send' />"
    numMessages()
    print "<p><a href='/cgi-bin/mainPage.py'>Home Page</a></p>"
    print "<center>"
    print "</form>"

# if user only inputs message
elif "name" not in form:
    message = form["message"].value  # keeps the message in the text box
    print "<center>"
    print "<p>You need to input your name</p>"
    print "<form method='POST' action='/cgi-bin/textSend.py'>"
    print "<body style='background-color:00FFFF;'>"
    print "<textarea name='message' rows='6' cols='50'>%s</textarea> " \
           % (message)
    print "<p></p>"
    print "<input type='text' name ='name' placeholder='Name'><br>"
    print "<input type='submit' value='Send' />"
    numMessages()
    print "<p><a href='/cgi-bin/mainPage.py'>Home Page</a></p>"
    print "<center>"
    print "</form>"

# If user provides input for all fields
else:
    print "<body style='background-color:00FFFF;'>"
    print "<center>"
    message = form["message"].value
    name = form["name"].value

    # Send the email
    try:
        cursor.execute("SELECT Number,Provider FROM numbers")
        rows = cursor.fetchall()
        for row in rows:
            if (row[1] == "ATT"):
                domain = "text.att.net"
            elif (row[1] == "Verizon"):
                domain = "vtext.com"
            elif (row[1] == "T-Mobile"):
                domain = "tmomail.net"
            elif (row[1] == "Sprint"):
                domain = "messaging.sprintpcs.com"
            msg = "\n%s\n-%s" % (message, name)
            # sends message based on provider
            server.sendmail("depsitext@gmail.com", [row[0] + "@" + domain],
                            msg)
    except:
        print "<p>Message failed to send</p>"
        print "<a href='/cgi-bin/mainPage.py'>Click</a> "\
              " to Try and Send Another Message"
    else:
        newNum = subMessage()
        # Outputs the message, name, and the number of messages left to send
        print "<h1>Message Sent</h1>"
        print "<p>Message: %s</p>" % (message)
        print "<p>Name: %s</p>" % (name)
        print "Number of messages left to send for the day: %s" % (newNum)
        print "<p></p>"
        print "<a href='/cgi-bin/mainPage.py'>Click</a> "\
              "to Send Another Message"
        print "<p></p>"
        print "<a href='http://www.depsifounding.org/site/'>Click</a> "\
              " to Return to the Depsi Home Page"
        print "<center>"

print "</body></html>"
