import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re


class TestPeselgenerator():
    def setup_method(self, method):  # wykonuje sie przed testem
        self.driver = webdriver.Chrome(executable_path='C:\webdriver\chromedriver.exe')
        self.vars = {}
        self.driver.set_window_size(1050, 660)

    def teardown_method(self, method):  # wykonuje się po teście
        self.driver.quit()

    def generate_pesel(self, year: str, month: str, day: str, gender: str):
      self.driver.find_element(By.NAME, "rok").send_keys(year)

      month_dropdown = self.driver.find_element(By.NAME, "miesiac")
      month_dropdown.find_element(By.XPATH, f"//option[. = '{month}']").click()

      self.driver.find_element(By.NAME, "dzien").send_keys(day)

      gender_dropdown = self.driver.find_element(By.NAME, "plec")
      gender_dropdown.find_element(By.XPATH, f"//option[. = '{gender}']").click()

      self.driver.find_element(By.CSS_SELECTOR, "input:nth-child(14)").click()


    def test_peselgenerator_kobieta_przed_2000(self):  # test do wykonania

        # wzorzec AAA - Arrange, Act, Assert

        # Arrange
        self.driver.get("http://pesel.felis-net.com/")

        # Act

        self.generate_pesel("1987", "marzec", "07", "kobieta")

        # Assert

        pesel = self.driver.find_element_by_xpath("//center/b").text
        result = re.search(pattern=r"PESEL: 870307\d{3}[24680]\d", string=pesel)
        assert result is not None


    def test_peselgenerator_kobieta_po_2000(self):  # test do wykonania

        # Arrange
        self.driver.get("http://pesel.felis-net.com/")

        # Act

        self.generate_pesel("2000", "marzec", "07", "kobieta")

        # Assert

        pesel = self.driver.find_element_by_xpath("//center/b").text
        result = re.search(pattern=r"PESEL: 002307\d{3}[24680]\d", string=pesel)
        assert result is not None



    def test_peselgenerator_mezczyzna_przed_2000(self):  # test do wykonania

        # Arrange
        self.driver.get("http://pesel.felis-net.com/")

        # Act

        self.generate_pesel("1987", "marzec", "07", "mężczyzna")

        # Assert

        pesel = self.driver.find_element_by_xpath("//center/b").text
        result = re.search(pattern=r"PESEL: 870307\d{3}[13579]\d", string=pesel)
        assert result is not None

    def test_peselgenerator_mezczyzna_po_2000(self):  # test do wykonania

      # Arrange
      self.driver.get("http://pesel.felis-net.com/")

      # Act

      self.generate_pesel("2000", "marzec", "07", "mężczyzna")

      # Assert

      pesel = self.driver.find_element_by_xpath("//center/b").text
      result = re.search(pattern=r"PESEL: 002307\d{3}[13579]\d", string=pesel)
      assert result is not None
