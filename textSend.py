#!/usr/bin/python
print "Content-type: text/html"
print
print "<html><head>"
print "</head><body>"
import datetime #for getting date

import smtplib #for sending email
server = smtplib.SMTP("smtp.gmail.com", 587)
server.starttls()

#for connecting to mysql
import mysql.connector
cnx = mysql.connector.connect(user = 'root', database = 'delta')
cursor = cnx.cursor()

#Gives the number of messages able to send for the day
def numMessages():
    cursor.execute("SELECT id FROM numbers")
    rows = cursor.fetchall();
    count = 0 #Variable to count how many numbers there are in database
    for row in rows:
        count += 1
    print "<p>Number of messages left to send for the day:"
    day = int(datetime.date.today().strftime("%j")) #Gets the day of the year

    #Gets the most recent day of the year used (stored in table)
    cursor.execute("SELECT current FROM day WHERE ID = 1") 
    day2 = cursor.fetchone()
    day2 = day2[0]
    day2 = int(day2)

    #Checks that it has been more than a day
    if ((day - day2) >= 1):
        messages = 500 / count #Gmail can send a max of 500 emails per day
        cursor.execute("UPDATE day SET messages=%s  WHERE ID=%s", (messages, 1))
        cnx.commit()
        cursor.execute("UPDATE day SET current=%s WHERE ID=%s", (day, 1))
        cnx.commit()
        print messages 
    #If it has been less than a day just get number of messages able to send from database
    else:
        cursor.execute("SELECT messages FROM day")
        messages = cursor.fetchone()
        messages = messages[0]
        print messages

#Logging in to server
server.login("email_address@email.com" , "password")

#Taking input from html
import cgi
form = cgi.FieldStorage()

#If user only inputs name
if "message" not in form:
    print "<center>"
    print "<p>You need to write a message</p>"
    print "<form method='POST' action='/cgi-bin/emailing.py'>"
    print "<body style='background-color:00FFFF;'>"
    print "<textarea name='message' rows='6' cols='50' placeholder='Enter your message here..'></textarea>"
    print "<p></p>"
    print "<input type='text' name ='name' placeholder='Name'><br>"
    print "<input type='submit' value='Send' />"
    numMessages()
    print "<p><a href='/cgi-bin/mainPage.py'>Home Page</a></p>"
    print "<center>"
    print "</form>"

#if user only inputs message
elif "name" not in form:
    message = form["message"].value #keeps the message in the text box
    print "<center>"
    print "<p>You need to input your name</p>"
    print "<form method='POST' action='/cgi-bin/emailing.py'>"
    print "<body style='background-color:00FFFF;'>"
    print "<textarea name='message' rows='6' cols='50'>%s</textarea>" %(message)
    print "<p></p>"
    print "<input type='text' name ='name' placeholder='Name'><br>"
    print "<input type='submit' value='Send' />"
    numMessages()
    print "<p><a href='/cgi-bin/mainPage.py'>Home Page</a></p>"
    print "<center>"
    print "</form>"      

#If user inputs all
else:
    print "<body style='background-color:00FFFF;'>"
    print "<center>"
    message = form["message"].value
    name = form["name"].value

    #Send the email
    cursor.execute("SELECT Number,Provider FROM numbers")
    rows = cursor.fetchall()
    for row in rows:
        if (row[1] == "ATT"):
            msg = "\n%s\n-%s" %(message, name) #The \n seprates the message from the headers
            
            #sends message based on provider
            server.sendmail("depsitext@gmail.com", [row[0] + "@txt.att.net"], msg)
        elif (row[1] == "Verizon"):
            msg = "\n%s\n-%s" %(message, name) 
            server.sendmail("depsitext@gmail.com", [row[0] + "@vtext.com"], msg)
        elif (row[1] == "T-Mobile"):
            msg = "\n%s\n-%s" %(message, name)
            server.sendmail("depsitext@gmail.com", [row[0] + "@tmomail.net"], msg)
        elif (row[1] == "Sprint"):
            msg = "\n%s\n-%s" %(message, name) 
            server.sendmail("depsitext@gmail.com", [row[0] + "@messaging.sprintpcs.com"], msg)

    #Subtracts one from number of messages able to send
    cursor = cnx.cursor()
    cursor.execute("SELECT messages FROM day WHERE ID=1")
    messageNum = cursor.fetchone()
    messageNum = messageNum[0]        
    newNum = messageNum - 1
    cursor.execute("UPDATE day SET messages = %s WHERE ID = %s ", (newNum, 1))
    cnx.commit()
            
    #Outputs the message and name to the user and the number of messages left to send        
    print "<h1>Message Sent</h1>"
    print "<p>Message: %s</p>" % (message)
    print "<p>Name: %s</p>" % (name)
    print "Number of messages left to send for the day: %s" % (newNum) 
    print "<p></p>"
    print "<a href='/cgi-bin/mainPage.py'>Click</a> to Send Another Message"
    print "<p></p>"
    print "<a href='http://www.depsifounding.org/site/'>Click</a> to Return to the Depsi Home Page"
    print "<center>"

print "</body></html>"
