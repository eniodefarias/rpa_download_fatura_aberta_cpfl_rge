import time

import requests
from prefect import flow, get_run_logger, task


# task para puxar verificar se tem working do healthcheck
@task
def get_healthcheck_info(url_projeto, rota_endpoint="healthcheck", timeout=100):
    logger = get_run_logger()
    try:
        logger.info(f"a1 - get endpoint={url_projeto}/{rota_endpoint}")
        response = requests.get(f"{url_projeto}/{rota_endpoint}", timeout=timeout, verify=False)
        if response.status_code != 200:
            raise Exception(
                f"a3 - Falha na requisição da API: code: {response.status_code} -"
                f" response={response.text}"
            )
        return response.json()
    except Exception as e:
        logger.error(f"X4 Erro ao obter informações do healthcheck: ---{e}---\n\n\n")
        time.sleep(5)
        raise


# fluxo para puxar as tasks
@flow(retries=3, retry_delay_seconds=20)
def health_flow(
    url_projeto: str = "https://elemental-monitor-gcp-prod.http-apps.tsuru.gcp.i.globo",
    timeout: float = 100,
):
    logger = get_run_logger()
    try:
        logger.info(f"c1 - pesquisando url_projeto={url_projeto}\n\n")
        health_info = get_healthcheck_info(url_projeto)
        logger.info(f"c2 - health_info={health_info}\n\n")
        time.sleep(5)
        return True
    except Exception as e:
        logger.error(f"X3 Erro no fluxo de healthcheck: ---{e}---\n\n\n")
        time.sleep(5)
        raise


# Let's rock
if __name__ == "__main__":
    print(f"Executando app COM timeout e retry")
    try:
        print(f"inicio extracao")
        teste = health_flow(
            url_projeto="https://argus-ui-dev.apps.tsuru.dev.gcp.i.globo/x", timeout=100
        )
        print(f"fim sucesso extracao = teste={teste}")
        time.sleep(5)
    except Exception as e:
        print(f"X2 Erro ao executar o fluxo: ---{e}---")
    print(f"\n\n---------\n\n")

    # logger.info(f"\n\n---------\n\n")
    print(f"\n\n---------\n\n")

    time.sleep(20)
    health_flow(url_projeto="https://argus-ui-dev.apps.tsuru.dev.gcp.i.globo", timeout=100)
    print(f"\n\n---------\n\n")
    # time.sleep(5)

    # health_flow(url_projeto="https://argus-ui.apps.tsuru.gcp.i.globo", timeout=100)
    # print(f"\n\n---------\n\n")
    # time.sleep(5)

    # health_flow(url_projeto="https://adtech-qg-dados-api.apps.tsuru.gcp.i.globo", timeout=100)
    # print(f"\n\n---------\n\n")
    # time.sleep(5)

    # health_flow(url_projeto="https://adtech-qg-dados-api-dev.apps.tsuru.dev.gcp.i.globo", timeout=100)
    # print(f"\n\n---------\n\n")
    # time.sleep(5)
