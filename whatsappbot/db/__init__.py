import json
from whatsappbot.services.regex_validation import *
from whatsappbot.services.weekday import *
import requests
import os

API_EVENTS = "https://agenda-ai-api.herokuapp.com/event"
path_arquivo = os.environ.get("DB_PATH") or "../../cadastros.json"

def registrar_usuario(numero, nome):
    usuarios_file = open(path_arquivo)
    usuarios = usuarios_file.read()
    usuarios_file.close()
    usuarios = json.loads(usuarios)
    usuarios.append({
        "nome": nome,
        "numero": numero,
        "agenda": None
    })
    usuarios_file = open(path_arquivo, "w")
    usuarios_file.write(json.dumps(usuarios))
    usuarios_file.close()

def usuario_existe(numero):
    usuarios_file = open(path_arquivo)
    usuarios = usuarios_file.read()
    usuarios_file.close()
    usuarios = json.loads(usuarios)
    for u in usuarios:
        if numero == u["numero"]:
            return True
    return False

def pegar_usuario(numero):
    usuarios_file = open(path_arquivo)
    usuarios = usuarios_file.read()
    usuarios_file.close()
    usuarios = json.loads(usuarios)
    for u in usuarios:
        if numero == u["numero"]:
            return u
    return {"nome": "Não encontrado"}

def nome_usuario(numero):
    return pegar_usuario(numero)["nome"]

def listar_visitas(numero):
    visitas = []
    for v in requests.get(API_EVENTS).json():
        numero_req = v["description"]
        numero_req = GET_NUMBER.search(numero_req)
        if numero_req:
            numero_req = numero_req.group().strip()
        if numero_req == numero:
            visitas.append(v)
    return visitas

def listar_visitas_formatas(numero):
    visitas = listar_visitas(numero)
    visitas_formatadas = ""
    for i, v in enumerate(visitas):
        data = convert_data_to_dd_mm_yyyy(v['start']['dateTime'])
        formatar_data = f"{get_dayname_from_data(data).title()} ({data})"
        description = v['description'].replace(numero, "")
        visitas_formatadas += f"*Visita: {i+1}*:\n{v['summary']}\n{description}\nMarcado para: {formatar_data} ---\n\n"
    return visitas_formatadas


def ultima_visita_agendada_formatada(numero):
    visitas = listar_visitas_formatas(numero).split("---")
    visitas = [v.strip() for v in visitas if v != '\n\n']
    visita = visitas[-1]
    return visita

def pegar_id_visita(numero, visita_alterar):
    visitas = listar_visitas(numero)
    visita_alterar = visitas[visita_alterar-1]
    visita_id = visita_alterar["id"]
    return visita_id

def pegar_todos_os_id_visitas(numero):
    visitas = listar_visitas(numero)
    ids = [v["id"] for v in visitas]
    return ids

def limpar_registros():
    usuarios_file = open(path_arquivo, "w")
    usuarios_file.write("[]")
    usuarios_file.close()
