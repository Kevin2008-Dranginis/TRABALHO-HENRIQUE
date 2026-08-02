import sys
import os

# Adiciona a pasta principal do projeto ao caminho de busca do Python,
# permitindo importar arquivos de outras pastas.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Agora seus imports vão funcionar normalmente:
from Clientes.cliente import (
    Cliente,
    formatar_e_validar_cpf,
    formatar_e_validar_data,
    carregar_cpfs_salvos,
    salvar_cpf_no_arquivo
)
from Cardapios.cardapio import Prato, Bebida, Sobremesa
from Pedidos.pedido import Pedido

# Dicionários com os itens disponíveis no restaurante.
# Eles permitem buscar os itens pelo código, evitando vários if/elif.
pratos = {
    "1": Prato("PF de Frango", 22, "simples"),
    "2": Prato("Feijoada Completa", 45, "complexo"),
    "3": Prato("MilaPura com Atraso", 25, "atrasado + desconto"),
    "4": Prato("Strogonoff Crunchy", 35, "medio")
}

bebidas = {
    "1": Bebida("Cerveja Heineken", 8.0, alcoolica=True),
    "2": Bebida("Cerveja Brahma", 7.0, alcoolica=True),
    "3": Bebida("Cerveja Skol", 6.0, alcoolica=True),
    "4": Bebida("Vinho Rosé", 45.0, alcoolica=True),
    "5": Bebida("Vinho Suave", 25.0, alcoolica=True),
    "6": Bebida("Vinho Seco", 20.0, alcoolica=True),
    "7": Bebida("Água", 0.0, alcoolica=False),
    "8": Bebida("Cola-Soda", 7.0, alcoolica=False),
    "9": Bebida("Suco de Laranja Natural", 5.0, alcoolica=False)
}

sobremesas = {
    "1": Sobremesa("Pudim", 12),
    "2": Sobremesa("Brownie de Chocolate", 15),
    "3": Sobremesa("Petit Gateau", 18)
}

brindes = {
    "1": Sobremesa("Musse de Maracuja", 0),
    "2": Sobremesa("Bolo de Pote", 0),
    "3": Sobremesa("Barra de Chocolate (Diamante)", 0)
}

def selecionar_categoria(categoria, dicionario, pedido, cliente, eh_bebida=False):
    itens_selecionados = []

    # lower() converte para minúsculas para facilitar a comparação.
    artigo = "a" if categoria.lower().endswith("a") else "o"

    # Cria automaticamente o plural da categoria.
    plural = f"{categoria.lower()}s"

    while True:
        print(f"\n=== {categoria.upper()}S ===")

        # items() percorre automaticamente todos os itens do dicionário.
        for c, item in dicionario.items():
            if item.tempo_preparo() > 0:
                print(f"{c} - {item.nome} - R${item.calcular_preco():.2f} (Preparo: {item.tempo_preparo()} min)")
            else:
                print(f"{c} - {item.nome} - R${item.calcular_preco():.2f}")

        # enumerate() numera automaticamente os itens selecionados.
        for idx, item in enumerate(itens_selecionados, start=1):
            print(f"{categoria} {idx} ja selecionado: {item.nome}")

        # strip() remove espaços e lower() aceita letras maiúsculas e minúsculas.
        e = input(f"Insira as opções de {plural} (0 para proximo/sair): ").strip().lower()

        if e == "0":
            break

        if e in dicionario:

            # Busca diretamente o item pelo código, evitando vários if/elif.
            item = dicionario[e]

            # Verificação de maioridade para bebidas alcoólicas.
            if eh_bebida and item.alcoolica:
                if not cliente.maior_de_idade():
                    print("Venda proibida para menores de 18 anos.")
                    continue

            pedido.adicionar_item(item)
            itens_selecionados.append(item)
            print(f"{categoria} {len(itens_selecionados)} selecionado com sucesso!")

            # strip() remove espaços e lower() aceita F/f, A/a e C/c.
            resp = input(f"Deseja finalizar, adicionar + {plural} ou cancelar ultim{artigo} {categoria.lower()}? (f = finalizar / a = adicionar mais / c = cancelar ultim{artigo} {categoria.lower()}): ").strip().lower()

            if resp == "f":
                return
            elif resp == "a":
                continue
            elif resp == "c":
                if itens_selecionados:

                    # pop() remove automaticamente o último item da lista.
                    ultimo = itens_selecionados.pop()

                    if ultimo in pedido.itens:
                        pedido.itens.remove(ultimo)

                    print(f"Ultim{artigo} {categoria.lower()} cancelad{artigo} com sucesso!")

                continue
            else:
                while True:

                    # strip() remove espaços e lower() aceita letras maiúsculas e minúsculas.
                    erro_resp = input("error 01 - use 0 para recomeçar: ").strip().lower()

                    if erro_resp == "0":

                        # Percorre todos os itens da lista para removê-los.
                        for it in itens_selecionados:
                            if it in pedido.itens:
                                pedido.itens.remove(it)

                        itens_selecionados.clear()

                        print("Selecao reiniciada.")
                        break

                continue
        else:
            print("Codigo invalido.")

