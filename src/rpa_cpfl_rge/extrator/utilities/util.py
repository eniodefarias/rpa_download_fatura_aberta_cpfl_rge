import os
import re
import shutil

# import sys
import threading

# import time
# from datetime import datetime as datetime

# import cloudpickle


class Utilities:
    def __init__(self):
        self.lock = threading.Lock()

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

    def agregar_arquivo(self, filename, valor, encode="utf-8"):
        with open(filename, "a", errors="replace", encoding=encode) as f:
            f.write(valor + "\n")
            f.close()

    def limpar_diretorio(self, path):
        # path = "diretorio"
        dir = os.listdir(path)
        os.listdir(path)
        # time.sleep(0.2)
        print("\n")
        for file in dir:
            self.logger.info("deletando {}/{}".format(path, file))
            try:
                os.remove(path + "/" + file)
            except:
                self.logger.info("Deletando file {} ---> não encontrado".format(file))
            # if file == "arquivo.txt":
            #    os.remove(file)
        print("\n")
        # time.sleep(0.3)

    def criar_diretorio(self, dirName):
        try:
            os.makedirs(dirName)
            print(f"       Directory {dirName} Created OK")
        # except FileExistsError:
        # except Exception as e:
        except:
            print(f"       Directory {dirName} already exists")
            # pass

    def deletar_diretorio(self, dir_name):
        try:
            shutil.rmtree(dir_name)
            print(f"Diretório {dir_name} e todo o seu conteúdo foram deletados com sucesso")
        except OSError as e:
            print(f"Erro ao deletar o diretório: {e}")

    def somente_letras_numeros_espaco_ponto(self, string):
        return re.sub("[^a-zA-Z0-9. ]+", "", string)

    def somente_letras_numeros(self, string):
        return re.sub("[^a-zA-Z0-9]+", "", string)

    def somente_letras_espaco(self, string):
        return re.sub("[^a-zA-Z ]+", "", string)

    def somente_letras(self, string):
        return re.sub("[^a-zA-Z]+", "", string)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["lock"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()
