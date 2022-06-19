from datetime import datetime


class Aposta:
    corResultado: str

    def __init__(self, valor: float, cor: str, gale: str):
        self.valor = valor
        self.cor = cor
        self.hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.ganhou = False
        self.eGale = gale
        self.podeApostar = False

    def getResult(self):
        result = "PERDEU"
        if self.ganhou:
            result = "GANHOU"
        return result