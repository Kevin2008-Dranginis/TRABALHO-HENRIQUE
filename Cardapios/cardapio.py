from abc import ABC, abstractmethod

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