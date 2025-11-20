# =============================================================================
# UTILITÁRIOS DE SEGURANÇA
# =============================================================================
# Este módulo fornece funções para hash e verificação de senhas usando bcrypt.
# Bcrypt é um algoritmo seguro que inclui salt automaticamente.

from passlib.context import CryptContext

# Contexto para hash de senhas com bcrypt
# "deprecated=auto" marca esquemas antigos como obsoletos automaticamente
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def criar_hash_senha(senha: str) -> str:
    """
    Cria hash seguro da senha usando bcrypt.

    Args:
        senha: Senha em texto plano

    Returns:
        Hash da senha (inclui salt automaticamente)
    """
    return pwd_context.hash(senha)


def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """
    Verifica se a senha corresponde ao hash armazenado.

    Args:
        senha_plana: Senha digitada pelo usuário
        senha_hash: Hash armazenado no banco de dados

    Returns:
        True se a senha estiver correta, False caso contrário
    """
    return pwd_context.verify(senha_plana, senha_hash)
