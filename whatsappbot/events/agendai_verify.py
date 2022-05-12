from chatbot import register_call
from requests import get as get_api
from whatsappbot.services.validate_users import *
from whatsappbot.db import cadastros_novos

@register_call("verificar_numero")
def verificar_numero(session, query):
    print(session)
    print(query)
    return "Deseja cadastrar seu número?"


def verificar_cliente_possui_agendamentos(numero):
    cliente = get_api('https://marcia-api.herokuapp.com/cliente/numero/{}'.format(numero)).json()
    vendas = get_api('https://marcia-api.herokuapp.com/venda')
    vendas_status = vendas.status_code
    vendas = vendas.json()
    venda_cliente = []
    if len(vendas) > 0 and vendas_status == 200:
        venda_cliente = [v for v in vendas if v['clienteId'] == cliente['clienteId']]
    if len(venda_cliente) > 0:
        return True
    return False
