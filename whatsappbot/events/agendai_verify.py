import requests
from chatbot import register_call
from whatsappbot.db import registrar_usuario, usuario_existe, nome_usuario, listar_visitas_formatas, limpar_registros
from whatsappbot.services.weekday import *
from whatsappbot.services.regex_validation import *

@register_call("escolha_e_verificar_numero")
def escolha_e_verificar_numero(session, query: str):
    numero, escolha = query.split()
    if not usuario_existe(numero):
        session.memory["escolha_antecipada"] = escolha
        return "Olá, seja bem-vindo a Casa do Celso! Vi que você não possui cadastro conosco, gostaria de se cadastrar?\n" \
               "1 - Sim\n" \
               "2 - Não"
    if escolha in "2 - listar minhas visitas marcadas" or escolha in ["listar", "agendamentos", "eventos",
                                                                      "listar viagens"]:
        return listar_visitas_formatas(numero)
    if escolha in "1 - agendar visita" or escolha in ["agendar", "agendar evento", "criar agendamento"]:
        return "Temos disponibilidades nos dias:\n" + get_days_options_format()


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
    nome = nome.replace("_", " ").strip()
    registrar_usuario(numero, nome)
    if "escolha_antecipada" not in session.memory:
        return "Sejá bem-vindo :) O que você gostaria de fazer?\n" \
               "1 - Agendar visita\n" \
               "2 - Listar minhas visitas marcadas\n" \
               "3 - Conversar com o filho do Celso"

    if session.memory["escolha_antecipada"] in "2 - listar minhas visitas marcadas" or session.memory[
        "escolha_antecipada"] in ["listar", "agendamentos", "eventos", "listar viagens"]:
        return listar_visitas_formatas(numero)
    if session.memory["escolha_antecipada"] in "1 - agendar visita" or session.memory["escolha_antecipada"] in [
        "agendar", "agendar evento", "criar agendamento"]:
        return "Temos disponibilidades nos dias:\n" + get_days_options_format()


@register_call("escolhas")
def escolhas(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ").strip().lower()
    print("Escolha opção: ", escolha)
    if escolha in "2 - listar minhas visitas marcadas":
        return listar_visitas_formatas(numero)
    if escolha in "1 - agendar visita":
        return "Temos disponibilidades nos dias:\n" + get_days_options_format()
    return "Não entendi, pode repetir?"


@register_call("escolha_dia")
def escolha_dia(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ").strip().lower()
    print("Escolha dia: ", escolha)
    dias = get_days_options_format().split("\n")
    for dia in dias:
        if escolha.lower().strip() in dia.lower():
            session.memory["dia"] = escolha
            return "Quantas pessoas irão?"
    return "Desculpe mas não entendi, pode repetir?"


@register_call("quantidade_pessoas")
def quantidade_pessoas(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ").strip().lower()
    dia = session.memory["dia"]

    if GET_DATA.search(dia):
        dia = GET_DATA.search(dia).group()
        dia = get_day_from_data(dia)

    elif GET_OPTION.search(dia):
        dia = GET_OPTION.search(dia).group()
        dias = get_days_options_format().split("\n")
        dia = dias[int(dia)-1]
        dayname = GET_DAYNAME.search(dia).group()
        dia = get_day_from_dayname(dayname)
    elif GET_DAYNAME.search(dia):
        dia = GET_DAYNAME.search(dia).group()
        dia = get_day_from_dayname(dia)
    else:
        return "Desculpe, não consegui identificar o dia escolhido!"

    dia = int(dia)
    d_inicial = getDayFormatted(dia)
    d_final = getDayFormatted(dia, 12)
    response = create_response(numero, dia, escolha, d_inicial, d_final)

    requests.post("https://agenda-ai-api.herokuapp.com/event", json=response)
    return "Visita agendada com sucesso!"


@register_call("pergunta_sim_nao")
def pergunta_sim_nao(session, query):
    if query.strip().lower() in ['s', 'sim', '1', 'si', 'y', 'yeah', 'yes', 'yep', 'claro']:
        return "Pode me informar seu nome?"
    return "Obrigado por entrar em contato! :)"


@register_call("esquecer_usuario")
def esquecer_usuario(session, query):
    limpar_registros()
    return "Esquecido!"


def create_response(numero, dia, escolha, data_inicial, data_final):
    return {
        "summary": f"{nome_usuario(numero)} - {get_dayname_from_day(dia)}",
        "description": numero + "\n" + escolha,
        "dateTimeStart": data_inicial,
        "dateTimeEnd": data_final
    }
