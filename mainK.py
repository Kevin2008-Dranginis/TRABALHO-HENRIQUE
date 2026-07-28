from abc import ABC, abstractmethod

class ItemCardapio(ABC):
    def __init__(self, prato1, prato2, prato3, prato4, prato5, prato6):
        self._prato1 = prato1
        self._prato2 = prato2
        self._prato3 = prato3
        self._prato4 = prato4
        self._prato5 = prato5
        self._prato6 = prato6

    @property
    def prato1(self):
        return self._prato1

    @property
    def prato2(self):
        return self._prato2

    @property
    def prato3(self):
        return self._prato3

    @property
    def prato4(self):
        return self._prato4

    @property
    def prato5(self):
        return self._prato5

    @property
    def prato6(self):
        return self._prato6

    @abstractmethod
    def tempo_preparo(self):
        pass

    
    @abstractmethod
    def calcular_preco(self):
        pass

        dw