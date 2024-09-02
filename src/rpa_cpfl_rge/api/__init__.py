from uvicorn import run as run_server


def main():
    run_server("rpa_cpfl_rge.api.app:app", worker=4, access_log=True, host="0.0.0.0")


if __name__ == "__main__":
    main()
