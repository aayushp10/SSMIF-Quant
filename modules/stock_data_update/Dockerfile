# docker container for lambda functions with conda
FROM continuumio/miniconda3

# Add Maintainer Info
LABEL maintainer="ssmif"

ARG ssh_private_key
RUN test -n "$ssh_private_key"

ARG env_name="env"
ENV env_name="$env_name"

# Authorize github ssh
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add ssh keys
RUN echo "$ssh_private_key" > /root/.ssh/id_ed25519 && \
    chmod 600 /root/.ssh/id_ed25519

ARG function_dir="/app"
ENV function_dir="$function_dir"

RUN mkdir -p "$function_dir"

# create app directory
WORKDIR "$function_dir"

# Create the environment
RUN mkdir -p envs
COPY envs/environment_linux.yml envs
RUN conda env create --prefix "envs/$env_name" --file envs/environment_linux.yml

# everything below is not cached by docker
ARG cache_bust
RUN test -n "$cache_bust"

# install pip dependencies
COPY envs/requirements.txt envs
RUN "envs/$env_name/bin/pip" install --force-reinstall --no-cache-dir -r envs/requirements.txt

# Copy app
COPY dist .

# Remove SSH keys
RUN rm -rf /root/.ssh/

# run application
WORKDIR "$function_dir/src"
ENTRYPOINT "$function_dir/envs/$env_name/bin/python" -m awslambdaric main.lambda_handler
