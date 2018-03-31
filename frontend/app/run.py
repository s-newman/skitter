from ui import app
from time import sleep as wait
import mysql.connector
from binascii import hexlify

# Create mySQL connection
cnx = None
while cnx is None:
    try:
        cnx = mysql.connector.connect(host='user-db', user='api-gateway',
                                      passwd='changemeplease-securitysucks',
                                      db='users')
    except Exception as e:
        wait(3)
        print(str(e))

c = cnx.cursor()

# Open file
with open('ui/static/img/default-profile.png', 'rb') as f:
    picture = f.read()

# Insert file to database
c.execute('INSERT INTO PROFILE_PICTURE VALUES (0, %s)', (hex_picture,))

# Close connection
cnx.close()