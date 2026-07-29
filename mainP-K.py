from abc import ABC, abstractmethod
from datetime import datetime, timedelta

# Nova classe Cliente adicionada para gerenciar os dados e a maioridade
class Cliente:
    def __init__(self, nome, cpf, data_nascimento):
        self.nome = nome
        self.cpf = cpf
        self.data_nascimento = data_nascimento  # Espera o formato dd/mm/aaaa

    def maior_de_idade(self):
        try:
            nasc = datetime.strptime(self.data_nascimento, "%d/%m/%Y")
            agora = datetime.now()
            # Calcula a idade exata comparando dia, mês e ano
            idade = agora.year - nasc.year - ((agora.month, agora.day) < (nasc.month, nasc.day))
            return idade >= 18
        except ValueError:
            # Caso a data seja digitada em formato inválido, considera menor por segurança
            return False

class ItemCardapio(ABC):
    def __init__(self, nome, preco_base):
        self.__nome = nome
        self.preco_base = preco_base

    @property
    def nome(self):
        return self.__nome

    @abstractmethod
    def calcular_preco(self):
        pass

    @abstractmethod
    def tempo_preparo(self):
        pass

class Prato(ItemCardapio):
    def __init__(self, nome, preco_base, complexidade="simples"):
        super().__init__(nome, preco_base)
        self.complexidade = complexidade.lower()

    def calcular_preco(self):
        if self.complexidade == "atrasado + desconto":
            return max(0, self.preco_base - 5)
        return self.preco_base

    def tempo_preparo(self):
        return {"simples": 15, "medio": 20, "complexo": 40, "atrasado + desconto": 60}.get(self.complexidade, 15)

class Bebida(ItemCardapio):
    def __init__(self, nome, preco_base, alcoolica=False):
        super().__init__(nome, preco_base)
        self.alcoolica = alcoolica

    def calcular_preco(self):
        return self.preco_base

    def tempo_preparo(self):
        return 0

class Sobremesa(ItemCardapio):
    def __init__(self, nome, preco_base):
        super().__init__(nome, preco_base)

    def calcular_preco(self):
        return self.preco_base

    def tempo_preparo(self):
        return 5

class Pedido:
    TEMPO_ENTREGA = 20

    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def calcular_total(self):
        return sum(i.calcular_preco() for i in self.itens)

    def calcular_tempo_preparo(self):
        if not self.itens:
            return 0
        pratos = [i for i in self.itens if isinstance(i, Prato)]
        outros = [i for i in self.itens if not isinstance(i, Prato)]
        tempo_pratos = max((p.tempo_preparo() for p in pratos), default=0)
        tempo_outros = sum(o.tempo_preparo() for o in outros)
        return tempo_pratos + tempo_outros

    def calcular_tempo_total(self):
        return self.calcular_tempo_preparo() + self.TEMPO_ENTREGA

    def obter_horarios(self):
        agora = datetime.now()
        tempo_preparo = self.calcular_tempo_preparo()
        horario_pronto = agora + timedelta(minutes=tempo_preparo)
        horario_entrega = horario_pronto + timedelta(minutes=self.TEMPO_ENTREGA)
        return {
            "atual": agora.strftime("%H:%M:%S"),
            "pronto": horario_pronto.strftime("%H:%M:%S"),
            "entrega": horario_entrega.strftime("%H:%M:%S")
        }

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

