import requests
from chatbot import register_call
from whatsappbot.db import registrar_usuario, usuario_existe, nome_usuario, \
    listar_visitas_formatas, limpar_registros, \
    ultima_visita_agendada_formatada, API_EVENTS, \
    pegar_id_visita, pegar_todos_os_id_visitas
from whatsappbot.services.weekday import *
from whatsappbot.services.regex_validation import *

opcoes = [
          "1 - Agendar visita",
          "2 - Listar minhas visitas marcadas",
          "3 - Alterar/Remarcar visita marcada",
          "4 - Cancelar/Desmarcar visita marcada"
          ]
opcoes_dict = {
    "agendar": opcoes[0],
    "listar": opcoes[1],
    "alterar": opcoes[2],
    "cancelar": opcoes[3]
}

def opcoes_escolhas():
    return "\n".join(opcoes)


@register_call("escolha_e_verificar_numero")
def escolha_e_verificar_numero(session, query: str):
    numero, escolha = query.split()
    if not usuario_existe(numero):
        session.memory["escolha_antecipada"] = escolha
        return "Olá, seja bem-vindo a Casa do Celso! Vi que você não possui cadastro conosco, gostaria de se cadastrar?\n" \
               "1 - Sim\n" \
               "2 - Não"
    if escolha in opcoes_dict["listar"].lower() or escolha in ["listar", "agendamentos", "eventos",
                                                                      "listar viagens"]:
        return listar_visitas_formatas(numero)
    if escolha in opcoes_dict["agendar"].lower() or escolha in ["agendar", "agendar evento", "criar agendamento"]:
        return "Temos disponibilidades nos dias:\n" + get_days_options_format()

    if escolha in opcoes_dict["alterar"].lower() or escolha in ["remarcar", "alterar data", "mudar visita"]:
        return "Escolha abaixo o número da visita que deseja *alterar*:\n" + listar_visitas_formatas(numero)

    if escolha in opcoes_dict["cancelar"].lower() or escolha in ["cancelar", "excluir", "desmarcar", "desmarca", "exclui", "cancela"]:
        return "Qual das visitas abaixo você gostaria de *desmarcar* (*Cancelar*)? Diga o número da visita:\n" + listar_visitas_formatas(
            numero)

@register_call("verificar_numero")
def verificar_numero(session, query: str):
    query = query.strip()
    if not usuario_existe(query):
        return "Olá, seja bem-vindo a Casa do Celso! Vi que você não possui cadastro conosco, gostaria de se cadastrar?\n" \
               "1 - Sim\n" \
               "2 - Não"
    return f"Olá, {nome_usuario(query).title()}, seja bem-vindo a Casa do Celso! O que você gostaria de fazer?\n" \
           + opcoes_escolhas()


@register_call("cadastrar_numero")
def cadastrar_numero(session, query):
    nome, numero = query.split()
    nome = nome.replace("_", " ").strip()
    registrar_usuario(numero, nome)
    if "escolha_antecipada" not in session.memory:
        return "Sejá bem-vindo :) O que você gostaria de fazer?\n" \
               + opcoes_escolhas()

    if session.memory["escolha_antecipada"] in opcoes_dict["listar"].lower() or session.memory[
        "escolha_antecipada"] in ["listar", "agendamentos", "eventos", "listar viagens"]:
        return listar_visitas_formatas(numero)
    if session.memory["escolha_antecipada"] in opcoes_dict["agendar"].lower() or session.memory["escolha_antecipada"] in [
        "agendar", "agendar evento", "criar agendamento"]:
        return "Temos disponibilidades nos dias:\n" + get_days_options_format()
    if session.memory["escolha_antecipada"] in opcoes_dict["alterar"].lower() or session.memory["escolha_antecipada"] in ["remarcar", "alterar data", "mudar visita"]:
        return "Escolha abaixo o número da visita que deseja alterar:\n" + listar_visitas_formatas(numero)
    if session.memory["escolha_antecipada"] in opcoes_dict["cancelar"].lower() or session.memory["escolha_antecipada"] in ["cancelar", "excluir", "desmarcar", "desmarca", "exclui", "cancela"]:
        return "Qual das visitas abaixo você gostaria de *desmarcar* (*Cancelar*)? Diga o número da visita:\n" + listar_visitas_formatas(
            numero)


