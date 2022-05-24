from flask import Blueprint, request, current_app
from twilio.twiml.messaging_response import MessagingResponse
from whatsappbot.events import users_conversation


bp = Blueprint("conversation", __name__)

@bp.route("/")
def home():
    return "funfou"


@bp.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body').lower()
    numero = request.values.get('From').strip()
    resp = MessagingResponse()
    msg = resp.message()
    incoming_msg = incoming_msg.replace(" ", "_")
    numero = numero.replace("whatsapp:", "")
    incoming_msg = incoming_msg.lower().strip()
    if numero not in users_conversation:
        current_app.agendai.start_new_session(session_id=numero)
        users_conversation[numero] = True
    user_say = numero+" "+incoming_msg
    agendai_response = current_app.agendai.say(user_say)
    print(f"Mensagem enviada: {user_say}")
    print(f"Marcia respondeu: {agendai_response}")
    msg.body(agendai_response)
    return str(resp)

    
def init_app(app):
    app.register_blueprint(bp)
