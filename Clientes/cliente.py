from datetime import datetime

class Cliente:
    def __init__(self, nome, cpf, data_nascimento, dia_nasc, mes_nasc, ano_nasc):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento
        self.dia_nasc = dia_nasc
        self.mes_nasc = mes_nasc
        self.ano_nasc = ano_nasc

    def maior_de_idade(self):
        agora = datetime.now()
        idade = agora.year - self.ano_nasc
        if (agora.month, agora.day) < (self.mes_nasc, self.dia_nasc):
            idade -= 1
        return idade >= 18


def formatar_e_validar_cpf(entrada_cpf):
    """
    Remove pontuações, valida se possui 11 dígitos e aplica a máscara XXX.XXX.XXX-XX.
    """
    numeros = "".join(c for c in entrada_cpf if c.isdigit())

    if len(numeros) != 11:
        return None, "Erro: O CPF deve conter exatamente 11 dígitos."

    if numeros == numeros[0] * 11:
        return None, "Erro: Digite um CPF válido."

    cpf_formatado = f"{numeros[:3]}.{numeros[3:6]}.{numeros[6:9]}-{numeros[9:]}"
    return cpf_formatado, None


def formatar_e_validar_data(entrada_data):
    """
    Valida dia/mês/ano e formata automaticamente para DD/MM/AAAA.
    """
    numeros = "".join(c for c in entrada_data if c.isdigit())

    if len(numeros) != 8:
        return None, "Erro: A data deve conter 8 dígitos (Exemplo: 06102007 ou 06/10/2007)."

    dia = int(numeros[:2])
    mes = int(numeros[2:4])
    ano = int(numeros[4:])

    if mes < 1 or mes > 12:
        return None, "Erro: Mês inválido. Deve ser de 01 a 12."

    dias_no_mes = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    # Ajuste para ano bissexto
    if (ano % 4 == 0 and ano % 100 != 0) or (ano % 400 == 0):
        dias_no_mes[2] = 29

    if dia < 1 or dia > dias_no_mes[mes]:
        return None, f"Erro: O mês {mes:02d} possui no máximo {dias_no_mes[mes]} dias em {ano}."

    agora_ano = datetime.now().year
    if ano < 1900 or ano > agora_ano:
        return None, "Erro: Ano de nascimento inválido."

    data_formatada = f"{dia:02d}/{mes:02d}/{ano}"
    return (data_formatada, dia, mes, ano), None


def carregar_cpfs_salvos():
    """Lê o arquivo clientes.txt e recupera os CPFs cadastrados anteriormente."""
    try:
        with open("clientes.txt", "r", encoding="utf-8") as arquivo:
            return set(linha.strip() for linha in arquivo if linha.strip())
    except FileNotFoundError:
        return set()


def salvar_cpf_no_arquivo(cpf):
    """Escreve um novo CPF no arquivo clientes.txt."""
    with open("clientes.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{cpf}\n")