@register_call("escolhas")
def escolhas(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ").strip().lower()
    print("Escolha opção: ", escolha)
    if escolha in opcoes_dict["listar"].lower() or escolha in ["listar", "agendamentos", "eventos",
                                                                      "listar viagens"]:
        return listar_visitas_formatas(numero)
    if escolha in opcoes_dict["agendar"].lower() or escolha in ["agendar", "agendar evento", "criar agendamento"]:
        return "Temos disponibilidades nos dias:\n" + get_days_options_format()
    if escolha in opcoes_dict["alterar"].lower() or escolha in ["remarcar", "alterar data", "mudar visita"]:
        return "Escolha abaixo o número da visita que deseja *alterar*:\n" + listar_visitas_formatas(numero)
    if escolha in opcoes_dict["cancelar"].lower() or escolha in ["cancelar", "excluir", "desmarcar", "desmarca", "exclui", "cancela"]:
        return "Qual das visitas abaixo você gostaria de *desmarcar* (*Cancelar*)? Diga o número da visita:\n" + listar_visitas_formatas(
            numero)

    return "Não entendi, pode repetir?"


@register_call("alterar_visita_dia")
def alterar_visita_dia(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ").strip().lower()
    session.memory["index_dia"] = escolha
    return "Para qual dia você gostaria de remarcar?\n" + get_days_options_format()


@register_call("alterar_visita_pessoas")
def alterar_visita_pessoas(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ").strip().lower()
    session.memory["dia"] = escolha
    return "Para quantas pessoas?"


@register_call("alterar_visita_concluida")
def alterar_visita_pessoas(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ").strip().lower()
    dia = session.memory["dia"]
    dia = validar_dia(dia)
    dia = int(dia)
    d_inicial = getDayFormatted(dia)
    d_final = getDayFormatted(dia, 12)
    response = create_response(numero, dia, escolha, d_inicial, d_final)
    url = API_EVENTS + "/" + pegar_id_visita(numero, int(session.memory["index_dia"]))
    requests.put(url, json=response)
    return "Ótimo! Você remarcou sua visita para:\n" + ultima_visita_agendada_formatada(numero)


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
    dia = validar_dia(dia)
    dia = int(dia)
    d_inicial = getDayFormatted(dia)
    d_final = getDayFormatted(dia, 12)
    response = create_response(numero, dia, escolha, d_inicial, d_final)

    requests.post(API_EVENTS, json=response)
    return "Visita agendada com sucesso!"


def validar_dia(dia):
    if GET_DATA.search(dia):
        dia = GET_DATA.search(dia).group()
        dia = get_day_from_data(dia)
        return dia
    elif GET_OPTION.search(dia):
        dia = GET_OPTION.search(dia).group()
        dias = get_days_options_format().split("\n")
        dia = dias[int(dia) - 1]
        dayname = GET_DAYNAME.search(dia).group()
        dia = get_day_from_dayname(dayname)
        return dia
    elif GET_DAYNAME.search(dia):
        dia = GET_DAYNAME.search(dia).group()
        dia = get_day_from_dayname(dia)
        return dia
    else:
        return "Desculpe, não consegui identificar o dia escolhido!"


@register_call("pergunta_sim_nao")
def pergunta_sim_nao(session, query):
    if query.strip().lower() in ['s', 'sim', '1', 'si', 'y', 'yeah', 'yes', 'yep', 'claro']:
        return "Pode me informar seu nome?"
    return "Obrigado por entrar em contato! :)"


@register_call("esquecer_usuario")
def esquecer_usuario(session, query):
    limpar_registros()
    return "Esquecido!"


@register_call("ultima_visita")
def ultima_visita(session, query):
    escolha, numero = query.split()
    ultima = ultima_visita_agendada_formatada(numero)
    return "A sua última visita agendada é:\n" + ultima


@register_call("excluir_visita")
def excluir_visita(session, query):
    escolha, numero = query.split()
    escolha = escolha.replace("_", " ").strip().lower()
    url = API_EVENTS + "/" + pegar_id_visita(numero, int(escolha))
    requests.delete(url)
    return "Sua visita foi *desmarcada* (*cancelada*)!!"


@register_call("excluir_todas_visitas")
def excluir_todas_visitas(session, query):
    escolha, numero = query.split()
    ids = pegar_todos_os_id_visitas(numero)
    for id_v in ids:
        url = API_EVENTS + "/" + id_v
        requests.delete(url)
    return "Todas as suas visitas foram *desmarcadas* (*excluídas*)!!"


def create_response(numero, dia, escolha, data_inicial, data_final):
    return {
        "summary": f"{nome_usuario(numero)} - {get_dayname_from_day(dia)}",
        "description": numero + "\n" + escolha,
        "dateTimeStart": data_inicial,
        "dateTimeEnd": data_final
    }
