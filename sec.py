#!/usr/bin/python
print "Content-type: text/html"
print
print "<html><head>"
print "</head><body>"
import cgi
form = cgi.FieldStorage()
import mysql.connector
import hashlib
from utils import printPage, changePass, numbers, editNums, buttons, emails, \
                  sendEmail
cnx = mysql.connector.connect(user='<your db user>',
                              database='<your db name>')
cursor = cnx.cursor()

if "login" in form:
    if "email" not in form:
        # ask for missing information (email address)
        printPage("Enter username")
    elif "pwd" not in form:
        # ask for missing information (password)
        printPage("Enter password")
    else:
        # check to see if login information matches
        hash_pwd = hashlib.sha224(form["pwd"].value).hexdigest()
        query2 = ("SELECT email_sec, email_pres, email_vp, password "
                  "FROM secretary WHERE password = %s AND email_sec = %s "
                  "OR password = %s AND email_pres = %s OR password = %s "
                  "AND email_vp = %s")
        cursor.execute(query2, (hash_pwd, form["email"].value, hash_pwd,
                       form["email"].value, hash_pwd, form["email"].value))
        rows = cursor.fetchall()
        cursor.close()

        # Incorrect Info, request login information again
        if rows == []:
            printPage("Incorrect Info")
        else:
            numbers("You are now logged in")

if "forgot" in form:
    # Create new, random-generated password
    import uuid
    password = str(uuid.uuid4())
    password = password.replace("-", "")
    password = password[0: 7]

    # send the password through email
    import smtplib
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    message = "New Delta Text password: " + password
    hashed_pwd = hashlib.sha224(password).hexdigest()

    # change the password in mysql
    cursor = cnx.cursor()
    cursor.execute("UPDATE secretary SET password = %s WHERE ID = %s ",
                   (hashed_pwd, 1))
    cnx.commit()

    # Logging in to server
    server.login("email_address@gmail.com", "password")

    # Send the email
    try:
        sendEmail()
    except:
        print "<p>There was a problem sending the password to emails</p>"
    else:
        print "<p>New Password Sent to your emails</p>"
    print "<a href='http://localhost/secretary.html'>Return to Log In</a>"


# If user clicks 'Change Password'
if 'changeP' in form:
    changePass("")
if 'submitP' in form and 'oldpw' not in form:
    changePass("Must Enter Current Password")
elif 'submitP' in form and 'newpw' not in form or 'submitP' in form and \
                                                  'newpw2' not in form:
    changePass("Must Enter New Password")
elif 'submitP' in form and 'oldpw' in form and 'newpw' in form and \
                                                 'newpw2' in form:
    oldpw_hashed = hashlib.sha224(form['oldpw'].value).hexdigest()
    cursor.execute("SELECT password FROM secretary WHERE password = %s AND "
                   "ID = %s", (oldpw_hashed, 1))
    rows2 = cursor.fetchall()
    if form["newpw"].value != form["newpw2"].value:
        changePass("Passwords do not match")
        # Incorrect Info, request login information again
    elif rows2 == []:
        changePass("Current password incorrect")
    else:
        # change the password in mysql
        import smtplib
        newpwd = hashlib.sha224(form["newpw"].value).hexdigest()
        cursor = cnx.cursor()
        cursor.execute("UPDATE secretary SET password = %s WHERE ID = %s ",
                       (newpwd, 1))
        cnx.commit()
        # send the password through email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        message = "New Delta Text password: " + form["newpw"].value
        # Logging in to server
        server.login("email_address@email.com", "password")
        # Send the email
        try:
            sendEmail()
        except:
            print "<p>There was a problem sending the password to emails</p>"
        else:
            print "<p>New Password Sent to your emails</p>"
        print "<p><form method='POST' action='/cgi-bin/sec.py'>"
        print "<center>"
        print "<body style='background-color:00FFFF;'>"
        print "<p>New Password Sent to your emails</p>"
        print "<p><input type = 'submit' name='back' value='Main Page'></p>"
        print "</center></form>"

