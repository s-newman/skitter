from ui import app
import MySQLdb

# Create mySQL connection
connection = None
while connection is None:
    try:
        connection = MySQLdb.connect(host='user-db', user='api-gateway',
                                     passwd='changemeplease-securitysucks',
                                     db='users')
    except:
        pass

c = connection.cursor()

# Open file
with open('ui/static/img/default-profile.png') as f:
    picture = f.read()

# Insert file to database
hex_picture = '0x{}'.format(binascii.hexlify(image).decode('ascii'))
c.execute('INSERT INTO PROFILE_PICTURE VALUES (0, %s)', (hex_picture,))