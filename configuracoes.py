class Configuracoes:
    _saldoMinimo = 1300
    _assertividadeMinima = 78.32
    _valorAposta = 5
    _intervaloGreens = 3
    _maxVitoriasSeguidas = 3

    def getSaldoMinimo(self):
        return self._saldoMinimo

    def getAssertividadeMinima(self):
        return self._assertividadeMinima

    def getValorAposta(self):
        return self._valorAposta

    def getValorPrimeiroGale(self):
        return self.getValorAposta() * 2

    def getValorSegundoGale(self):
        return self.getValorPrimeiroGale() * 2

    def getIntervaloGreens(self):
        return self._intervaloGreens

    def getMaxVitoriasSeguidas(self):
        return self._maxVitoriasSeguidas