# User clicks 'Change Emails
if 'changeE' in form:
    emails("Change emails")

# User clicks Submit
if 'submitE' in form:

    # Changes the email address saved in table for each
    if 'email1' in form:
        cursor.execute("UPDATE secretary SET email_sec = %s WHERE ID = %s",
                       (form["email1"].value, 1))
        cnx.commit()
    if 'email2' in form:
        cursor.execute("UPDATE secretary SET email_pres = %s WHERE ID = %s",
                       (form["email2"].value, 1))
        cnx.commit()
    if 'email3' in form:
        cursor.execute("UPDATE secretary SET email_vp = %s WHERE ID = %s",
                       (form["email3"].value, 1))
        cnx.commit()

    # Prints the page again with the changed emails
    emails("Emails have been changed")

# If user clicks 'main page' takes them back to main page
if 'back' in form:
    numbers("")
# Edit Numbers
if 'edit' in form:
    # Table with edit buttons
    editNums()
    print "</table>"
    buttons()
    print "</center></form>"

# Keeps track of number of rows in table, numbers
cursor.execute("SELECT ID FROM numbers")
rows = cursor.fetchall()
countMain = 1
for row in rows:
    countMain += 1

# If editName + any number from 1 to the number of entries in table
for x in range(1, countMain):
    if ('editName' + str(x)) in form:
        print "<form method ='POST' action='/cgi-bin/sec.py'>"
        print "<center>"
        print "<body style='background-color:00FFFF;'>"
        cursor = cnx.cursor()

        # Iterate through the rows of data in table 'numbers' and print them
        cursor.execute("SELECT Name, Number, Provider FROM numbers")
        rows = cursor.fetchall()
        print "<table border='5' width=42% align='center'>"
        print "<tr>"
        print   "<th>Name</th>"
        print   "<th>Number</th>"
        print   "<th>Provider</th>"
        print "</tr>"

        # Variable that will keep track of each row
        count3 = 1

        # Prints table again but with a text box where the user clicked 'edit'
        #     and a button to submit
        for row in rows:
            print "<tr>"
            if ('editName' + str(count3)) == ('editName' + str(x)):
                print "<td><input type = 'text' name = %s><input type='submit' "\
                      "name=%s value='OK'</td>" % ('newName' + str(x),
                                                   'submitName' + str(x))
            else:
                print   "<td>%s<input type='submit' name=%s value='Edit'>"\
                        "</td>" % (row[0], "editName" + str(count3))
            print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                    % (row[1], "editNum" + str(count3))
            print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                    % (row[2], "editPro" + str(count3))
            print "</tr>"
            count3 += 1
        print "</table>"
        buttons()
        print "</center></form>"

# When the 'OK' button for the Name corresponding to the box being edited is
#     clicked, the change will be made in mysql
for x in range(1, countMain):
    if ('submitName' + str(x)) in form:
        cursor = cnx.cursor()
        cursor.execute("UPDATE numbers SET Name = %s WHERE ID = %s ",
                       ((form['newName' + str(x)].value), x))
        cnx.commit()

        # Table is printed with edit buttons
        editNums()
        print "</table>"
        buttons()
        print "</center></form>"

