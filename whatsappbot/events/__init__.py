from chatbot import Chat
from .agendai_verify import *

users_conversation = {

}

def create_bot():
    return Chat(default_template="whatsappbot/templates/conversation.j2", language='pt-br')