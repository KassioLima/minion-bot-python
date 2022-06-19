from selenium import webdriver
from minion import Minion

with webdriver.Firefox() as driver:
    Minion(driver)