# If editNum + any number from 1 to the number of entries in table
for x in range(1, countMain):
    if ('editNum' + str(x)) in form:
        print "<form method ='POST' action='/cgi-bin/sec.py'>"
        print "<center>"
        print "<body style='background-color:00FFFF;'>"
        cursor = cnx.cursor()

        # Iterate through the rows of data in table 'numbers' and print them
        cursor.execute("SELECT Name, Number, Provider FROM numbers")
        rows = cursor.fetchall()
        print "<table border='5' width=42% align='center'>"
        print "<tr>"
        print   "<th>Name</th>"
        print   "<th>Number</th>"
        print   "<th>Provider</th>"
        print "</tr>"

        # Variable that will keep track of each row
        count3 = 1

        # Prints the table again but with a text box where the user clicked
        #     'edit' and a button to submit
        for row in rows:
            print "<tr>"
            print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                    % (row[0], "editName" + str(count3))
            if ('editNum' + str(count3)) == ('editNum' + str(x)):
                print   "<td><input type = 'text' name = %s>"\
                        "<input type='submit' name=%s value='OK'</td>" \
                        % ('newNum' + str(x), 'submitNum' + str(x))
            else:
                print   "<td>%s<input type='submit' name=%s value='Edit'>"\
                        "</td>" % (row[1], "editNum" + str(count3))
            print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                    % (row[2], "editPro" + str(count3))
            print "</tr>"
            count3 += 1
        print "</table>"
        buttons()
        print "</center></form>"

# When the 'OK' button (for numbers) corresponding to the box being edited is
#     clicked, the change will be made in mysql
for x in range(1, countMain):
    if ('submitNum' + str(x)) in form:
        cursor = cnx.cursor()
        cursor.execute("UPDATE numbers SET Number = %s WHERE ID = %s ",
                       ((form['newNum' + str(x)].value), x))
        cnx.commit()

        # Print Table with edit buttons
        editNums()
        print "</table>"
        buttons()
        print "</center></form>"

# If editPro + any number from 1 to the number of entries in table
for x in range(1, countMain):
    if ('editPro' + str(x)) in form:
        print "<form method ='POST' action='/cgi-bin/sec.py'>"
        print "<center>"
        print "<body style='background-color:00FFFF;'>"
        cursor = cnx.cursor()

        # Iterate through the rows of data in table 'numbers' and print them
        cursor.execute("SELECT Name, Number, Provider FROM numbers")
        rows = cursor.fetchall()
        print "<table border='5' width=42% align='center'>"
        print "<tr>"
        print   "<th>Name</th>"
        print   "<th>Number</th>"
        print   "<th>Provider</th>"
        print "</tr>"

        # Variable that will keep track of each row
        count3 = 1

        # Prints the table again but with a text box where the user clicked
        #    'edit' and a button to submit
        for row in rows:
            print "<tr>"
            print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                    % (row[0], "editName" + str(count3))
            print   "<td>%s<input type='submit' name=%s value='Edit'></td>" \
                    % (row[1], "editNum" + str(count3))
            if ('editPro' + str(count3)) == ('editPro' + str(x)):
                print "<td><select name='newPro'>"
                print   "<option value='ATT'>ATT</option>"
                print   "<option value='T-Mobile'>T-Mobile</option>"
                print   "<option value='Verizon'>Verizon</option>"
                print   "<option value='Sprint'>Sprint</option>"
                print "</select>"
                print "<input type='submit' name=%s value='OK'></td>" \
                      % ("submitPro" + str(count3))
            else:
                print   "<td>%s<input type='submit' name=%s value='Edit'>"\
                        "</td>" % (row[2], "editPro" + str(count3))
            print "</tr>"
            count3 += 1
        print "</table>"
        buttons()
        print "</center></form>"

# When the 'OK' button (for numbers) corresponding to the box being edited
#     is clicked, the change will be made in mysql
for x in range(1, countMain):
    if ('submitPro' + str(x)) in form:
        cursor = cnx.cursor()
        cursor.execute("UPDATE numbers SET Provider = %s WHERE ID = %s ",
                       ((form['newPro'].value), x))
        cnx.commit()
        # Print Table with edit buttons
        editNums()
        print "</table>"
        buttons()
        print "</center></form>"

