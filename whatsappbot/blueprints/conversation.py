from flask import Blueprint, request
from twilio.twiml.messaging_response import MessagingResponse
from whatsappbot.events import create_bot, users_conversation


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
        agendai_bot = create_bot()
        users_conversation[numero] = agendai_bot
    tentativa_resposta_correta = 10
    tentativas = 0
    agendai_response = "Desculpa, não entendi"
    while tentativas < tentativa_resposta_correta and agendai_response == "Desculpa, não entendi":
        agendai_response = users_conversation[numero].say(numero+" "+incoming_msg)
        tentativas += 1
    print(f"Mensagem enviada: {numero} {incoming_msg}")
    print(f"Marcia respondeu: {agendai_response}")
    msg.body(agendai_response)
    return str(resp)

    
def init_app(app):
    app.register_blueprint(bp)
