#!/usr/bin/python
print "Content-type: text/html"
print
print "<html><head>"
print "</head><body>"

#import module for getting day
import datetime

#import module for connecting to mysql
import mysql.connector
cnx = mysql.connector.connect(user='root', database='delta')
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

#Html part, which prints blue screen with textbox and text space with a send button
print "<center>"
print "<form method='POST' action='/cgi-bin/emailing.py'>"
print "<body style='background-color:00FFFF;'>"
print "<h1>Delta Text</h1>"
print "<p></p>"
print "<textarea name='message' rows='6' cols='50' placeholder='Enter your message here..'></textarea>"
print "<p></p>"
print "<input type='text' name ='name' placeholder='Name'><br>"
print "<input type='submit' value='Send' />"
numMessages()
print "<p></p>"
print "<a href='/secretary.html'>Click</a> if you are the secretary"
print "<p></p>"
print "<a href='http://www.depsifounding.org/site/'>Click</a> to Return to the Depsi Home Page"
print "<center>"
print "</form>"

print "</body></html>"
