#!/usr/bin/python
print "<html><head>"
print "</head><body>"

# import module for getting day
import datetime

# import module for connecting to mysql
import mysql.connector
cnx = mysql.connector.connect(user='root', database='delta')
cursor = cnx.cursor()

# Gives the number of messages able to send for the day
# Necessary because messages are sent using gmail
# has limit of 500 emails per day
def numMessages():
    cursor.execute("SELECT count(*) FROM numbers")
    rows = cursor.fetchall()
    count = (rows[0])[0]  # Variable to count how many numbers are in database
    day = int(datetime.date.today().strftime("%j"))  # Gets the day of the year

    # Gets the most recent day of the year used (stored in table)
    cursor.execute("SELECT current FROM day WHERE ID = 1")
    day2 = int(cursor.fetchone()[0])

    # Checks that it has been more than a day
    if ((day - day2) >= 1):
        messages = 500 / count  # Gmail can send a max of 500 emails per day
        cursor.execute("UPDATE day SET messages=%s  WHERE ID=1", (messages))
        cnx.commit()
        cursor.execute("UPDATE day SET current=%s WHERE ID=1", (day))
        cnx.commit()
        if (messages == 0):
            print "<p>You cannot send anymore messages today, "\
                  "try again tomorrow</p>"
        else:
            print "<p>Number of messages left to send for the day:"
            print messages
    # If it has been less than a day just get number of messages left to send
    #     from database
    else:
        cursor.execute("SELECT messages FROM day")
        messages = cursor.fetchone()
        messages = messages[0]
        if (messages == 0):
            print "<p>You cannot send anymore messages today, "\
                  "try again tomorrow</p>"
        else:
            print "<p>Number of messages left to send for the day:"
            print messages

# Subtracts one from number of messages able to send
def subMessage():
    cursor.execute("SELECT messages FROM day WHERE ID=1")
    messageNum = cursor.fetchone()
    messageNum = messageNum[0]
    newNum = messageNum - 1
    cursor.execute("UPDATE day SET messages=%s WHERE ID=%s ", (newNum, 1))
    cnx.commit()
    return newNum

def printPage(errorMes):
    print "<p><form method='POST' action='/cgi-bin/sec.py'>"
    print "<center>"
    print "<h2>%s</h2>" % (errorMes)
    print "<body style='background-color:00FFFF;'>"
    print "<input type='text' name='email' placeholder='Email'<br>"
    print "<input type='password' name ='pwd' placeholder='Password'><br>"
    print "<input type='submit' name='login' value='Login' />"
    print "<p></p>"
    print "<input type='submit' name='forgot' value='Forgot Password' />"
    print "</center></form>"

def changePass(message):
    print "<p><form method='POST' action='/cgi-bin/sec.py'>"
    print "<center>"
    print "<h1>Change Password</h1>"
    print "<p>%s</p>" % (message)
    print "<body style='background-color:00FFFF;'>"
    print "<p>Enter Current Password:<input type = 'text' name='oldpw' "\
          "placeholder='Enter Current Password'></p>"
    print "<p>Enter New Password:<input type = 'text' name='newpw' "\
          "placeholder='Enter New Password'></p>"
    print "<p>Re-enter New Password:<input type = 'text' name = 'newpw2' "\
          "placeholder='Re-enter New Password'></p>"
    print "<p><input type = 'submit' name='submitP' value='Submit'></p>"
    print "<p><input type = 'submit' name='back' value='Main Page'></p>"
    print "</center></form>"

def numbers(message):
    print "<form method ='POST' action='/cgi-bin/sec.py'>"
    print "<center>"
    print "<h1>%s<h1>" % (message)
    print "<input type='submit' name='changeP' value='Change Password'>"
    print "<input type='submit' name='changeE' value='Change Emails'>"
    print "<input type='submit' name='edit' value='Edit Numbers'>"
    print "<body style='background-color:00FFFF;'>"
    cursor = cnx.cursor()

    # Iterate through the rows of data in table 'numbers' and print them out
    cursor.execute("SELECT Name, Number, Provider FROM numbers")
    rows = cursor.fetchall()
    print "<table border='5' width=42% align='center'>"
    print "<tr>"
    print   "<th>Name</th>"
    print   "<th>Number</th>"
    print   "<th>Provider</th>"
    print "</tr>"
    for row in rows:
        print "<tr>"
        print   "<td>%s</td>" % (row[0])
        print   "<td>%s</td>" % (row[1])
        print   "<td>%s</td>" % (row[2])
        print "</tr>"
    print "</table>"
    print "<p><a href='/cgi-bin/mainPage.py'>Home Page</a></p>"
    print "</center></form>"

def editNums():
    # Table is printed with edit buttons
    print "<form method ='POST' action='/cgi-bin/sec.py'>"
    print "<center>"
    print "<body style='background-color:00FFFF;'>"

    # Iterate through the rows of data in table 'numbers' and print them out
    cursor.execute("SELECT Name, Number, Provider FROM numbers")
    rows = cursor.fetchall()
    print "<table border='5' width=42% align='center'>"
    print "<tr>"
    print   "<th>Name</th>"
    print   "<th>Number</th>"
    print   "<th>Provider</th>"
    print "</tr>"
    count = 1
    for row in rows:
        print "<tr>"
        print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                % (row[0], "editName" + str(count))
        print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                % (row[1], "editNum" + str(count))
        print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                % (row[2], "editPro" + str(count))
        print "</tr>"
        count += 1

# Prints buttons at bottom of page
def buttons():
    print "<p><input type='submit' name='addNumber' value='Add Number'>"
    print "<input type='submit' name='deleteNumber' value='Delete Number'></p>"
    print "<p><input type = 'submit' name='back' value='Main Page'></p>"
    print "<p><a href='/cgi-bin/mainPage.py'>Home Page</a></p>"

# Prints email editing page
def emails(message):
    cursor.execute("SELECT email_sec, email_pres, email_vp FROM secretary "
                   "WHERE ID = 1")
    emails = cursor.fetchall()
    print "<p><form method='POST' action='/cgi-bin/sec.py'>"
    print "<center>"
    print "<body style='background-color:00FFFF;'>"
    print"<h2>%s</h2>" % (message)
    for item in emails:
        email1 = item[0]
        email2 = item[1]
        email3 = item[2]
    print "<p>%s: <input type = 'text' name='email1' placeholder=%s></p>" \
          % (email1, email1)
    print "<p>%s: <input type = 'text' name='email2' placeholder=%s></p>" \
          % (email2, email2)
    print "<p>%s: <input type = 'text' name='email3' placeholder=%s></p>" \
          % (email3, email3)
    print "<p><input type = 'submit' name='submitE' value='Submit'></p>"
    print "<p><input type = 'submit' name='back' value='Main Page'></p>"
    print "</center><form>"

# send emails for new passwords
def sendEmail():
    cursor.execute("SELECT email_sec, email_pres, email_vp FROM secretary "
                   "WHERE ID = 1")
    emails = cursor.fetchall()
    print "<p><form method='POST' action='/cgi-bin/sec.py'>"
    print "<center>"
    print "<body style='background-color:00FFFF;'>"
    print"<h2>%s</h2>" % (message)
    for item in emails:
        email1 = item[0]
        email2 = item[1]
        email3 = item[2]
    msg = "\n%s" % (message)
    server.sendmail("email_address@email.com", [email1, email2, email3],
                    msg)
