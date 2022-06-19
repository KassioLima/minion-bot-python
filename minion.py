import time
from selenium.webdriver.opera.webdriver import WebDriver
from aposta import Aposta
from blaze import Blaze
from configuracoes import Configuracoes
from log_jogadas import LogJogadas
from telegram import Telegram
from telegram_bot import TelegramBot


class Minion:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.configuracoes = Configuracoes()
        self.log = LogJogadas()
        self.blaze = Blaze(driver)
        self.telegramBot = TelegramBot()
        self.telegram = Telegram(driver, self.blaze.getWindowHandle())
        self.start()

    def start(self):
        for second in range(60):
            print("Comecando em " + str(60 - second))
            time.sleep(1)
        print("\nMinion iniciado com sucesso!\n")

        self.leChatDoBot()

    def leChatDoBot(self):
        textoMensagens = list()
        descartarAposta = True

        while True:
            try:
                self.driver.switch_to.window(self.telegram.getWindowHandle())
                mensagens = self.telegram.getAllMessageElements()
                ultima_mensagem = mensagens[len(mensagens) - 1]
                textoUltimaMensagem = str(self.driver.execute_script("return arguments[0].innerHTML", ultima_mensagem))

                if "Parcial" in ultima_mensagem.text:
                    self.telegramBot.setAssertividadeAtual(ultima_mensagem.text)

                if "Aposte no" in textoUltimaMensagem and textoUltimaMensagem not in textoMensagens:
                    textoMensagens.append(textoUltimaMensagem)
                    if descartarAposta and not self.telegramBot.getAssertividadeAtual():
                        descartarAposta = False
                        print("Aposta descartada")
                        continue

                    if "26ab.png" in textoUltimaMensagem:
                        self.apostar("black", self.configuracoes.getValorAposta())
                    elif "1f534.png" in textoUltimaMensagem:
                        self.apostar("red", self.configuracoes.getValorAposta())
                    else:
                        print(str(self.driver.execute_script("return arguments[0].innerHTML", ultima_mensagem)))
                        break
                else:
                    if "VAMOS PARA O 1" in textoUltimaMensagem and len(self.telegramBot.apostas) >= 1:
                        if self.telegramBot.apostas[len(self.telegramBot.apostas) - 1].eGale != "1o GALE":
                            self.apostar(self.telegramBot.apostas[len(self.telegramBot.apostas) - 1].cor,
                                         self.configuracoes.getValorPrimeiroGale(), "1o GALE")
                    elif "VAMOS PARA O 2" in textoUltimaMensagem and len(self.telegramBot.apostas) >= 2:
                        if self.telegramBot.apostas[len(self.telegramBot.apostas) - 1].eGale != "2o GALE":
                            self.apostar(self.telegramBot.apostas[len(self.telegramBot.apostas) - 1].cor,
                                         self.configuracoes.getValorSegundoGale(), "2o GALE")
            except Exception as error:
                print(error)

    def apostar(self, cor, valor, gale="Nao"):
        aposta = Aposta(valor, cor, gale)
        aposta.podeApostar = self.podeApostar(aposta)
        saldoAtual = self.blaze.fazerAposta(aposta)

        self.log.saveLog(saldoAtual, self.telegramBot.getAssertividadeAtual(), aposta)
        self.telegramBot.apostas.append(aposta)

        print(
            "\n========================================================Ultimas 10=========================================================")
        for aposta_passada in self.telegramBot.apostas[-10:]:
            result = "PERDEU"
            if aposta_passada.ganhou:
                result = "GANHOU"
            print(str(self.telegramBot.apostas.index(aposta_passada) + 1).zfill(3) + " | Valor: " + str(
                aposta_passada.valor) + " | Cor: " + aposta_passada.cor + " | GALE: " + aposta_passada.eGale + " | Cor Resultado: " + aposta_passada.corResultado + " | " + result + " | Hora: " + aposta_passada.hora + " | Jogou: " + str(
                aposta_passada.podeApostar))
        print(
            "===========================================================================================================================\n")

    def podeApostar(self, aposta: Aposta):
        saldoOK = self.temSaldoSuficiente(aposta.valor)
        assertividadeOK = True  # self.assertividadeSufuciente()
        ultimasApostasOK = self.verificaUltimasApostas(aposta)

        if not saldoOK:
            print("\n==================================================")
            print("Saldo insuficiente para fazer apostas")
            print("Saldo: RS" + str(self.blaze.getSaldoAtual()))
            print("Aposta: RS" + str(aposta.valor))
            print("Saldo minimo: RS" + str(self.configuracoes.getSaldoMinimo()))
            print("==================================================\n")

        if not assertividadeOK:
            print("\n==================================================")
            print("Assertividade baixa demais para fazer apostas!!")
            print("Assertividade atual: " + str(round(self.telegramBot.getAssertividadeAtual(), 2)) + "%")
            print("Assertividade minima: " + str(round(self.configuracoes.getAssertividadeMinima(), 2)) + "%")
            print("==================================================\n")

        return saldoOK and assertividadeOK and ultimasApostasOK

    def verificaUltimasApostas(self, aposta: Aposta):
        if not len(self.telegramBot.apostas):
            return True

        if self.houveErroNasUltimasXJogadas():
            print("\n==================================================")
            print("Houve erro entre as ultimas " + str(self.configuracoes.getIntervaloGreens() + " apostas"))
            print("==================================================\n")
            return False

        if self.vitoriasSeguidas() >= self.configuracoes.getMaxVitoriasSeguidas():
            print("\n==================================================")
            print("Limite de greens seguidos atingido")
            print("==================================================\n")
            return False

        # Se não jogou a ultima e está tentando ir para um gale
        if (not self.getJogadasReverse()[0].podeApostar) and ("GALE" in aposta.eGale):
            print("\n==================================================")
            print("Nao jogou a ultima. " + aposta.eGale + " descartado")
            print("==================================================\n")
            return False

        return True

    def vitoriasSeguidas(self):
        jogadas = 0
        for aposta in self.getJogadasReverse():

            if not aposta.podeApostar:  # Não apostou
                break

            elif aposta.ganhou:  # Apostou e ganhou
                jogadas += 1

            else:  # Apostou e perdeu
                if aposta.eGale == "2o GALE" or (aposta.eGale == "1o GALE" and aposta.corResultado == "white"):
                    break
                else:
                    continue

        return jogadas

    def houveErroNasUltimasXJogadas(self):
        greens = 0
        for aposta in self.getJogadasReverse():
            if not aposta.ganhou:
                if aposta.eGale == "2o GALE" or (aposta.eGale == "1o GALE" and aposta.corResultado == "white"):
                    return True
                else:
                    continue

            greens += 1
            if greens == self.configuracoes.getIntervaloGreens():
                break

        return False

    def getJogadasReverse(self):
        apostas = self.telegramBot.apostas.copy()
        apostas.reverse()
        return apostas

    def assertividadeSufuciente(self):
        return self.telegramBot.getAssertividadeAtual() >= self.configuracoes.getAssertividadeMinima()

    def temSaldoSuficiente(self, valor: float):
        return (self.blaze.getSaldoAtual() - valor) >= self.configuracoes.getSaldoMinimo()
