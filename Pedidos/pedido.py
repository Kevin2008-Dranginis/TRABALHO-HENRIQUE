from datetime import datetime, timedelta
from Cardapios.cardapio import Prato

class Pedido:
    TEMPO_ENTREGA = 20

    def __init__(self):
        self.itens = []

    def adicionar_item(self, item):
        self.itens.append(item)

    def calcular_total(self):
        # sum() soma automaticamente o preço de todos os itens,
        # evitando criar uma variável acumuladora e um laço.
        return sum(i.calcular_preco() for i in self.itens)

    def calcular_tempo_preparo(self):
        if not self.itens:
            return 0

        # Separa automaticamente os pratos usando isinstance(),
        # evitando vários ifs.
        pratos = [i for i in self.itens if isinstance(i, Prato)]

        # Separa automaticamente os demais itens.
        outros = [i for i in self.itens if not isinstance(i, Prato)]

        # max() encontra automaticamente o maior tempo de preparo.
        # default=0 evita erro caso não exista nenhum prato.
        tempo_pratos = max((p.tempo_preparo() for p in pratos), default=0)

        # sum() soma automaticamente o tempo dos outros itens.
        tempo_outros = sum(o.tempo_preparo() for o in outros)

        return tempo_pratos + tempo_outros

    def calcular_tempo_total(self):
        return self.calcular_tempo_preparo() + self.TEMPO_ENTREGA

    def obter_horarios(self):
        agora = datetime.now()
        tempo_preparo = self.calcular_tempo_preparo()

        # timedelta() adiciona minutos ao horário sem fazer cálculos manuais.
        horario_pronto = agora + timedelta(minutes=tempo_preparo)

        horario_entrega = horario_pronto + timedelta(minutes=self.TEMPO_ENTREGA)

        return {
            # strftime() formata a hora usando:
            # %H = hora, %M = minuto e %S = segundo.
            "atual": agora.strftime("%H:%M:%S"),
            "pronto": horario_pronto.strftime("%H:%M:%S"),
            "entrega": horario_entrega.strftime("%H:%M:%S")
        }
