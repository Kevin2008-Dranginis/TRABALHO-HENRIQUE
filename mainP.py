from abc import ABC, abstractmethod

# ==========================================
# 1. CLASSE ABSTRATA BASE
# ==========================================
class ItemCardapio(ABC):
    def __init__(self, nome: str, preco_base: float):
        self.__nome = nome
        self.preco_base = preco_base

    @property
    def nome(self):
        return self.__nome

    @abstractmethod
    def calcular_preco(self) -> float:
        pass

    @abstractmethod
    def tempo_preparo(self) -> int:
        pass


# ==========================================
# 2. SUBCLASSES (PRATOS E BEBIDAS)
# ==========================================
class Pratos(ItemCardapio):
    def __init__(self, nome: str, preco_base: float, complexidade: str = "simples"):
        super().__init__(nome, preco_base)
        self.complexidade = complexidade.lower()

    def calcular_preco(self) -> float:
        if self.complexidade == "atrasado + desconto":
            return max(0.0, self.preco_base - 5.0)
        return self.preco_base

    def tempo_preparo(self) -> int:
        if self.complexidade == "simples":
            return 15
        elif self.complexidade == "medio":
            return 20
        elif self.complexidade == "complexo":
            return 40
        elif self.complexidade == "atrasado + desconto":
            return 60
        else:
            raise ValueError("Complexidade inválida.")


class Bebidas(ItemCardapio):
    def __init__(self, nome: str, preco_base: float, alcoolica: bool = False):
        super().__init__(nome, preco_base)
        self.alcoolica = alcoolica

    def calcular_preco(self) -> float:
        return self.preco_base

    def tempo_preparo(self) -> int:
        return 2


# PRATOS - CARDÁPIO

cardapio_Pratos = {
    "1": Pratos("PF de Frango", 22.0, complexidade="simples"),
    "2": Pratos("Feijoada Completa", 45.0, complexidade="complexo"),
    "3": Pratos("MilaPurê com Atraso", 25.0, complexidade="atrasado + desconto"),
    "4": Pratos("Strogo Cruncy", 35.0, complexidade="medio"),
}

# BEBIDAS - CARDÁPIO

cardapio_Bebidas = {
    "1": Bebidas("Cerveja Heineken", 8.0, alcoolica=True),
    "2": Bebidas("Cerveja Brahma", 7.0, alcoolica=True),
    "3": Bebidas("Cerveja Skol", 6.0, alcoolica=True),
    "4": Bebidas("Vinho Rosé", 45.0, alcoolica=True),
    "5": Bebidas("Vinho Suave", 25.0, alcoolica=True),
    "6": Bebidas("Vinho Seco", 20.0, alcoolica=True),
    "7": Bebidas("Água", 3.0, alcoolica=False),
    "8": Bebidas("Cola-Soda", 7.0, alcoolica=False),
    "9": Bebidas("Suco de Laranja Natural", 5.0, alcoolica=False),
}

# EXECUÇÕES DE PEDIDOS

pedido_Pratos = []

print(" PRATOS - CARDÁPIO")

while True:
    print("\nPRATOS - CARDÁPIO:")
    for codigo, prato in cardapio_Pratos.items():
        print(f"{codigo} - {prato.nome} - R${prato.calcular_preco():.2f}")

    escolha = input("Digite o código do prato que deseja adicionar: ")

    if escolha in cardapio_Pratos:
        prato_selecionado = cardapio_Pratos[escolha]
        pedido_pratos.append(prato_selecionado)
        print(f" {prato_selecionado.nome} foi adicionado ao pedido!")
    else:
        print(" error no code")

    resposta = input("Deseja adicionar mais algum prato? (s/n): ")
    if resposta.lower() != "s":
        break

print(" CARDÁPIO - BEBIDAS ")

for codigo, bebida in cardapio_Bebidas.items():
    print(f"{codigo} - {bebida.nome} - R${bebida.calcular_preco():.2f}")

    escolha_bebida = input("\nDigite o número da bebida: ")
    bebida_selecionada = None

    if escolha_bebida in cardapio_Bebidas:
        bebida_temp = cardapio_Bebidas[escolha_bebida]
    if bebida_temp.alcoolica:
        idade = int(input("Esta bebida é alcoólica. Informe sua idade: "))
    if idade >= 18:
            bebida_selecionada = bebida_temp
            print(f" {bebida_selecionada.nome} adicionada ao pedido.")
        else:
            print(" Venda proibida para menores de 18 anos. Bebida não adicionada.")

    else:
        bebida_selecionada = bebida_temp
        print(f"✅ {bebida_selecionada.nome} adicionada ao pedido.") 
else:
    print("Opção de bebida inválida.")
