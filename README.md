<a href="https://wakatime.com/badge/user/739793a6-a4fb-4d88-b1e6-f79a9182d930/project/63cdcda9-95a5-4461-bc65-ee66c95de780"><img src="https://wakatime.com/badge/user/739793a6-a4fb-4d88-b1e6-f79a9182d930/project/63cdcda9-95a5-4461-bc65-ee66c95de780.svg" alt="wakatime"></a>
<p align="center">
  <img src="http://www.ideiadofuturo.com.br/img/logo_ideia.png" width="120" title="ideia"  alt="ideia">
</p>




# rpa_download_fatura_aberta_cpfl_rge
Automação RPA para realizar o download da fatura em aberto da CPFL Energia RGE de RS

## Breefing do projeto

 - abrir o site https://www.cpfl.com.br/login
 - clicar em "Entrar"
	- aguardar pelo form de login
 - inserir os dados de usuario e senha
 - clicar em "Entrar"
	- aguardar que o login seja efetivado por completo
 - selecionar a sua instalação de energia conforme o numero da instalação
	- clicar em "Avançar"
		-aguardar pelo carregamento dos dados da intalação
 - localizar a seção de "CONTA ATUAL"
	- coletar os dados de Valor, Referencia e Vencimento
		- clicar em "Ver conta completa" para realizar o download do pdf
			- renomear o arquivo baixado e salvá-lo na pasta de downloads

Vídeo ilustrativo do passo a passo do processo feito manualmente



## Depêndencias

 - python 3.11
 - Para mais informações de requisitos e configurações iniciais podem ser verificados no arquivo [setup.py](setup.py)

## Desenvolvimento

Para facilitar o uso deste projeto, foi utilizado o Makefile.

 - para acesso ao help do make basta usar o comando abaixo
	- ```bash
		make help
		```

### instruções para iniciar o ambiente de dev manualmente na sua máquina

 - realize o clone do projeto
	- ```bash
		git clone https://github.com/eniodefarias/rpa_download_fatura_aberta_cpfl_rge.git
		```
 - entre no dir do projeto
	- ```bash
		cd rpa_download_fatura_aberta_cpfl_rge
		```

#### Método 1: executando o python localmente

 - faça o download do [google-chrome](https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb) e instale em sua máquina
 - use o python 3.11 em seu venv

 - criar o ambiente virtual:
	- ```bash
		python3 -m venv .venv
		```

 - ativar o ambiente virtual:
	- ```bash
		source .venv/bin/activate
		source ~/.bashrc
		```

 - instale os pacotes necessário para o setup:
	- ```bash
		make setup
		```

 - execute o app:
	- ```bash
		make extrator user="usuario" passwd="senha" instalacao="numdaintalacao"
		```
 - recupere seu arquivo baixado no diretorio:
    - var/download/

#### Método 2: usando docker
 - tenha o docker instalado em sua máquina

 - realize a buida da imagem
	- ```bash
		make build
		```

 - execute o conteiner do projeto
	- ```bash
		make run user="usuario" passwd="senha" instalacao="numdaintalacao"
		```
 - recupere seu arquivo baixado no diretorio:
    - var/download/



***

# Melhorias para o futuro

Como todo MVP, este projeto em sua versão 0.0.1 está funcional e cumpre com os requisitos básicos propostos no briefing, porém ainda há oportunidades para melhorias:

 - melhorar o tratamento e captura na falha de usuário ou senha incorreta

 - adicionar opção para localizar e baixar segunda via de faturas anteriores

 - criar persistencia de logs em arquivo

 - criar alarmes e sinalização ao desenvolvedor e equipe de suporte (dashboard ou email) sobre erros ocorridos

 - utilizar fastapi para criar rotas de endpoint para realizar a extração via api atraves de um frontend web
	- e documentar a api via swagger

 - desenvolver um frontend web para o usuário inserir seus dados

 - criar uma interface de loginautenticação para o usuário realizar o login e salvar suas credencias de usuário da CPF e assim não precisar inserir seus dados toda vez

 - implementar banco de dados de para guardar os dados, arquivos, e informações das faturas e credenciais(criptografadas)

 - criar token para cada solicitação de extração e responder via api, para consulta posterior após o processo finalizar

 - implentar sinalização de cada etapa do processo, tempo decorrido, status e dados da fatura atrelado ao token para ser consultado via api

 - tornar o projeto em um serviço web api para poder hospedá-lo em um server/cloud

# Sugestão de dicas e boas práticas

## dicas de uso do Makefile
fontes:
 - https://makefiletutorial.com/

 -





## dicas para um bom Dockerfile:

fonte: https://testdriven.io/blog/docker-best-practices/

### ordene os comandos
 - mantenha os arquivos que mudam com frequência no final do Dockerfile
   - O Docker armazena em cache cada etapa (ou camada) em um Dockerfile específico para acelerar compilações subsequentes. Quando uma etapa muda, o cache será invalidado não apenas para essa etapa específica, mas para todas as etapas subsequentes.

