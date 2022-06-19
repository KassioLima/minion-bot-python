class TelegramBot:
    _assertividadeAtual = 0
    apostas = list()

    def getAssertividadeAtual(self):
        return self._assertividadeAtual

    def setAssertividadeAtual(self, ultima_mensagem: str):
        valores = ultima_mensagem.split("\n\n")[0].split(" = ")
        acertos = int(valores[1]) - int(valores[3])
        jogadasTotais = int(valores[1]) + int(valores[2])

        self._assertividadeAtual = (acertos / jogadasTotais) * 100