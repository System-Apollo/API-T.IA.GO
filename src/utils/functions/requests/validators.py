import re

def validar_cpf(cpf):
    """Valida o CPF, verificando o formato e os dígitos verificadores."""
    cpf = str(cpf)  # Garantir que é string
    cpf = ''.join(filter(str.isdigit, cpf))  # Remove caracteres não numéricos
    if len(cpf) != 11 or cpf in [str(x) * 11 for x in range(10)]:
        return False

    # Validação dos dígitos verificadores
    for i in range(9, 11):
        soma = sum(int(cpf[num]) * peso for num, peso in enumerate(range(i + 1, 1, -1)))
        digito = (soma * 10 % 11) % 10
        if digito != int(cpf[i]):
            return False
    return True

def validar_cnpj(cnpj):
    """Valida o CNPJ, verificando o formato e os dígitos verificadores."""
    cnpj = str(cnpj)  # Garantir que é string
    cnpj = ''.join(filter(str.isdigit, cnpj))  # Remove caracteres não numéricos
    if len(cnpj) != 14:
        return False

    # Validação dos dígitos verificadores
    for i in range(12, 14):
        pesos = list(range(i - 7, 1, -1)) + list(range(9, 1, -1))
        soma = sum(int(cnpj[num]) * peso for num, peso in enumerate(pesos))
        digito = (soma * 10 % 11) % 10
        if digito != int(cnpj[i]):
            return False
    return True


def validar_email(email):
    """Valida o formato do e-mail."""
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None
