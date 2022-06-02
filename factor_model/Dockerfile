FROM continuumio/miniconda3

# Add Maintainer Info
LABEL maintainer="ssmif"

ARG ssh_private_key
RUN test -n "$ssh_private_key"

# base dependencies
RUN mkdir -p /usr/share/man/man1
RUN apt-get update
RUN apt-get install -y g++ default-jre-headless scala

# spark setup
RUN wget https://archive.apache.org/dist/spark/spark-3.1.1/spark-3.1.1-bin-hadoop3.2.tgz && \
    tar -xvf spark-3.1.1-bin-hadoop3.2.tgz && rm spark-3.1.1-bin-hadoop3.2.tgz && \
    mv spark-3.1.1-bin-hadoop3.2 /opt/spark

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin

# teset if pyspark is wworking
RUN pyspark --version

# Authorize github ssh
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add ssh keys
RUN echo "$ssh_private_key" > /root/.ssh/id_ed25519 && \
    chmod 600 /root/.ssh/id_ed25519

ARG FUNCTION_DIR="/app"

RUN mkdir -p ${FUNCTION_DIR}

# create app directory
WORKDIR ${FUNCTION_DIR}

# Create the environment
RUN mkdir -p envs
COPY envs/environment_linux.yml envs
RUN conda env create --prefix "envs/factor_model_env" --file envs/environment_linux.yml

# everything below is not cached by docker
ARG cache_bust
RUN test -n "$cache_bust"

# install pip dependencies
COPY envs/requirements.txt envs
RUN "envs/factor_model_env/bin/pip" install --force-reinstall --no-cache-dir -r envs/requirements.txt

# clean
RUN apt-get remove -y g++

# Remove SSH keys
RUN rm -rf /root/.ssh/
