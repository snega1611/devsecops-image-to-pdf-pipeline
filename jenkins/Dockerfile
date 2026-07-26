FROM jenkins/jenkins:lts-jdk21

USER root

# Install required packages + Docker CLI
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip \
    python3-venv \
    curl \
    ca-certificates \
    docker.io \
    && rm -rf /var/lib/apt/lists/*


# Copy plugin list
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

# Install Jenkins plugins
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt


USER jenkins