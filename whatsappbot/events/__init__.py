from chatbot import Chat
from .agendai_verify import *
from .register import *
from .alert import *


marcia = Chat(default_template="whatsappbot/templates/conversation.j2", language='pt-br')