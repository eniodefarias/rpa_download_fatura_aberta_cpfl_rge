import os

from setuptools import find_packages, setup
from setuptools.command.install import install


class Utilities:
    def sobrescrever_arquivo(self, filename, valor, encode="utf-8"):
        with open(filename, "w", errors="replace", encoding=encode) as file:
            file.write("{}".format(valor))
            file.close()

    def ler_arquivo(self, filename, encoding=None):
        if encoding is None:
            f = open(filename, errors="replace")
        else:
            f = open(filename, encoding=encoding, errors="replace")
        lines = f.read()
        f.close()
        return lines


class PostInstall(install):
    def __init__(self, *args, **kwargs):
        super(PostInstall, self).__init__(*args, **kwargs)
        _install_requirements()


def _install_requirements():
    os.system("pip install pre-commit")
    os.system("pre-commit install")
    os.system("pre-commit run --all-files")


util = Utilities()
versao = util.ler_arquivo("version")

REQUIREMENTS_PACKAGES = [
    "alembic == 1.13.2",
    "setuptools == 70.1.1",
    "fastapi == 0.111.1",
    "pydantic == 2.8.2",
    "python-dotenv == 1.0.1",
    "uvicorn == 0.30.3",
    "prefect==2.20.3",
    "selenium",
    "webdriver_manager",
    "undetected_chromedriver",
    "get_chromedriver",
]

TEST_PACKAGES = [
    "pytest == 7.3.1",
]

EXTRA_REQUIREMENTS = {"test": TEST_PACKAGES}

setup(
    name="rpa_cpfl_rge",
    # para alterar a versão, edite o arquivo version na raiz do repositorio
    version=f"{versao}",
    description="API e extrator de FATURA CPFL RGE",
    packages=find_packages(where="src", include=["rpa_cpfl_rge*"]),
    package_dir={"": "src"},
    python_requires=">= 3.11",
    include_package_data=True,
    install_requires=REQUIREMENTS_PACKAGES,
    cmdclass={"install": PostInstall},
)
