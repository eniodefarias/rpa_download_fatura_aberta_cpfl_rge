#estágio de construção
FROM python:3.11-slim-buster AS builder
# FROM python:3.11 AS builder
# FROM debian AS builder

RUN useradd -m -u 1000 -U -s /bin/sh app && usermod -aG sudo app

RUN apt-get update && \
    apt-get -y install curl gnupg2 logrotate tzdata wget dpkg

RUN apt-get -y install fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 \
    libcairo2 libcups2 libdbus-1-3 libdrm2 libgbm1 libglib2.0-0 libgtk-3-0 libnspr4 libnss3 \
    libpango-1.0-0 libvulkan1 libx11-6 \
    libxcb1 libxcomposite1 libxdamage1 libxext6 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils


ENV TZ="America/Sao_Paulo"

ENV APP_DIR /app
WORKDIR ${APP_DIR}

RUN wget -c https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN ls -latrh
RUN dpkg -i google-chrome-stable_current_amd64.deb

COPY setup.py ${APP_DIR}/
COPY version ${APP_DIR}/
COPY .pre-commit-config.yaml ${APP_DIR}/
COPY .coveragerc ${APP_DIR}/
COPY pyproject.toml ${APP_DIR}/src/pyproject.toml

COPY ./logrotate_app /etc/logrotate.d/app

RUN mkdir -p /var/lib/logrotate/ && \
    mkdir -p /app/var/ && \
    mkdir -p /var/log/ && \
    touch /var/log/app.log && \
    touch /var/lib/logrotate/status && \
    chmod 644 /etc/logrotate.d/* && \
    chmod 775 /app/var/ && \
    chown -R app ${APP_DIR} && \
    chgrp -R app ${APP_DIR}

# ENV PATH="/home/app/.local/bin:${PATH}"

# USER app

# RUN echo "pip direct" && pip install pre-commit && \
#     echo "pip direct" && pip install --upgrade pip && \
#     echo "pip direct" && pip install -e '.[all]'

# Estágio final
# FROM python:3.11-slim-buster AS rpa_cpfl_rge
# FROM python:3.11 AS rpa_cpfl_rge
# FROM debian AS rpa_cpfl_rge

COPY Procfile ./

ENV TZ="America/Sao_Paulo"
ENV APP_DIR /app

# RUN useradd -m -u 1000 -U -s /bin/sh app && usermod -aG sudo app

ENV PATH="/home/app/.local/bin:${PATH}"

# WORKDIR ${APP_DIR}

# COPY --from=builder /usr/ /usr/
# COPY --from=builder /etc/logrotate.d/ /etc/logrotate.d/
# COPY --from=builder /var/ /var/
# COPY --from=builder /home /home
# COPY --from=builder /app /app
COPY src ${APP_DIR}/src
COPY pyproject.toml ${APP_DIR}/src/pyproject.toml

RUN logrotate -d /etc/logrotate.d/app && \
    chown -R app /var/log && \
    chown -R app ${APP_DIR}

USER app

RUN echo "pip direct" && pip install pre-commit && \
    echo "pip direct" && pip install --upgrade pip && \
    echo "pip direct" && pip install -e '.[all]'


EXPOSE 8000

# CMD ["uvicorn", "rpa_cpfl_rge.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--access-log", "--log-level", "debug", "--use-colors"]
# CMD ["python", "src/rpa_cpfl_rge/extrator/main.py" --user "$VUSER" --passwd "$VPASSWD" --instalacao "$VINSTALACAO" ]


# CMD ["python", "src/rpa_cpfl_rge/extrator/main.py", "--user", "$VUSER", "--passwd", "$VPASSWD", "--instalacao", "$VINSTALACAO"]
CMD ["python", "src/rpa_cpfl_rge/extrator/main.py"]
