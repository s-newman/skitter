from ui import app
from time import sleep as wait
import MySQLdb
from binascii import hexlify

# Create mySQL connection
connection = None
while connection is None:
    try:
        connection = MySQLdb.connect(host='user-db', user='api-gateway',
                                     passwd='changemeplease-securitysucks',
                                     db='users')
    except Exception as e:
        wait(3)
        print(str(e))

c = connection.cursor()

# Open file
with open('ui/static/img/default-profile.png', 'rb') as f:
    picture = f.read()

# Insert file to database
hex_picture = '0x{}'.format(hexlify(picture).decode('ascii'))
c.execute('INSERT INTO PROFILE_PICTURE VALUES (0, %s)', (hex_picture,))