# 2. Assinatura alterada para receber o objeto cliente
def selecionar_categoria(categoria, dicionario, pedido, cliente, eh_bebida=False):
    itens_selecionados = []
    
    artigo = "a" if categoria.lower().endswith("a") else "o"
    plural = f"{categoria.lower()}s"

    while True:
        print(f"\n=== {categoria.upper()}S ===")
        for c, item in dicionario.items():
            if item.tempo_preparo() > 0:
                print(f"{c} - {item.nome} - R${item.calcular_preco():.2f} (Preparo: {item.tempo_preparo()} min)")
            else:
                print(f"{c} - {item.nome} - R${item.calcular_preco():.2f}")
        
        for idx, item in enumerate(itens_selecionados, start=1):
            print(f"{categoria} {idx} ja selecionado: {item.nome}")

        e = input(f"Ensira as opções de {plural} (0 para proximo/sair): ").strip().lower()
        if e == "0":
            break

        if e in dicionario:
            item = dicionario[e]
            
            # 3. Verificação de bebida alcoólica utilizando o método do Cliente
            if eh_bebida and item.alcoolica:
                if not cliente.maior_de_idade():
                    print("Venda proibida para menores de 18 anos.")
                    continue

            pedido.adicionar_item(item)
            itens_selecionados.append(item)
            print(f"{categoria} {len(itens_selecionados)} selecionado com sucesso!")
            
            resp = input(f"Deseja finalizar, adicionar + {plural} ou cancelar ultim{artigo} {categoria.lower()}? (f = finalizar / a = adicionar mais / c = cancelar ultim{artigo} {categoria.lower()}): ").strip().lower()

            if resp == "f":
                return
            elif resp == "a":
                continue
            elif resp == "c":
                if itens_selecionados:
                    ultimo = itens_selecionados.pop()
                    if ultimo in pedido.itens:
                        pedido.itens.remove(ultimo)
                    print(f"Ultim{artigo} {categoria.lower()} cancelad{artigo} com sucesso!")
                continue
            else:
                while True:
                    erro_resp = input("error 01 - use 0 para recomeçar: ").strip().lower()
                    if erro_resp == "0":
                        for it in itens_selecionados:
                            if it in pedido.itens:
                                pedido.itens.remove(it)
                        itens_selecionados.clear()
                        print("Selecao reiniciada.")
                        break
                continue
        else:
            print("Codigo invalido.")

while True:
    print("\nBEM VINDO AO RESTAURANTE DA ESQUINA !")
    while True:
        inicio = input("PRESSIONE 01: ").strip()
        if inicio == "01":
            break

    # 4. Inserção do cadastro do cliente antes da criação do pedido
    print("\n===== CADASTRO DO CLIENTE =====")
    nome = input("Nome: ")
    cpf = input("CPF: ")
    nascimento = input("Data de nascimento (dd/mm/aaaa): ")
    cliente = Cliente(nome, cpf, nascimento)

    pedido = Pedido()

    # 5. Passagem do parâmetro 'cliente' em todas as chamadas da função
    selecionar_categoria("Prato", pratos, pedido, cliente)
    selecionar_categoria("Bebida", bebidas, pedido, cliente, eh_bebida=True)
    selecionar_categoria("Sobremesa", sobremesas, pedido, cliente)

    qtd_pratos = sum(isinstance(i, Prato) for i in pedido.itens)
    if qtd_pratos >= 3:
        print("\nParabens! Voce ganhou direito a um brinde!")
        selecionar_categoria("Brinde", brindes, pedido, cliente)

    horarios = pedido.obter_horarios()

    print("\n===== RESUMO =====")
    print(f"Cliente: {cliente.nome} | CPF: {cliente.cpf}")
    for i in pedido.itens:
        print(f"{i.nome} - R${i.calcular_preco():.2f}")

    print(f"\nTotal: R${pedido.calcular_total():.2f}")
    print(f"Horario do pedido (agora): {horarios['atual']}")
    print(f"Tempo de preparo: {pedido.calcular_tempo_preparo()} min (Pronto as {horarios['pronto']})")
    print(f"Tempo de entrega: {pedido.TEMPO_ENTREGA} min")
    print(f"Tempo total estimado: {pedido.calcular_tempo_total()} min")
    print(f"Estimativa de horario de entrega final: {horarios['entrega']}")

    print("\n===== CONFIRMAÇÃO DO PEDIDO =====")
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
