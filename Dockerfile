FROM python:3.12.10

RUN mkdir /app && \
        chmod 777 /app && \
        apt-get update && \
        apt-get -y upgrade

RUN install -d -m 0755 /etc/apt/keyrings
RUN apt-get -y install wget sudo which vim
RUN wget -q https://packages.mozilla.org/apt/repo-signing-key.gpg -O- | sudo tee /etc/apt/keyrings/packages.mozilla.org.asc > /dev/null
RUN gpg -n -q --import --import-options import-show /etc/apt/keyrings/packages.mozilla.org.asc | awk '/pub/{getline; gsub(/^ +| +$/,""); if($0 == "35BAA0B33E9EB396F59CA838C0BA5CE6DC6315A3") print "\nThe key fingerprint matches ("$0").\n"; else print "\nVerification failed: the fingerprint ("$0") does not match the expected one.\n"}'
RUN echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] \
            https://packages.mozilla.org/apt mozilla main" | sudo tee -a /etc/apt/sources.list.d/mozilla.list > /dev/null
RUN echo 'Package: * \
            Pin: origin packages.mozilla.org \
            Pin-Priority: 1000 \
            ' | tee /etc/apt/preferences.d/mozilla

RUN apt-get update && \
        apt-get -y upgrade
RUN apt-get -y --fix-broken install gnome-browser-connector \
        firefox-esr \
        software-properties-common \
        cron \
        netcat-openbsd \
        telnet

# Configure Poetry
ENV POETRY_VERSION=2.1.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

# Install poetry separated from system interpreter
RUN python3 -m venv $POETRY_VENV \
    && $POETRY_VENV/bin/pip install -U pip setuptools \
    && $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"

COPY cron-init /etc/cron.d/cron-init
COPY entrypoint.sh /tmp/entrypoint.sh
ADD . /app

WORKDIR /app

# Install dependencies
RUN poetry lock && \
        poetry show --tree && \
        poetry install -v && \
        touch /var/log/cron.log && \
        crontab /etc/cron.d/cron-init && \
        chmod -Rf 777 /tmp/entrypoint.sh

#CMD [ "/bin/bash" ]
#CMD [ "nohup", "poetry", "run", "python3.13", "src/main.py", "&" ]
#CMD [ "poetry", "run", "python3.13", "src/main.py" ]
ENTRYPOINT [ "/tmp/entrypoint.sh" ]
