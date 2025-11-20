# =============================================================================
# DECORATOR E FUNÇÕES DE AUTENTICAÇÃO
# =============================================================================
# Este módulo fornece funções para gerenciar sessões de usuário e um decorator
# para proteger rotas que exigem autenticação.

from fastapi import Request, status
from fastapi.responses import RedirectResponse
from functools import wraps
from typing import Optional


def criar_sessao(request: Request, usuario: dict):
    """
    Cria sessão de usuário após login bem-sucedido.

    Args:
        request: Objeto Request do FastAPI
        usuario: Dicionário com dados do usuário (id, nome, email)
    """
    request.session["usuario_logado"] = usuario


def destruir_sessao(request: Request):
    """
    Destrói a sessão do usuário (logout).
    Remove todos os dados da sessão.

    Args:
        request: Objeto Request do FastAPI
    """
    request.session.clear()


def obter_usuario_logado(request: Request) -> Optional[dict]:
    """
    Obtém dados do usuário logado da sessão.

    Args:
        request: Objeto Request do FastAPI

    Returns:
        Dicionário com dados do usuário ou None se não estiver logado
    """
    return request.session.get("usuario_logado")


def esta_logado(request: Request) -> bool:
    """
    Verifica se há um usuário logado na sessão.

    Args:
        request: Objeto Request do FastAPI

    Returns:
        True se há usuário logado, False caso contrário
    """
    return "usuario_logado" in request.session


def requer_autenticacao():
    """
    Decorator para proteger rotas que exigem autenticação.

    Se o usuário não estiver logado, redireciona para /login.
    Se estiver logado, injeta o usuario_logado nos kwargs da função.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Obtém o request dos argumentos
            request = kwargs.get('request') or args[0]

            # Verifica se está logado
            usuario = obter_usuario_logado(request)
            if not usuario:
                # Redireciona para login mantendo a URL original
                return RedirectResponse(
                    f"/login?redirect={request.url.path}",
                    status_code=status.HTTP_303_SEE_OTHER
                )

            # Injeta usuario_logado nos kwargs para uso na função
            kwargs['usuario_logado'] = usuario
            return await func(*args, **kwargs)

        return wrapper
    return decorator
