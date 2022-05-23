from chatbot import Chat
from .agendai_verify import *
import os
users_conversation = {

}
agendai = Chat(default_template=os.environ.get("TEMPLATE_PATH") or "../templates/conversation.j2", language='pt-br')