Notas:

 1. Sempre coloque as camadas com maior probabilidade de alteração o mais baixo possível no Dockerfile.
 1. Combine RUN apt-get updatee RUN apt-get installcomandos. (Isso também ajuda a reduzir o tamanho da imagem. Falaremos sobre isso em breve.)
 1. Se você quiser desativar o cache para uma compilação específica do Docker, adicione o --no-cache=Truesinalizador.

### use imagens pequenas
Como exemplo, neste projeto é necessário usar a imagem para o python 3.11

Então, com base nos tamanhos das imagens relacionadas, foi escolhido a menor conformo a indicação dos tamanhos aproximados:
 - **python:3.11-slim-buster = 400Mb --> melhor escolha**
 - python:3.11-buster = 900Mb
 - python:3.11 = 1.1Gb

 ### Minimize o número de camadas

É uma boa ideia combinar os comandos RUN, COPY, e ADDo máximo possível, pois eles criam camadas. Cada camada aumenta o tamanho da imagem, pois elas são armazenadas em cache. Portanto, conforme o número de camadas aumenta, o tamanho também aumenta.

Para reduzir o tamanho da imagem combinando comandos sempre que possível. Por exemplo:

 - exemplo com multiplas camadas:
   - ```bash
     RUN apt-get update
     RUN apt-get install -y netcat
      ```
 - melhore, combinando os dois comandos em uma única camada RUN:
   - ```bash
     RUN apt-get update && apt-get install -y netcat
      ```

Notas:
1. RUN, COPY, e ADD: cada um cria camadas.
1. Cada camada contém as diferenças da camada anterior.
1. As camadas aumentam o tamanho da imagem final.

Pontas:
1. Combine comandos relacionados.
1. Remova arquivos desnecessários na mesma etapa RUN em que os criou.
1. Minimize o número de vezes que apt-get upgrade é executado, pois ele atualiza todos os pacotes para a versão mais recente.
1. Com compilações de vários estágios, não se preocupe muito em otimizar demais os comandos em estágios temporários.

### Use contêineres sem privilégios
Por padrão o docker executa todos os comandos como root, então uma recomendação de seguração é criar um usuário não-root para executar o seu projeto.

exemplo para criação de um usuário:
```bash
RUN addgroup --system app && adduser --system --group app
USER app
```

### Prefira COPIAR em vez de ADICIONAR
Use COPY, a menos que tenha certeza de que precisa da funcionalidade adicionar do ADD.

Exemplo de usos:
```bash
ADD <src> <dest>
COPY <src> <dest>
```

Ambos os comandos permitem que você copie arquivos de um local específico para uma imagem do Docker, mas o ADD tem algumas funcionades embutidas:
 1. COPY é usado para copiar arquivos ou diretórios locais do host Docker para a imagem.
 1. ADD pode ser usado para a mesma coisa, assim como para baixar arquivos externos. Além disso, se você usar um arquivo compactado (tar, gzip, bzip2, etc.) como <src> parâmetro, o ADD descompactará automaticamente o conteúdo para o local fornecido.

 ### Prefira a sintaxe de array em vez de string
 Você pode escrever os comandos CMD e ENTRYPOINTem seus Dockerfiles em formatos de array (exec) ou string (shell):

```bash
# array (exec)
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app"]

# string (shell)
CMD "gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app"
```

Ambos são acitáveis, mas prefica usar o métoddo com Arrays

Como a maioria dos shells não processa sinais para processos filhos, se você usar o formato shell CTRL-C(que gera um SIGTERM), talvez não consiga parar um processo filho.

Por exemplo, com o formato shell, o input do comando  "CTRL+C" não mata o processo. Em vez disso, você verá ^C^C^C^C^C^C^C^C^C^C^C.
Já usando o método com Array, o input do "CTRL+C" será reconhecido como um signal válido para matar o processo.

Outra ressalva é que o formato do shell carrega o PID do shell, não o processo em si.

## dicas de comandos Docker

 - realizar o build do Dockerfile
   - docker build -t \<nome-da-imagem-para-criar\> .
     - docker build -t rpa_app .

 - executar o conteiner:
   - docker run  --rm -p \<numero-da-porta-docker:porta-host\> --name \<nome-do-container\> \<nome-da-imagem\>
     - docker run  --rm -p 8000:8000 --name rpa_app-ui rpa_app

 - apagar imagens não utilizadas em lote:
   - docker rmi -f $(docker images -aq)

 - acessar um container via terminal
   - docker exec -it \<nome-do-conteiner\> /bin/bash
     - docker exec -it rpa_app-ui /bin/bash

 - criar um volume
   - docker volume create \<nome-do-volume-para-criar\>
     - docker volume create var_docker

 - persistindo  dados no conteiner
   - docker run --rm -d -p 8000:8000 --name \<nome-container\> -v var_docker:\</diretorio/dentro/do/container/\> \<nome-da-imagem\>
     - docker run --rm -d -p 8000:8000 --name rpa_app-ui -v var_docker:/var/ rpa_app

<p align="center">
  <img src="http://www.ideiadofuturo.com.br/img/logo_ideia.png" width="120" title="ideia"  alt="ideia">
</p>
