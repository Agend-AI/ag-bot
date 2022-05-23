from chatbot import Chat
from .agendai_verify import *
import os
users_conversation = {

}
agendai = Chat(pairs=os.environ.get("TEMPLATE_PATH") or "../templates/conversation.template", default_template=os.environ.get("TEMPLATE_PATH") or "../templates/conversation.template", language='pt-br')



