FROM jenkins/jenkins:lts-jdk21

USER root

# Install required packages
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    ca-certificates \
    lsb-release \
    gnupg

# Install Docker CLI
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /usr/share/keyrings/docker.gpg && \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker.gpg] https://download.docker.com/linux/debian \
    $(. /etc/os-release && echo $VERSION_CODENAME) stable" \
    > /etc/apt/sources.list.d/docker.list && \
    apt-get update && \
    apt-get install -y docker-ce-cli

# Copy plugin list
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Install Jenkins plugins
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

USER jenkins