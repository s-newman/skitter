from flask import Flask

app = Flask(__name__)

from following import routes
