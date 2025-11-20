# =============================================================================
# SISTEMA DE MENSAGENS FLASH
# =============================================================================
# Mensagens flash são mensagens temporárias exibidas uma única vez ao usuário.
# São úteis para feedback de ações como "Login realizado com sucesso!".

from fastapi import Request
from typing import Optional


def adicionar_mensagem(request: Request, tipo: str, texto: str):
    """
    Adiciona uma mensagem flash à sessão.

    Args:
        request: Objeto Request do FastAPI
        tipo: Tipo da mensagem (success, danger, warning, info)
        texto: Texto da mensagem
    """
    if "flash_messages" not in request.session:
        request.session["flash_messages"] = []
    request.session["flash_messages"].append({"tipo": tipo, "texto": texto})


def informar_sucesso(request: Request, texto: str):
    adicionar_mensagem(request, "success", texto)


def informar_erro(request: Request, texto: str):
    adicionar_mensagem(request, "danger", texto)


def obter_mensagens(request: Request) -> list:
    mensagens = request.session.get("flash_messages", [])
    request.session["flash_messages"] = []
    return mensagens
