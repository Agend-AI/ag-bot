from whatsappbot.services.weekday import *
from whatsappbot.events import users_conversation, agendai


while True:
    incoming_msg = input("mensagem enviada: ")
    numero = "+559184762085"
    incoming_msg = incoming_msg.replace(" ", "_").lower()
    resp = numero + ":" + incoming_msg
    if numero not in users_conversation:
        agendai.start_new_session(session_id=numero)
        users_conversation[numero] = True
    print(resp)
    marcia_disse = agendai.say(resp, session_id=numero)
    print(marcia_disse)
