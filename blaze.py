import time
from selenium.webdriver.common.by import By
from selenium.webdriver.opera.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from aposta import Aposta
from window import Window
from os import getenv


class Blaze(Window):

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self._blazeLink = getenv("BLAZE_LINK")
        self._email = getenv("BLAZE_EMAIL")
        self._password = getenv("BLAZE_PASSWORD")

        self._driver.get(self._blazeLink)
        self._window_handle = driver.current_window_handle
        time.sleep(2)

        self._driver.find_element(By.CLASS_NAME, "link").click()
        time.sleep(2)
        self._driver.find_elements(By.TAG_NAME, "input")[0].send_keys(self._email)
        time.sleep(1)
        self._driver.find_elements(By.TAG_NAME, "input")[1].send_keys(self._password)
        time.sleep(1)
        self._driver.find_element(By.CLASS_NAME, "red.submit.undefined").click()
        time.sleep(2)

    def getSaldoAtual(self):
        elementoSaldo = self._driver.find_element(By.CLASS_NAME, "currency")
        saldo = float(str(self._driver.execute_script("return arguments[0].innerText", elementoSaldo)).split("R$")[1])
        return saldo

    def fazerAposta(self, aposta: Aposta):
        time.sleep(3)
        self._driver.find_element(By.CLASS_NAME, "input-field").clear()
        if aposta.podeApostar:
            print("Apostando RS" + str(aposta.valor) + " em " + aposta.cor)
            time.sleep(0.5)
            self._driver.find_element(By.CLASS_NAME, "input-field").send_keys(str(aposta.valor))
            time.sleep(0.5)
            elementoOpcoesAposta = self._driver.find_element(By.CLASS_NAME, 'input-wrapper.select')
            elementoOpcoesAposta.find_element(By.CLASS_NAME, aposta.cor).click()
            time.sleep(0.5)
            divDoBotaoDeApostar = self._driver.find_element(By.CLASS_NAME, "place-bet")
            while not divDoBotaoDeApostar.find_element(By.CLASS_NAME, "red").is_enabled():
                pass
            # divDoBotaoDeApostar.find_element(By.CLASS_NAME, "red").click()
        else:
            print("Observando aposta de RS" + str(aposta.valor) + " em " + aposta.cor)

        aposta.ganhou = self.getResultadoAposta(aposta)

        if aposta.ganhou:
            print("GANHOU")
        else:
            print("PERDEU")

        if aposta.ganhou and aposta.podeApostar:
            return self.getSaldoAtual() + (aposta.valor * 2)
        else:
            return self.getSaldoAtual()

    def getResultadoAposta(self, aposta: Aposta):
        print("Aguardando resultado da aposta")
        ultimoSorteio = self._driver.find_element(By.CLASS_NAME, "sm-box").id
        while self._driver.find_element(By.CLASS_NAME, "sm-box").id == ultimoSorteio:
            continue

        elementoCorSorteada = self._driver.find_element(By.CLASS_NAME, "sm-box")
        corSorteada = str(self._driver.execute_script("return arguments[0].className.split(' ')[1]", elementoCorSorteada))
        aposta.corResultado = corSorteada

        return aposta.cor == corSorteada