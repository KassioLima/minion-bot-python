import csv
from datetime import datetime
from aposta import Aposta


class LogJogadas:

    def __init__(self):
        self.logFileName = "logs/log_" + datetime.now().strftime('%d-%m-%Y_%H-%M-%S') + ".csv"
        with open(self.logFileName, "w") as log:
            csv.writer(log, delimiter=",").writerow(
                [
                    "Valor",
                    "Cor",
                    "Data e hora",
                    "Gale",
                    "Cor Sorteada",
                    "Resultado",
                    "Saldo Resultante",
                    "Assertividade Atual",
                    "Jogou",
                ])

    def saveLog(self, saldoAtual: float, assertividadeAtual: float, aposta: Aposta):
        with open(self.logFileName, "a") as log:
            csv.writer(log, delimiter=",").writerow(
                [
                    str(aposta.valor).replace(".", ","),
                    aposta.cor,
                    aposta.hora,
                    aposta.eGale,
                    aposta.corResultado,
                    aposta.getResult(),
                    str(saldoAtual).replace(".", ","),
                    str(round(assertividadeAtual, 2)).replace(".", ",") + "%",
                    str(aposta.podeApostar),
                ])
