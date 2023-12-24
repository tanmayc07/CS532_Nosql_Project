from flask import Flask
import os

templates_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates'))
app = Flask(__name__, template_folder=templates_path)

from app import routes