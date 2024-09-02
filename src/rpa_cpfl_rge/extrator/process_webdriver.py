import os
import sys
import threading
import time

# from prefect import flow, task, get_run_logger
# from utilities.driversfactory import DriversFactory
import utilities.driversfactory

# from selenium import webdriver
# from selenium.common.exceptions import NoSuchElementException
# from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import (
    expected_conditions as EC,  # available since 2.26.0
)
from selenium.webdriver.support.ui import WebDriverWait  # available since 2.4.0

# from datetime import datetime as datetime
#
# import cloudpickle
# import selenium


# from selenium.webdriver import ActionChains


class Process_Webdriver:
    # def __init__(self, *args, **kwargs):
    # super(CLASS_NAME, self).__init__(*args, **kwargs)

    def __init__(self, logger):
        self.logger = logger
        # self.btn_login = '(//a[@href="/b2c-auth/login"])[1]'
        # self.btn_login = '//a[@href="/b2c-auth/login"][contains(text(),"Entrar")]'
        self.btn_login = '//a[contains(text(),"Entrar")]'

        self.input_user = '//input[@id="signInName"]'
        self.input_passwd = '//input[@id="password"]'
        self.btn_entrar = '//button[@id="next"]'
        self.txt_conta_atual = '//h2[@class="card-title" and contains(text(), "Conta Atual")]'
        self.lnk_ver_conta_completa = (
            '//a[@class="entenda-conta" and contains(text(), "Ver conta completa")]'
        )
        # self.txt_mes_referencia = '//main[@id="grupo-b"]//p[@class="sub-title"]'
        self.txt_mes_referencia = '//main[@id="grupo-b"]//p[@class="sub-title"]'
        self.txt_mes_valor = '//main[@id="grupo-b"]//div[@class="card"]/div/p[@class="title"]'
        # self.txt_mes_valor = '//main[@id="grupo-b"]//div[@class="card"]/div/p[@class="title"]'
        self.txt_mes_vencimento = '(//div[@class="vencimento"])[1]'
        self.label_instalacao = '//label[@for="instalacao-(NUM_INSTALACAO)"]'
        self.h4_selecione_instalacao = (
            '//div[@id="instalacoes-results-wrapper"]/h4[contains(text(), "Selecione sua'
            ' instalação")]'
        )
        self.btn_avancar = '//input[@id="btn-buscar"]'

        self.lock = threading.Lock()

    # def __reduce__(self):
    #     raise TypeError("Serialização não permitida para esta classe")

    # def __reduce_ex__(self, protocol):
    #     raise TypeError("Serialização não permitida para esta classe")

    def __getstate__(self):
        state = self.__dict__.copy()
        # Remova o lock do estado a ser serializado
        del state["lock"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()

    def exit_driver(self, driver):
        print("\n\n")
        try:
            try:
                self.logger.debug("saindo stop_client webdriver")
                driver.stop_client()
                self.logger.info("OK stop_client webdriver")
            except Exception as e:
                self.logger.warning(f"saindo close webdriver {e}")

            try:
                self.logger.debug("saindo close webdriver")
                driver.close()
                self.logger.info("OK close webdriver")
            except Exception as e:
                self.logger.warning(f"saindo close webdriver {e}")

            try:
                self.logger.debug("saindo quit webdriver")
                driver.quit()
                self.logger.info("OK quit webdriver")
            except Exception as e:
                self.logger.warning(f"saindo quit webdriver {e}")

            try:
                self.logger.debug("saindo exit webdriver")
                driver.exit()
                self.logger.info("OK exit webdriver")
            except Exception as e:
                self.logger.warning(f"saindo exit webdriver {e}")

            try:
                self.logger.debug("saindo stop webdriver")
                driver.stop()
                self.logger.info("OK stop webdriver")
            except Exception as e:
                self.logger.warning(f"saindo stop webdriver {e}")

            try:
                self.logger.debug("saindo dispose webdriver")
                driver.dispose()
                self.logger.info("OK dispose webdriver")
            except Exception as e:
                self.logger.warning(f"saindo dispose webdriver {e}")

        except Exception as e:
            self.logger.error(f"ERRO ao finalizar webdriver! {e}")
        print("\n\n")

    def existe_xpath(self, driver, xpath, tempo=2, loop=9):
        url_atual = driver.current_url
        self.logger.debug(f"url_atual: {url_atual}")
        retorno = False
        counter = 1
        while loop > 0:
            try:
                # print('\n\n')
                self.logger.info(f'  ({loop})Procurando xpath "{xpath}"')
                elemento = WebDriverWait(driver, tempo).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                self.logger.info(f'  ({loop})Achou xpath "{xpath}"')
                retorno = True
                loop = 0
            except:
                time.sleep(counter)
            counter += 1
            loop -= 1
        if not retorno:
            url_atual = driver.current_url
            msg = (
                f"    ({loop})Não achou o xpath {xpath} para clicar na pagina ({url_atual}) do"
                " navegador; "
            )
            self.logger.error(msg)
            # raise Exception(msg)
        print("\n\n")
        return retorno

    def clicar_xpath(self, driver, xpath, tempo=2, loop=5):
        url_atual = driver.current_url
        self.logger.debug(f"url_atual: {url_atual}")
        retorno = False
        counter = 1
        while loop > 0:
            try:
                # print('\n\n')
                self.logger.info(f'  ({loop})Procurando xpath "{xpath}"')
                elemento = WebDriverWait(driver, tempo).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                self.logger.info(f'  ({loop})Achou xpath "{xpath}"')
                elemento.click()
                self.logger.info(f'  ({loop})Clicou xpath "{xpath}"')
                retorno = True
                loop = 0
            except:
                time.sleep(counter)
            counter += 1
            loop -= 1
        if not retorno:
            url_atual = driver.current_url
            msg = (
                f"    ({loop})Não achou o xpath {xpath} para clicar na pagina ({url_atual}) do"
                " navegador; "
            )
            self.logger.error(msg)
            # raise Exception(msg)
        print("\n\n")
        return retorno

    def wait_for_downloads(self, dir_downloadx=None, timemax=300, delay=0.3):
        time.sleep(delay)
        download_path = os.path.abspath(f"{dir_downloadx}")
        self.logger.info(f"download_path={download_path}")
        self.logger.info(f"dir_downloadx={dir_downloadx}")

        max_delay = timemax
        interval_delay = 1
        total_delay = 0
        file = ""
        done = False
        while not done and total_delay < max_delay:
            files = [f for f in os.listdir(download_path) if f.endswith(".crdownload")]
            file_full = [f for f in os.listdir(download_path) if not f.endswith(".crdownload")]

            if files:
                self.logger.info(f"        downloading... {files}")

            if file_full:
                self.logger.info(f'         downloaded!!! "{file_full}"')
            # if not files and len(file) > 1:
            if not files and len(file_full) >= 1:
                done = True
                max_delay = 0
            if file_full:
                file = file_full[0]

            time.sleep(interval_delay)
            total_delay += interval_delay
            self.logger.info(f"                loop: {total_delay}")

        if done:
            self.logger.info(f'File(s) "{file}" downloaded in {total_delay} seconds')
        if not done:
            self.logger.error("File(s) couldn't be downloaded")
        final = os.path.abspath(download_path + "/" + file).replace(".crdownload", "")
        return final

    def digitar_input_xpath(self, driver, xpath, texto, tempo=1, loop=3):
        url_atual = driver.current_url
        self.logger.debug(f"url_atual: {url_atual}")
        retorno = False
        counter = 1
        while loop > 0:
            try:
                # print('\n\n')
                self.logger.info(f' digitar: Procurando xpath "{xpath}"')
                elemento = WebDriverWait(driver, tempo).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                self.logger.info(f' digitar: Achou xpath "{xpath}"')
                elemento.click()
                self.logger.info(f' digitar: Clicou xpath "{xpath}"')

                elemento.send_keys(texto)
                self.logger.info(f' digitar: Digitou "{texto}" no xpath "{xpath}"')

                retorno = True
                loop = 0
            except:
                time.sleep(counter)
            counter += 1
            loop -= 1
        if not retorno:
            url_atual = driver.current_url
            msg = (
                f"Não achou o xpath {xpath} para digitar o texto {texto} na pagina ({url_atual}) do"
                " navegador; "
            )
            self.logger.error(msg)
            # raise Exception(msg)
        print("\n\n")
        return retorno

    def captura_texto_xpath(self, driver, xpath, tempo=1, loop=3):
        url_atual = driver.current_url
        self.logger.debug(f"url_atual: {url_atual}")
        retorno = ""
        bol_retorno = False
        counter = 1

        while loop > 0:
            try:
                # print('\n\n')
                self.logger.info(f' txt Procurando xpath "{xpath}"')
                elemento = WebDriverWait(driver, tempo).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                self.logger.info(f' txt Achou xpath "{xpath}"')
                retorno = elemento.text
                self.logger.info(f' txt Capturou texto "{retorno}"')
                loop = 0
                bol_retorno = True
            except Exception as e:
                self.logger.error(f'Erro ao capturar texto xpath "{xpath}" {e}')
                time.sleep(counter)
            counter += 1
            loop -= 1
        if not bol_retorno:
            url_atual = driver.current_url
            msg = (
                f"Não achou o xpath {xpath} para capturar o texto na pagina ({url_atual}) do"
                " navegador; "
            )
            self.logger.error(msg)
            # raise Exception(msg)
            retorno = False
        print("\n\n")
        return retorno

    def captura_dados_fatura(self, driver):
        self.logger.info(f"capturando dados da fatura")
        mes_vencimento = self.captura_texto_xpath(
            driver=driver, xpath=self.txt_mes_vencimento, tempo=5, loop=15
        )
        self.logger.info(f"mes_vencimento={mes_vencimento}")
        if mes_vencimento:
            mes_valor = self.captura_texto_xpath(
                driver=driver, xpath=self.txt_mes_valor, tempo=5, loop=15
            )
            self.logger.info(f"mes_valor={mes_valor}")
            if mes_valor:
                mes_referencia = self.captura_texto_xpath(
                    driver=driver, xpath=self.txt_mes_referencia, tempo=5, loop=15
                )
                self.logger.info(f"mes_referencia={mes_referencia}")
                if mes_referencia:
                    self.logger.info(
                        f"vencimento={mes_vencimento} valor={mes_valor} referencia={mes_referencia}"
                    )
                    self.logger.info(f"referencia={mes_referencia}")
                    self.logger.info(f"valor={mes_valor}")

                    return {
                        "vencimento": mes_vencimento,
                        "valor": mes_valor,
                        "referencia": mes_referencia,
                    }

                else:
                    raise Exception(f"Erro ao capturar dados da fatura mes_referencia")
            else:
                raise Exception(f"Erro ao capturar dados da fatura mes_valor")
        else:
            raise Exception(f"Erro ao capturar dados da fatura mes_vencimento")

    def seleciona_instalacao(self, driver, instalacao):
        # txt_instalacao = f'instalacao-{3093095986}'

        xpath_instalacao = self.label_instalacao.replace("(NUM_INSTALACAO)", instalacao)

        if self.clicar_xpath(driver=driver, xpath=xpath_instalacao, tempo=2, loop=9):
            if self.clicar_xpath(driver=driver, xpath=self.btn_avancar, tempo=2, loop=9):
                if self.existe_xpath(driver=driver, xpath=self.txt_conta_atual, tempo=5, loop=15):
                    self.logger.info(f"Login realizado com sucesso na instalação {instalacao}")
                    return True
                else:
                    raise Exception(f"Erro ao entrar em instalação {instalacao}")
            else:
                raise Exception(f"Erro ao clicar no botão de avançar")

        else:
            raise Exception(f"Erro ao selecionar instalação residencia {residencia}")

    def realizar_download(self, driver, dir_download):
        try:
            self.logger.info(f"realizando download da fatura")
            if self.clicar_xpath(driver=driver, xpath=self.lnk_ver_conta_completa, tempo=2, loop=9):
                result_download = self.wait_for_downloads(dir_downloadx=dir_download)
                return result_download
            else:
                raise Exception(f"Erro ao clicar no link ver conta completa")
        except Exception as e:
            self.logger.error(f"Erro ao clicar no link ver conta completa: >>{e}<<")
            raise

    def create_driver(
        self, headless=False, dir_download="var/download/", altura=1200, largura=1000, kiosk=False
    ):
        # logger = get_run_logger()
        try:
            print(f"a1")
            DriverFactory = utilities.driversfactory.DriverFactory
            driverfactory = DriverFactory()
            self.logger.info(
                "criando driver"
                f" headless={headless} dir_download={dir_download} largura={largura} altura={altura}"
            )
            print(f"a2")
            driver = driverfactory.create_driver(
                type="chrome",
                headless=headless,
                path_to_download=dir_download,
                install_extension=False,
                largura=largura,
                altura=altura,
                kiosk=kiosk,
                nome_robo_exec=sys.argv[0],
                robo_pid_exec=os.getpid(),
                logger=None,
                scale_factor=0.8,
                # scale_factor=1,
                posX=30,
                posY=1050,
            )

            self.logger.info(f"2 xt driver criado com sucesso: {driver}")

            return driver
        except Exception as e:
            try:
                self.exit_driver(driver)
            except Exception as er:
                self.logger.error(f"Erro ao encerrar driver: >>{er}<< \n")

            self.logger.error(f"Erro ao criar driver: >>{e}<< \n")
            raise

    def start_login(
        self,
        driver,
        url: str,
        user: str,
        passwd: str,
        dir_download: str,
        timeout: float = 180,
        headless: bool = False,
    ):
        self.logger.info(f"preparando criação do driver")
        # headless = False

        self.logger.info(f"start_login criado com sucesso")

        self.logger.info(f"abrindo url {url}")
        driver.get(url)
        time.sleep(1)
        # driver.get(f"{url}/b2c-auth/login")

        # self.clicar_xpath(driver=driver, xpath="//BUTTON[@id='onetrust-accept-btn-handler']", tempo=5, loop=5)
        # time.sleep(1)

        if self.clicar_xpath(driver=driver, xpath=self.btn_login, tempo=5, loop=5):
            # if True:
            self.logger.info(f"clicou no btn login")
            if self.digitar_input_xpath(
                driver=driver, xpath=self.input_user, texto=user, tempo=1, loop=3
            ):
                if self.digitar_input_xpath(
                    driver=driver, xpath=self.input_passwd, texto=passwd, tempo=1, loop=3
                ):
                    if self.clicar_xpath(driver=driver, xpath=self.btn_entrar, tempo=2, loop=9):
                        if self.existe_xpath(
                            driver=driver, xpath=self.h4_selecione_instalacao, tempo=5, loop=5
                        ):
                            self.logger.info(f"Login realizado com sucesso")
                            return True
                        else:
                            raise Exception(f"Erro ao validar login")
                    else:
                        raise Exception(f"Erro ao clicar no botão de login")
                else:
                    raise Exception(f"Erro ao digitar senha")
            else:
                raise Exception(f"Erro ao digitar usuário")
        else:
            raise Exception(f"Erro ao clicar no botão de login")


# dados_fatura = self.captura_dados_fatura(driver)
#                             self.logger.info(f"dados_fatura={dados_fatura}")
#                             # resultado_download = self.download_fatura(driver)
#                             time.sleep(55)

# def __getstate__(self):
#     state = self.__dict__.copy()
#     del state['lock']
#     return state
