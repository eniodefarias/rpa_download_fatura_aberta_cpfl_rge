# import os
# import sys
# import threading
# import time
# from datetime import datetime as datetime

# import cloudpickle
# import selenium
# import utilities.driversfactory

# from selenium.webdriver import ActionChains
from process_webdriver import Process_Webdriver

# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.by import By
from selenium.webdriver.support import (
    expected_conditions as EC,  # available since 2.26.0
)
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0
from utilities.util import Utilities


class Process_RPA:
    def __init__(self, logger):
        self.logger = logger
        self.pweb = Process_Webdriver(logger)
        self.logger.info(f"Class Process_RPA iniciado")

    def extrair_dados_fatura(self, driver):
        try:
            self.logger.info(f"iniciará self.pweb captura_dados_fatura")
            dados_fatura = self.pweb.captura_dados_fatura(driver=driver)
            return dados_fatura
        except Exception as e:
            self.logger.error(f"Erro ao extrair dados da fatura: >>{e}<<\n\n\n")
            # time.sleep(5)
            raise

    def create_driver(self, headless: bool = False, dir_download: str = "var/download/"):
        try:
            self.logger.info(f"preparando criação do driver")
            # headless = False
            driver = self.pweb.create_driver(headless=headless, dir_download=dir_download)
            self.logger.info(f"1main driver criado com sucesso: driver={driver}")
            # # time.sleep(20)
            return driver
        except Exception as e:
            self.logger.error(f"Erro ao criar driver : >>{e}<<\n\n\n")
            # time.sleep(5)
            raise

    def realizar_download(self, driver, dir_download):
        try:
            # limpa dir de download
            self.logger.info(f"iniciará self.pweb realizar_download")
            name_file = self.pweb.realizar_download(driver=driver, dir_download=dir_download)
            self.logger.info(f"download realizado com sucesso {name_file}")
            return name_file
        except Exception as e:
            self.logger.error(f"Erro ao realizar download : >>{e}<<\n\n\n")
            # time.sleep(5)
            raise

    def start_login(self, driver, url, user, passwd, dir_download):
        try:
            # extrator = self.pweb
            # serialized_obj = cloudpickle.dumps(extrator)

            # # Desserializar o objeto
            # deserialized_obj = cloudpickle.loads(serialized_obj)

            self.logger.info(f"iniciará self.pweb start_login")
            if self.pweb.start_login(
                driver=driver, url=url, user=user, passwd=passwd, dir_download=dir_download
            ):
                self.logger.info(f"login efetuado com sucesso")
                return True
        except Exception as e:
            self.logger.error(f"Erro ao criar driver : >>{e}<<\n\n\n")
            # time.sleep(5)
            raise

    def seleciona_instalacao(self, driver, instalacao):
        try:
            self.logger.info(f"iniciará self.pweb seleciona_instalacao")
            if self.pweb.seleciona_instalacao(driver=driver, instalacao=instalacao):
                self.logger.info(f"instalação selecionada com sucesso")
                return True
        except Exception as e:
            self.logger.error(f"Erro ao selecionar instalação : >>{e}<<\n\n\n")
            # time.sleep(5)
            raise

    def exit_driver(self, driver):
        try:
            self.logger.info(f"iniciará self.pweb exit_driver")
            self.pweb.exit_driver(driver=driver)
            self.logger.info(f"driver finalizado com sucesso")
        except Exception as e:
            self.logger.error(f"Erro ao finalizar driver : >>{e}<<\n\n\n")
            # time.sleep(5)

    def starter_process(
        self,
        url: str,
        user: str,
        passwd: str,
        instalacao: str,
        dir_download: str,
        timeout: float = 180,
        headless: bool = False,
        token: str = None,
    ):
        try:
            self.logger.warning(f"3 headless={headless}")
            driver = None
            # # Serializar o objeto usando cloudpickle
            # extrator = self.pweb
            # serialized_obj = cloudpickle.dumps(extrator)

            # # Desserializar o objeto
            # deserialized_obj = cloudpickle.loads(serialized_obj)

            driver = self.create_driver(headless, dir_download)
            if self.start_login(
                driver=driver, url=url, user=user, passwd=passwd, dir_download=dir_download
            ):
                self.logger.info(f"login efetuado com sucesso")

                if self.seleciona_instalacao(driver=driver, instalacao=instalacao):
                    self.logger.info(f"instalação selecionada com sucesso, vai para dados fatura")

                    dados_fatura = self.extrair_dados_fatura(driver=driver)

                    if dados_fatura:
                        self.logger.info(
                            f"dados da fatura extraidos com sucesso dados_fatura={dados_fatura}"
                        )
                        # mes_vencimento = dados_fatura["vencimento"]
                        mes_vencimento = dados_fatura["vencimento"].replace("\n", " ")
                        # self.logger.info(f"mes_vencimento1={mes_vencimento}")

                        # # time.sleep(20)

                        mes_valor = dados_fatura["valor"]
                        mes_referencia = dados_fatura["referencia"]
                        txt_dados_fatura_full = (
                            f"CPFL Energia - RGE - {mes_referencia} - {mes_vencimento} -"
                            f" {mes_valor} - {token}"
                        )
                        txt_dados_fatura = (
                            f"CPFL Energia - RGE - {mes_referencia} - {mes_vencimento} - {token}"
                        )

                        filename = (
                            Utilities()
                            .somente_letras_numeros_espaco_ponto(txt_dados_fatura)
                            .replace(" ", "_")
                        )

                        file_download = self.realizar_download(
                            driver=driver, dir_download=dir_download
                        )

                        try:
                            self.exit_driver(driver)
                        except Exception as er:
                            self.logger.warning(f"warning ao encerrar driver: >>{er}<< \n")

                        return {"file_download": file_download, "filename": filename}
                        # destino_final = f"{final_dir_download}/{filename}.pdf"
                        # if os.path.isfile(f"{file_download}"):
                        #     self.logger.info(f"O arquivo {file_download} existe.")
                        #     shutil.move(file_download, destino_final)
                        #     # Utilities().deletar_diretorio(dir_download)

                    else:
                        try:
                            self.exit_driver(driver)
                        except Exception as er:
                            self.logger.warning(f"warning ao encerrar driver: >>{er}<< \n")
                        raise Exception(f"Arquivo {file_download} não encontrado")

        except Exception as e:
            try:
                self.exit_driver(driver)
            except Exception as er:
                self.logger.warning(f"warning ao encerrar driver: >>{er}<< \n")
            self.logger.error(f"Erro no fluxo : >>{e}<<\n\n\n")
            # time.sleep(5)
            raise
