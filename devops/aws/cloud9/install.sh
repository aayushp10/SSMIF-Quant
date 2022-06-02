#!/bin/sh

set -e

rm README.md

sudo apt-get -y update && sudo apt-get -y upgrade
sudo apt-get install -y libbz2-dev lzma liblzma-dev default-jdk scala

# puppeteer dependencies
sudo apt-get install -y ca-certificates fonts-liberation gconf-service libappindicator1 \
    libasound2 libatk-bridge2.0-0 libatk1.0-0 libc6 libcairo2 libcups2 libdbus-1-3 \
    libexpat1 libfontconfig1 libgbm1 libgcc1 libgconf-2-4 libgdk-pixbuf2.0-0 libglib2.0-0 \
    libgtk-3-0 libnspr4 libnss3 libpango-1.0-0 libpangocairo-1.0-0 libstdc++6 libx11-6 \
    libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 libxext6 libxfixes3 libxi6 \
    libxrandr2 libxrender1 libxss1 libxtst6 lsb-release wget xdg-utils

# create ssh key for ci/cd account
# see https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

ssh-keygen -t ed25519 -C "ssmifquant@gmail.com"
cat ~/.ssh/id_ed25519.pub

# from https://stackoverflow.com/a/13364116/8623391
ssh-keyscan -t rsa github.com >> ~/.ssh/known_hosts

# git lfs
# https://github.com/git-lfs/git-lfs/wiki/Installation
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
git lfs install

git clone git@github.com:SSMIF-Quant/quant.git ssmif

cd ssmif
current_dir="$pwd"
ln -s "$pwd/aws/cloud9/.profile" ~
cd -

# before next commands, you need to resize the volume in ec2, making it 30gb or something

wget https://repo.anaconda.com/archive/Anaconda3-2020.11-Linux-x86_64.sh

bash Anaconda3-*.sh
conda config --set auto_activate_base false

# install node
# from https://github.com/nodesource/distributions/blob/master/README.md
curl -sL https://deb.nodesource.com/setup_15.x | sudo -E bash -
sudo apt-get install -y nodejs
nvm install 15
nvm alias default 15
npm install -g yarn

git config --global core.editor vim
git config core.editor vim
git config --global user.name "ssmif"
git config user.name "ssmif"
git config --global user.email "ssmifquant@gmail.com"
git config user.email "ssmifquant@gmail.com"

# pip environment
# from https://github.com/pyenv/pyenv-installer
curl https://pyenv.run | bash

# https://pipenv.pypa.io/en/latest/#install-pipenv-today
pip install --user pipenv

cd ssmif

git checkout overhaul

# install packages
yarn install

cd scripts/install
./git-secrets.sh
cd -

# spark

wget https://dlcdn.apache.org/spark/spark-3.1.2/spark-3.1.2-bin-hadoop3.2.tgz
tar xvf spark-*
sudo mv spark-3.1.2-bin-hadoop3.2 /opt/spark
cp /opt/spark/conf/spark-defaults.conf.template /opt/spark/conf/spark-defaults.conf
vim /opt/spark/conf/spark-defaults.conf # add configuration parameters
# like spark.history.fs.logDirectory and spark.eventLog.dir

# eksctl
curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
sudo mv /tmp/eksctl /usr/local/bin

# terraform
# from https://learn.hashicorp.com/tutorials/terraform/install-cli
curl -fsSL https://apt.releases.hashicorp.com/gpg | sudo apt-key add -
sudo apt-add-repository "deb [arch=amd64] https://apt.releases.hashicorp.com $(lsb_release -cs) main"
sudo apt-get update && sudo apt-get install terraform
terraform -install-autocomplete

# kubectl
# from https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/
sudo apt-get install -y apt-transport-https ca-certificates curl
sudo curl -fsSLo /usr/share/keyrings/kubernetes-archive-keyring.gpg https://packages.cloud.google.com/apt/doc/apt-key.gpg
echo "deb [signed-by=/usr/share/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
sudo apt-get update
sudo apt-get install -y kubelet kubeadm kubectl
sudo apt-mark hold kubelet kubeadm kubectl

# create new terminal now

# create shared terminal
# see https://stackoverflow.com/a/25206998/8623391
tmux display-message -p '#S'
# tmux switch -t <id>