# Carrega os CPFs já cadastrados para evitar cadastros duplicados.
cpfs_cadastrados = carregar_cpfs_salvos()

# Loop Principal da Aplicação.
while True:
    print("\nBEM VINDO AO RESTAURANTE DA ESQUINA !")

    while True:
        # strip() remove espaços caso o usuário digite " 01 ".
        inicio = input("PRESSIONE 01: ").strip()

        if inicio == "01":
            break

    print("\n===== CADASTRO DO CLIENTE =====")

    # strip() remove espaços antes e depois do nome digitado.
    nome = input("Nome: ").strip()

    # Validação, máscara automática e verificação de CPF já cadastrado.
    while True:
        cpf_input = input("CPF (digite apenas os números ou com pontos): ")

        cpf_valido, erro_cpf = formatar_e_validar_cpf(cpf_input)

        if cpf_valido:

            # Como cpfs_cadastrados é um set, a busca por CPF é rápida
            # e evita cadastros repetidos.
            if cpf_valido in cpfs_cadastrados:
                print("Erro: Este CPF já possui cadastro no sistema!")
                continue

            # Salva o CPF no conjunto e também no arquivo.
            cpfs_cadastrados.add(cpf_valido)
            salvar_cpf_no_arquivo(cpf_valido)

            print(f"CPF registrado com sucesso: {cpf_valido}")
            break

        print(erro_cpf)

    # Validação e máscara automática da data de nascimento.
    while True:
        data_input = input("Data de nascimento (ex: 06102007 ou 06/10/2007): ")

        dados_data, erro_data = formatar_e_validar_data(data_input)

        if dados_data:
            data_formatada, dia, mes, ano = dados_data

            print(f"Data registrada: {data_formatada}")
            break

        print(erro_data)

    cliente = Cliente(nome, cpf_valido, data_formatada, dia, mes, ano)

    pedido = Pedido()

    selecionar_categoria("Prato", pratos, pedido, cliente)
    selecionar_categoria("Bebida", bebidas, pedido, cliente, eh_bebida=True)
    selecionar_categoria("Sobremesa", sobremesas, pedido, cliente)

    # isinstance() verifica quais itens são objetos da classe Prato.
    # sum() soma automaticamente a quantidade desses pratos.
    qtd_pratos = sum(isinstance(i, Prato) for i in pedido.itens)

    if qtd_pratos >= 3:
        print("\nParabens! Voce ganhou direito a um brinde!")
        selecionar_categoria("Brinde", brindes, pedido, cliente)

    # Chama apenas uma função para obter todos os horários do pedido.
    horarios = pedido.obter_horarios()

    print("\n===== RESUMO =====")
    print(f"Cliente: {cliente.nome} | CPF: {cliente.cpf}")

    # Percorre automaticamente todos os itens do pedido.
    for i in pedido.itens:
        print(f"{i.nome} - R${i.calcular_preco():.2f}")

    print(f"\nTotal: R${pedido.calcular_total():.2f}")
    print(f"Horario do pedido (agora): {horarios['atual']}")
    print(f"Tempo de preparo: {pedido.calcular_tempo_preparo()} min (Pronto as {horarios['pronto']})")
    print(f"Tempo de entrega: {pedido.TEMPO_ENTREGA} min")
    print(f"Tempo total estimado: {pedido.calcular_tempo_total()} min")
    print(f"Estimativa de horario de entrega final: {horarios['entrega']}")

    print("\n===== CONFIRMAÇÃO DO PEDIDO =====")

    # strip() remove espaços e lower() aceita C/c ou R/r.
    confirmacao = input("Deseja confirmar a compra e pedido? (c = confirmar / r = cancelar e reiniciar): ").strip().lower()

    if confirmacao == "c":
        print("Pedido confirmado com sucesso!")
        break

    elif confirmacao == "r":
        print("Pedido cancelado. Reiniciando o sistema...\n")
        continue

    else:
        print("Opcao invalida. Reiniciando o sistema...\n")
        continue