# If user clickes Add Number
if 'addNumber' in form:
    # Print table with edit buttons
    editNums()
    # Creates a new row in the table with text areas to be filled in for name
    #     and number
    print "<tr>"
    print   "<td><input type='text' name=%s></td>" % ("addName")
    print   "<td><input type='text' name=%s></td>" % ("addNum")
    # Creates drop down for provider with 4 options
    print "<td><select name='addPro'>"
    print   "<option value='ATT'>ATT</option>"
    print   "<option value='T-Mobile'>T-Mobile</option>"
    print   "<option value='Verizon'>Verizon</option>"
    print   "<option value='Sprint'>Sprint</option>"
    print "</select>"
    print "</table>"
    # Button to submit these values
    print "<input type='submit' name=%s value='Submit'>" % ("submitInfo")
    buttons()
    print "</center></form>"

# If the button to submit the new info is clicked, it will update table
#      and print out table again
if 'submitInfo' in form:

    # If the user does not type anything for Name or Number
    if 'addName' not in form or 'addNum' not in form:
        # Table is printed again
        editNums()
        buttons()
        print "</table>"
        print "</center></form>"

    # If the user properly fills in all info
    else:
        # Updates MySQL table
        cursor = cnx.cursor()
        cursor.execute("INSERT INTO numbers (Name, Number, Provider, id) "
                       "VALUES (%s, %s, %s, %s)", (form["addName"].value,
                                                   form["addNum"].value,
                                                   form["addPro"].value,
                                                   countMain))
        cnx.commit()
        # Table is printed again
        editNums()
        print "</table>"
        buttons()
        print "</center></form>"

# If the user clicks Delete Number
if 'deleteNumber' in form:
    # Table is printed again
    print "<form method ='POST' action='/cgi-bin/sec.py'>"
    print "<center>"
    print "<body style='background-color:00FFFF;'>"

    # Iterate through the rows of data in table 'numbers' and print them
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
        # Prints out a delete button before the name in each ro
        print   "<td><input type='submit' name=%s value='Delete'>%s</td>" \
                % (("delete" + str(count)), row[0])
        print   "<td>%s</td>" % (row[1])
        print   "<td>%s</td>" % (row[2])
        print "</tr>"
        count += 1

    print "</table>"
    print "<p><input type='submit' name='edit' value='Edit Numbers'>"
    print "<input type='submit' name='addNumber' value='Add Number'></p>"
    print "<p><input type = 'submit' name='back' value='Main Page'></p>"
    print "<p><a href='/cgi-bin/mainPage.py'>Home Page</a></p>"
    print "</center></form>"

# For every number from 1 to the number of entries in the table
for x in range(1, countMain):

    # If the delete button corresponding to any row is clicked
    if ("delete" + str(x)) in form:

        # Delete that entire entry
        cursor = cnx.cursor()
        cursor.execute("DELETE FROM numbers WHERE ID = %s and ID = %s", (x, x))
        cnx.commit()

        # Resets ID numbers
        i = 1
        cursor.execute("SELECT Name, Number, Provider FROM numbers")
        rows = cursor.fetchall()
        for row in rows:
            cursor.execute("UPDATE numbers SET ID = %s WHERE Number = %s",
                           (i, row[1]))
            cnx.commit()
            i += 1

        # Table is printed again
        print "<form method ='POST' action='/cgi-bin/sec.py'>"
        print "<center>"
        print "<body style='background-color:00FFFF;'>"

        # Iterate through the rows of data in table 'numbers' and print them
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
            print   "<td><input type='submit' name=%s value='Delete'>%s</td>" \
                    % ("delete" + str(count), row[0])
            print   "<td>%s</td>" % (row[1])
            print   "<td>%s</td>" % (row[2])
            print "</tr>"
            count += 1

        print "</table>"
        print "<p><input type='submit' name='edit' value='Edit Numbers'>"
        print "<input type='submit' name='addNumber' value='Add Number'></p>"
        print "<p><input type = 'submit' name='back' value='Main Page'></p>"
        print "<p><a href='/cgi-bin/mainPage.py'>Home Page</a></p>"
        print "</center></form>"

print "</body></html>"
