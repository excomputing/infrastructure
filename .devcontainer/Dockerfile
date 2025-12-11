# Base Image
FROM python:3.13.7-bookworm


# If the steps of a `Dockerfile` use files that are different from the `context` file, COPY the
# file of each step separately; and RUN the file immediately after COPY
WORKDIR /app
COPY /.devcontainer/requirements.txt /app


# Environment
SHELL [ "/bin/bash", "-c" ]


# Setting-up
RUN apt update && apt -q -y upgrade && apt -y install sudo && sudo apt -y install graphviz && apt -y install vim && \
    sudo apt -y install wget && sudo apt -y install curl && sudo apt -y install unzip && \
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "/tmp/awscliv2.zip" && \
    unzip /tmp/awscliv2.zip -d /tmp/ && cd /tmp && sudo ./aws/install && cd ~ && \
    pip install --upgrade pip && \
    pip install --requirement /app/requirements.txt --no-cache-dir && \
    curl -O "https://s3.us-west-2.amazonaws.com/amazon-eks/1.33.5/2025-11-13/bin/linux/amd64/kubectl" && \
    curl -O "https://s3.us-west-2.amazonaws.com/amazon-eks/1.33.5/2025-11-13/bin/linux/amd64/kubectl.sha256" && \
    chmod +x ./kubectl && \
    mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$HOME/bin:$PATH && \
    echo 'export PATH=$HOME/bin:$PATH' >> ~/.bashrc && \
    curl -sLO "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_Linux_amd64.tar.gz" && \
    curl -sL "https://github.com/eksctl-io/eksctl/releases/latest/download/eksctl_checksums.txt" | grep Linux_amd64 | sha256sum --check && \
    tar -xzf eksctl_Linux_amd64.tar.gz -C /tmp && rm eksctl_Linux_amd64.tar.gz && \
    sudo install -m 0755 /tmp/eksctl /usr/local/bin && rm /tmp/eksctl


# Port
EXPOSE 8050


# ENTRYPOINT
ENTRYPOINT ["bash"]
