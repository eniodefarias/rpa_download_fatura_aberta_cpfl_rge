import argparse
import os
import shutil

# import sys
# import threading
import time
from datetime import datetime as datetime
from distutils.util import strtobool

# import cloudpickle
from prefect import flow, get_run_logger, task

# import threading
from process_rpa import Process_RPA
from utilities.util import Utilities


@task
def downloader(
    url: str,
    user: str,
    passwd: str,
    instalacao: str,
    dir_download: str,
    timeout: float = 180,
    headless: bool = False,
    token: str = None,
):
    logger = get_run_logger()
    logger.info("downloader iniciado")

    logger.warning(f"2 headless={headless}")

    try:
        rpa_process = Process_RPA(logger=logger)
        downloader_file = rpa_process.starter_process(
            url=url,
            user=user,
            passwd=passwd,
            instalacao=instalacao,
            dir_download=dir_download,
            timeout=timeout,
            headless=headless,
            token=token,
        )

        logger.info(f"downloader_file={downloader_file}")

        return downloader_file
        # Utilities().deletar_diretorio(dir_download)

    except Exception as e:
        Utilities().deletar_diretorio(dir_download)
        logger.error(f"Erro no fluxo : >>{e}<<\n\n\n")
        time.sleep(10)
        raise


@flow(retries=3, retry_delay_seconds=30)
def fatura_rge(
    url: str,
    user: str,
    passwd: str,
    instalacao: str,
    dir_download: str,
    timeout: float = 180,
    headless: bool = False,
    token: str = None,
):
    logger = get_run_logger()

    final_dir_download = os.path.abspath(f"{dir_download}/")
    dir_download = os.path.abspath(f"{final_dir_download}/.{token}/")

    logger.info(f"dir_download={dir_download}")
    logger.info(f"final_dir_download={final_dir_download}")

    logger.warning(f"1headless={headless}")

    dados_download = downloader(
        url=url,
        user=user,
        passwd=passwd,
        instalacao=instalacao,
        dir_download=dir_download,
        timeout=timeout,
        headless=headless,
        token=token,
    )

    logger.info(f"dados_download={dados_download}")

    filename = dados_download["filename"]
    file_download = dados_download["file_download"]

    destino_final = f"{final_dir_download}/{filename}.pdf"
    if os.path.isfile(f"{file_download}"):
        logger.info(f"O arquivo {file_download} existe.")
        shutil.move(file_download, destino_final)
        Utilities().deletar_diretorio(dir_download)


# Let's rock
if __name__ == "__main__":
    url = "https://www.cpfl.com.br/login"
    # user="xxxxxxx@gmail.com"
    # passwd="***&**$%**%&*&**"
    # instalacao="124123123123123"
    dir_download = "var/download/"

    vuser = os.getenv("VUSER")
    vpasswd = os.getenv("VPASSWD")
    vinstalacao = os.getenv("VINSTALACAO")

    parser = argparse.ArgumentParser(description="argumentos")

    try:
        parser.add_argument(
            "--headless",
            "-H",
            dest="arg_headless",
            type=lambda x: bool(strtobool(x)),
            help="parametro do headless, deve ser True ou False",
            default=True,
        )
    except Exception as e:
        erro = f"ERROR: erro ao pegar argumento arg_headless: {e}"
        print(f"{erro}")

    try:
        parser.add_argument(
            "--user", "-u", dest="arg_user", type=str, help="usuario", default=vuser
        )
    except Exception as e:
        erro = f"ERROR: erro ao pegar argumento arg_user: {e}"
        print(f"{erro}")

    try:
        parser.add_argument(
            "--passwd", "-p", dest="arg_passwd", type=str, help="senha", default=vpasswd
        )
    except Exception as e:
        erro = f"ERROR: erro ao pegar argumento arg_passwd: {e}"
        print(f"{erro}")

    try:
        parser.add_argument(
            "--instalacao",
            "-i",
            dest="arg_instalacao",
            type=str,
            help="numero da instalação",
            default=vinstalacao,
        )
    except Exception as e:
        erro = f"ERROR: erro ao pegar argumento arg_instalacao: {e}"
        print(f"{erro}")

    args = parser.parse_args()
    print(f"iniciando paramentros")

    headless = args.arg_headless
    user = args.arg_user
    passwd = args.arg_passwd
    instalacao = args.arg_instalacao
    print(f"headless={headless}")
    print(f"user={user}")
    print(f"passwd={passwd}")
    print(f"instalacao={instalacao}")

    datetimenow = datetime.today().strftime("%Y%m%d%H%M%S%f")
    user_txt = Utilities().somente_letras_numeros(user)
    cut_user_txt = user_txt[:5]

    token = f"{instalacao}{cut_user_txt}{datetimenow}"

    fatura_rge(
        url=url,
        user=user,
        passwd=passwd,
        instalacao=instalacao,
        dir_download=dir_download,
        headless=headless,
        timeout=190,
        token=token,
    )
