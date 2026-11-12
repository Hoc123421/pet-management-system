# Custom Jenkins image: Jenkins LTS + .NET 8 SDK + Docker CLI + Compose + SSH client
FROM jenkins/jenkins:lts-jdk17

USER root

# Base tools + SSH client (dùng cho stage deploy qua SSH)
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl gnupg lsb-release openssh-client wget \
    && apt-get install -y --no-install-recommends \
        $(apt-cache search --names-only '^libicu[0-9]+$' | awk '{print $1}' | head -n1) \
        libssl3 zlib1g libgssapi-krb5-2 \
    && rm -rf /var/lib/apt/lists/*

# Docker CLI + docker compose plugin (dùng docker.sock của host)
RUN install -m 0755 -d /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc \
    && chmod a+r /etc/apt/keyrings/docker.asc \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo $VERSION_CODENAME) stable" > /etc/apt/sources.list.d/docker.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends docker-ce-cli docker-compose-plugin \
    && rm -rf /var/lib/apt/lists/* \
    && printf '#!/bin/sh\nexec docker compose "$@"\n' > /usr/local/bin/docker-compose \
    && chmod +x /usr/local/bin/docker-compose

# .NET 8 SDK
RUN wget -q https://dot.net/v1/dotnet-install.sh -O /tmp/dotnet-install.sh \
    && bash /tmp/dotnet-install.sh --channel 8.0 --install-dir /usr/share/dotnet \
    && ln -s /usr/share/dotnet/dotnet /usr/local/bin/dotnet \
    && rm /tmp/dotnet-install.sh
ENV DOTNET_CLI_TELEMETRY_OPTOUT=1 \
    DOTNET_ROOT=/usr/share/dotnet \
    PATH="${PATH}:/root/.dotnet/tools"

# SonarScanner for .NET (cần Java - đã có sẵn trong image Jenkins)
RUN dotnet tool install --global dotnet-sonarscanner

# Cho phép git đọc repo được mount từ host
RUN git config --system --add safe.directory '*'

# Cài sẵn plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt
