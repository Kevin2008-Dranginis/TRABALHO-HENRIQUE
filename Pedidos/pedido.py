from datetime import datetime, timedelta
from Cardapios.cardapio import Prato

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