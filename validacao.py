import re

from email_validator import EmailNotValidError, validate_email

NOME_VALIDO = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ][A-Za-zÀ-ÖØ-öø-ÿ' .-]*")
SENHA_MIN = 12
SENHA_MAX = 128
PALAVRAS_FRACAS = ("senha", "password", "admin", "qwerty", "123456", "abcdef", "letmein")


def checar_senha(senha, email=""):
    """Devolve uma mensagem de erro, ou None se a senha for aceitável."""
    if len(senha) < SENHA_MIN:
        return f"A senha precisa ter pelo menos {SENHA_MIN} caracteres."
    if len(senha) > SENHA_MAX:
        return f"A senha pode ter no máximo {SENHA_MAX} caracteres."

    minuscula = senha.lower()
    if senha.isdigit():
        return "A senha não pode ter só números. Misture letras ou use uma frase longa."
    if len(set(senha)) <= 3:
        return "A senha tem poucos caracteres diferentes. Use algo menos repetitivo."
    if any(palavra in minuscula for palavra in PALAVRAS_FRACAS):
        return "A senha contém uma sequência ou palavra muito comum. Escolha outra."

    parte_inicial = email.split("@")[0].lower()
    if len(parte_inicial) >= 4 and parte_inicial in minuscula:
        return "A senha não pode conter a parte inicial do seu e-mail."
    return None


def validar_cadastro(formulario):
    """Valida os dados do cadastro. Devolve (dados_limpos, erros)."""
    nome = formulario.get("nome", "").strip()
    email = formulario.get("email", "").strip()
    senha = formulario.get("senha", "")
    confirmacao = formulario.get("confirmacao", "")
    erros = {}

    # Nome
    if not 2 <= len(nome) <= 80:
        erros["nome"] = "Informe seu nome, com 2 a 80 caracteres."
    elif not NOME_VALIDO.fullmatch(nome):
        erros["nome"] = "Use apenas letras, espaços, hífen e apóstrofo."

    # E-mail (formato; não confirma que a caixa existe)
    try:
        email = validate_email(email, check_deliverability=False).normalized.lower()
    except EmailNotValidError:
        erros["email"] = "Informe um e-mail válido, como nome@exemplo.com."

    # Senha
    erro_senha = checar_senha(senha, "" if "email" in erros else email)
    if erro_senha:
        erros["senha"] = erro_senha
    elif senha != confirmacao:
        erros["confirmacao"] = "As senhas não são iguais."

    dados = {"nome": nome, "email": email, "senha": senha}
    return dados, erros


def validar_troca_senha(formulario, email):
    """Valida o formulário de troca de senha. Devolve (senha_atual, senha_nova, erros)."""
    atual = formulario.get("senha_atual", "")
    nova = formulario.get("senha_nova", "")
    confirmacao = formulario.get("confirmacao", "")
    erros = {}

    if not atual:
        erros["senha_atual"] = "Informe sua senha atual."

    erro_senha = checar_senha(nova, email)
    if erro_senha:
        erros["senha_nova"] = erro_senha
    elif atual and nova == atual:
        erros["senha_nova"] = "A nova senha precisa ser diferente da atual."
    elif nova != confirmacao:
        erros["confirmacao"] = "As senhas não são iguais."

    return atual, nova, erros