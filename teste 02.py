
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
    def __init__(self,nome,preco_base,complexidade="simples"):
        super().__init__(nome,preco_base)
        self.complexidade=complexidade.lower()
    def calcular_preco(self):
        if self.complexidade=="atrasado + desconto":
            return max(0,self.preco_base-5)
        return self.preco_base
    def tempo_preparo(self):
        return {"simples":15,"medio":20,"complexo":40,"atrasado + desconto":60}.get(self.complexidade,15)

class Bebida(ItemCardapio):
    def __init__(self,nome,preco_base,alcoolica=False):
        super().__init__(nome,preco_base)
        self.alcoolica=alcoolica
    def calcular_preco(self):
        return self.preco_base
    def tempo_preparo(self):
        return 2

class Sobremesa(ItemCardapio):
    def calcular_preco(self):
        return self.preco_base
    def tempo_preparo(self):
        return 5

class Pedido:
    def __init__(self):
        self.itens=[]
    def adicionar_item(self,item):
        self.itens.append(item)
    def calcular_total(self):
        return sum(i.calcular_preco() for i in self.itens)
    def calcular_tempo(self):
        return sum(i.tempo_preparo() for i in self.itens)

pratos={
"1":Prato("PF de Frango",22,"simples"),
"2":Prato("Feijoada Completa",45,"complexo"),
"3":Prato("MilaPur锚 com Atraso",25,"atrasado + desconto"),
"4":Prato("Strogonoff Crunchy",35,"medio")
}

bebidas={
"1":Bebida("Cerveja Heineken",8,True),
"2":Bebida("Cerveja Brahma",7,True),
"3":Bebida("Água",3),
"4":Bebida("Refrigerante",7)
}

sobremesas={
"1":Sobremesa("Pudim",12),
"2":Sobremesa("Brownie de Chocolate",15),
"3":Sobremesa("Petit Gateau",18)
}

brindes={
"1":Sobremesa("Musse de Maracuj谩",0),
"2":Sobremesa("Bolo de Pote",0),
"3":Sobremesa("Barra de Chocolate (Diamante)",0)
}

pedido=Pedido()

print("=== PRATOS ===")
while True:
    for c,p in pratos.items():
        print(f"{c} - {p.nome} - R${p.calcular_preco():.2f}")
    e=input("C贸digo (0 sair): ")
    if e=="0":
        break
    if e in pratos:
        pedido.adicionar_item(pratos[e])
    else:
        print("C贸digo inv谩lido")

print("\n=== BEBIDAS ===")
while True:
    for c,b in bebidas.items():
        print(f"{c} - {b.nome} - R${b.calcular_preco():.2f}")
    e=input("C贸digo (0 sair): ")
    if e=="0":
        break
    if e in bebidas:
        b=bebidas[e]
        if b.alcoolica:
            idade=int(input("Confirme sua idade: "))
            if idade<18:
                print("Venda proibida.")
                continue
        pedido.adicionar_item(b)
    else:
        print("C贸digo inv谩lido")

print("\n=== SOBREMESAS ===")
while True:
    for c,s in sobremesas.items():
        print(f"{c} - {s.nome} - R${s.calcular_preco():.2f}")
    e=input("C贸digo (0 sair): ")
    if e=="0":
        break
    if e in sobremesas:
        pedido.adicionar_item(sobremesas[e])

qtd=sum(isinstance(i,Prato) for i in pedido.itens)
if qtd>=3:
    print("\nParab茅ns! Escolha um brinde:")
    for c,b in brindes.items():
        print(f"{c} - {b.nome}")
    e=input("Brinde: ")
    if e in brindes:
        pedido.adicionar_item(brindes[e])

print("\n===== RESUMO =====")
for i in pedido.itens:
    print(f"{i.nome} - R${i.calcular_preco():.2f}")
print(f"Total: R${pedido.calcular_total():.2f}")
print(f"Tempo estimado: {pedido.calcular_tempo()} minutos")
