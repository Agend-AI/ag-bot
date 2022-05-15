from chatbot import Chat, register_call
from whatsappbot.db import cadastros_novos as cadastros

dias_disponiveis = {
    "segunda": {"horarios": ["13:00", "14:00"], "data": "16/05/2022"},
    "quarta": {"horarios": ["14:00", "15:00"], "data": "18/05/2022"}
}

def dias_disponiveis_texto():
    dias = ""
    for i, dia in enumerate(dias_disponiveis.keys()):
        dias += str(i + 1) + " - " + dia.title() + " - " + dias_disponiveis[dia]["data"] + "\n"
    return dias

def horarios_do_dia_escolhido_texto(dia):
    horarios = ""
    for ii, horario in enumerate(dias_disponiveis[dia]["horarios"]):
        horarios += str(ii + 1) + " - " + horario + "\n"
    return horarios


@register_call("verificar_numero")
def verificar_numero(session, query: str):
    query = query.strip()
    if query not in cadastros:
        return "Olá, seja bem-vindo a Casa do Celso! Vi que você não possui cadastro conosco, gostaria de se cadastrar?\n" \
               "1 - Sim\n" \
               "2 - Não"
    return f"Olá, {cadastros[query]['nome']}, seja bem-vindo a Casa do Celso! O que você gostaria de fazer?\n" \
           "1 - Agendar visita\n" \
           "2 - Listar minhas visitas marcadas\n" \
           "3 - Conversar com o filho do Celso"

@register_call("cadastrar_numero")
def cadastrar_numero(session, query):
    nome, numero = query.split()
    cadastros[numero] = {
        "nome": nome,
        "visitas_marcadas": None,
        "forma_pagamento": None
    }
    return "Sejá bem-vindo :) O que você gostaria de fazer?\n" \
           "1 - Agendar visita\n" \
           "2 - Listar minhas visitas marcadas\n" \
           "3 - Conversar com o filho do Celso"


@register_call("escolhas")
def escolhas(session, query):
    escolha, numero = query.split()
    if escolha in "2 - listar minhas visitas marcadas":
        return listar_visitas(numero)
    if escolha in "1 - agendar visita":
        return "Temos disponibilidades nos dias:\n" + dias_disponiveis_texto()
    return "Seu contato está sendo redirecionado para o filho do Celso! Obrigado pelo que conversamos, te amo, bebê <3"

@register_call("escolha_dia")
def escolha_dia(session, query):
    escolha, numero = query.split()

    dias = dias_disponiveis_texto().split("\n")
    for i, dia in enumerate(dias):
        if escolha.lower().strip() in dia.lower():
            dia_escolhido = list(dias_disponiveis.keys())[i]
            session.memory["dia"] = dia_escolhido
            return "Possuímos os horários:\n" + horarios_do_dia_escolhido_texto(dia_escolhido)
    return "Desculpe mas não entendi, pode escolher um horário respondendo o número ou escrevendo o horário que listei " \
           "na mensagem anterior!"

@register_call("escolha_horario")
def escolha_dia(session, query):
    escolha, numero = query.split()
    horarios = horarios_do_dia_escolhido_texto(session.memory["dia"]).split("\n")
    hora_escolhida = -1
    for i, hora in enumerate(horarios):
        if escolha.lower().strip() in hora.lower():
            hora_escolhida = i
    nova_visita = f"{session.memory['dia'].title()} - "\
                  f"{dias_disponiveis[session.memory['dia']]['data']} - "\
                  f"às {dias_disponiveis[session.memory['dia']]['horarios'][hora_escolhida]}"
    if cadastros[numero.strip()]["visitas_marcadas"] is None:
        cadastros[numero.strip()]["visitas_marcadas"] = [nova_visita]
    else:
        cadastros[numero.strip()]["visitas_marcadas"].append(nova_visita)
    return "Muito bem, sua visita foi agendada com SUCESSO!!!!!!! AEHOOOOOOO PORRRRRRRAA"

def listar_visitas(usuario):
        visitas = "Suas visitas são:\n"
        if not cadastros[usuario]["visitas_marcadas"]:
            return cadastros[usuario]["nome"]+", você não possui visitar agendadas! :O, gostaria de agendar?\n" \
                                            "1 - Sim\n" \
                                            "2 - Não"
        for visita in cadastros[usuario]["visitas_marcadas"]:
            visitas += visita+"\n"
        return visitas

@register_call("pergunta_deseja_cadastrar")
def teste(session, query):
    print(query)
    return query

@register_call("pergunta_sim_nao")
def pergunta_sim_nao(session, query):
    if query.strip().lower() in ['s', 'sim', '1', 'si', 'y', 'yeah', 'yes', 'yep', 'claro']:
        return "Pode me informar seu nome?"
    return "Obrigado por entrar em contato! :)"


marcia = Chat(default_template="../templates/conversation.j2", language='pt-br')


while True:
    incoming_msg = input("mensagem enviada: ")
    numero = "+559184762085"
    marcia_disse = marcia.say(numero + " " + incoming_msg)
    print(marcia_disse)

