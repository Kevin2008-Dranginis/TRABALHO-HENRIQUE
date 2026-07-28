from abc import ABC, abstractmethod

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

        # subclasses (pratos, bebidas, brindes)

class Pratos(ItemCardapio):
        def __init__(self, nome: str, preco_base: float, complexidade: str ="simples"):
            super().__init__(nome, preco_base)
            self.complexidade = complexidade.lower()

        def calcular_preco(self) -> float:
             if self.complexidade == "atrasado + desconto":
                  return max(0.0, self.preco_base - 5.0)  # R$5 de desconto para o cliente.
             return self.preco_base

        @abstractmethod
        def tempo_preparo(self) -> int:
                if self.complexidade == "simples":
                    return 15
                elif self.complexidade == "medio":
                    return 20
                elif self.complexidade == "complexo":
                    return 40
                elif self.complexidade == "atrasado + desconto ao cliente":
                    return 60  # R$5 de desconto para o cliente.

                else:
                    raise ValueError("Complexidade inválida. Use 'simples', 'medio', 'complexo' ou 'atrasado + desconto ao cliente'.")

# PRATOS - CARDÁPIO

cardapio_Pratos = {
    "1": Pratos("PF de Frango", 22.0, complexidade="simples"),
    "2": Pratos("Feijoada Completa", 45.0, complexidade="complexo"),
    "3": Pratos("MilaPurê com Atraso", 25.0, complexidade="atrasado + desconto"),
    "4": Pratos("Strogo Cruncy", 35.0, complexidade="medio"),
}

class Bebidas(ItemCardapio):
        def __init__(self, nome: str, preco_base: float, alcoolica: bool = False):
             super().__init__(nome, preco_base)
             self.alcoolica = alcoolica

        def calcular_preco(self) -> float:

            def tempo_preparo(self) -> int:
             return 2 

 # BEBIDAS - CARDÁPIO

cardapio_bebidas = {
      "1": Bebidas("Cerveja Heineken", 8.0, alcoolica=True),
      "2": Bebidas("Cerveja Brahma", 7.0, alcoolica=True),
      "3": Bebidas("Cerveja Skol", 6.0, alcoolica=True),
      "4": Bebidas("Vinho Rosé", 45.0, alcoolica=True),  
      "5": Bebidas("Vinho Suave", 25.0, alcoolica=True),
      "6": Bebidas("Vinho Seco", 20.0, alcoolica=True),
      "7": Bebidas("Água", 0.0, alcoolica=False),
      "8": Bebidas("Cola-Soda", 7.0, alcoolica=False),
      "9": Bebidas("Suco de Laranja Natural", 5.0, alcoolica=False),
 }       
