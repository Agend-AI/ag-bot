import requests
from chatbot import Chat, register_call
from whatsappbot.db import registrar_usuario, usuario_existe, nome_usuario, listar_visitas_formatas
import datetime
dias_semana = {
    0: "segunda-feira",
    1: "terça-feira",
    2: "quarta-feira",
    3: "quinta-feira",
    4: "sexta-feira",
    5: "sábado",
    6: "domingo"
}
def dias_disponiveis_texto():
    dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira"]
    dias_formatado = ""
    for dia in dias:
        dias_formatado += dia.title() + "\n"
    return dias_formatado


@register_call("verificar_numero")
def verificar_numero(session, query: str):
    query = query.strip()
    if not usuario_existe(query):
        return "Olá, seja bem-vindo a Casa do Celso! Vi que você não possui cadastro conosco, gostaria de se cadastrar?\n" \
               "1 - Sim\n" \
               "2 - Não"
    return f"Olá, {nome_usuario(query)}, seja bem-vindo a Casa do Celso! O que você gostaria de fazer?\n" \
           "1 - Agendar visita\n" \
           "2 - Listar minhas visitas marcadas\n" \
           "3 - Conversar com o filho do Celso"

@register_call("cadastrar_numero")
def cadastrar_numero(session, query):
    nome, numero = query.split()
    registrar_usuario(numero, nome)
    return "Sejá bem-vindo :) O que você gostaria de fazer?\n" \
           "1 - Agendar visita\n" \
           "2 - Listar minhas visitas marcadas\n" \
           "3 - Conversar com o filho do Celso"


@register_call("escolhas")
def escolhas(session, query):
    escolha, numero = query.split()
    if escolha in "2 - listar minhas visitas marcadas":
        return listar_visitas_formatas(numero)
    if escolha in "1 - agendar visita":
        return "Temos disponibilidades nos dias:\n" + dias_disponiveis_texto()
    return "Não entendi, pode repetir?"

@register_call("escolha_dia")
def escolha_dia(session, query):
    escolha, numero = query.split()
    dias = ["segunda-feira", "terça-feira", "quarta-feira", "quinta-feira", "sexta-feira"]
    for dia in dias:
        if escolha.lower().strip() in dia.lower():
            session.memory["dia"] = escolha
            return "Quantas pessoas irão?"
    return "Desculpe mas não entendi, pode repetir?"

@register_call("quantidade_pessoas")
def quantidade_pessoas(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ")
    dia = session.memory["dia"]
    d_inicial = datetime.datetime(year=datetime.datetime.now().year,
                          month=datetime.datetime.now().month,
                          day=18,
                          hour=9, minute=0, second=0, microsecond=000)
    d_inicial = datetime.datetime.isoformat(d_inicial)
    d_inicial += "-03:00"

    d_final = datetime.datetime(year=datetime.datetime.now().year,
                                  month=datetime.datetime.now().month,
                                  day=18,
                                  hour=12, minute=0, second=0, microsecond=000)
    d_final = datetime.datetime.isoformat(d_final)
    d_final += "-03:00"
    response = {
        "summary": f"{nome_usuario(numero)} - {dia}",
        "description": numero+"\n"+escolha,
        "dateTimeStart": d_inicial,
        "dateTimeEnd": d_final
    }
    requests.post("https://agenda-ai-api.herokuapp.com/event", json=response)
    return "Visita agendada com sucesso!"

@register_call("pergunta_sim_nao")
def pergunta_sim_nao(session, query):
    if query.strip().lower() in ['s', 'sim', '1', 'si', 'y', 'yeah', 'yes', 'yep', 'claro']:
        return "Pode me informar seu nome?"
    return "Obrigado por entrar em contato! :)"


marcia = Chat(default_template="../templates/conversation.j2", language='pt-br')


while True:
    incoming_msg = input("mensagem enviada: ")
    numero = "+559184762085"
    incoming_msg = incoming_msg.replace(" ", "_")
    marcia_disse = marcia.say(numero + " " + incoming_msg)
    print(marcia_disse)

