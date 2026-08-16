"""
Padroniza o formato das respostas JSON da API, para o frontend sempre
saber onde encontrar os dados e as mensagens de erro.
"""
from flask import jsonify


def sucesso(dados=None, mensagem=None, status=200):
    corpo = {"sucesso": True}
    if mensagem:
        corpo["mensagem"] = mensagem
    if dados is not None:
        corpo["dados"] = dados
    return jsonify(corpo), status


def erro(mensagem, status=400, detalhes=None):
    corpo = {"sucesso": False, "mensagem": mensagem}
    if detalhes:
        corpo["detalhes"] = detalhes
    return jsonify(corpo), status
