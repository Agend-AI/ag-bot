import os

from chatbot import Chat
from flask import Flask
from .extensions.configuration import load_modules
from .extensions.configuration import init_app as init_conf
from .services.weekday import start_thread


def create_app():
    app = Flask(__name__)
    start_thread()
    init_conf(app)
    load_modules(app)
    app.agendai = Chat(pairs=os.environ.get("TEMPLATE_PATH") or "../templates/conversation.template",
                       default_template=os.environ.get("TEMPLATE_PATH") or "../templates/conversation.template",
                       language='pt-br')
    return app

