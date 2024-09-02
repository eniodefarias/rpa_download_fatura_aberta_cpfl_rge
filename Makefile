.PHONY: help
-include makefiles/*.mk
ENV := dev
VERSION := $(shell cat version)
PROJECT := rpa_cpfl_rge


# Main variables
BASE_URL := http://localhost:8000

# ENVIRONMENT -----------------------------------------------------------------------------

# venv:
# python3 -m venv .venv
# source .venv/bin/activate
# source ~/.bashrc

help:			# exibe esta lista de comandos disponíveis
	@echo ""
	@echo "     $(PROJECT) - $(ENV) - $(VERSION)"
	@echo "---------------------------------------"
	@cat Makefile | grep -E '^[a-zA-Z0-9_-]+:.*?# .*$$' | awk 'BEGIN {FS = ":.*?# "}; {printf " make \033[36m%-15s\033[0m -> %s\n", $$1, $$2}'
	@echo "---------------------------------------"
	@echo ""



setup:			# instala as dependencias python do projeto no venv local conforme o arquivo setup.py
	@echo "Iniciando SETUP \n"
	@pip install -e ".[all]"
	@echo "\n SETUP completo"

# api:			# executa a api via uvicorn localmente sem docker
#	@uvicorn rpa_cpfl_rge.api.app:app --host 0.0.0.0 --port 8000 --reload --access-log  --log-level debug

extrator:		# executa o extrator diretamente, use assim: make extrator user="usuario" passwd="senha" instalacao="numdaintalacao"
	@python src/rpa_cpfl_rge/extrator/main.py --user '$(user)' --passwd '$(passwd)' --instalacao '$(instalacao)' --headless False


# Build
build:			# realiza o build do projeto no docker local
	@docker build --tag "$(PROJECT)-$(ENV)-$(VERSION)" .
	@echo "Finalizado Docker Build ver: $(VERSION)"

stop:			# para o container docker local
	docker container stop "$(PROJECT)-$(ENV)"
	@echo "Encerrador conteiner: $(PROJECT)-$(ENV)"

run:			# executa o container docker local, use assim: make run user="usuario" passwd="senha" instalacao="numdaintalacao"
	@mkdir $(shell pwd)/var
	@chmod 755 $(shell pwd)/var
	@docker run -it --rm -p 8000:8000 --name "$(PROJECT)-$(ENV)" -v $(shell pwd)/var/:/app/var -e VUSER="$(user)" -e VPASSWD="$(passwd)" -e VINSTALACAO="$(instalacao)"  "$(PROJECT)-$(ENV)-$(VERSION)"




#	@docker run -it --rm -p 8000:8000 --name "$(PROJECT)-$(ENV)" "$(PROJECT)-$(ENV)-$(VERSION)"


docker-shell:	# abre uma sessão shell no docker local
	@docker exec -it "$(PROJECT)-$(ENV)" /bin/bash

# TSURU
#tsuru-log:		# faz a chamada do log do tsuru
#	@tsuru app log -f -a $(PROJECT)-$(ENV)

#tsuru-shell:	# abre uma sessão shell no tsuru
#	@tsuru app shell -a $(PROJECT)-$(ENV)

#deploy:			# realiza o deploy diretamente no tsuru, mas verifique o ENV do Makefile antes de fazer isso. Tenha cuidado e atenção.
#	@tsuru app deploy -a $(PROJECT)-$(ENV) --dockerfile .
