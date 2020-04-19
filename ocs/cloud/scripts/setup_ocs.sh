#!/bin/bash -e

echo 'echo $GIT_PASSWORD' > .git-askpass
chmod +x .git-askpass

rm -rf ocs || true
GIT_PASSWORD="diqnin-cocxaX-8bykda" GIT_ASKPASS=./.git-askpass git clone https://ocs-bot@github.com/Hippskill/ocs.git

sudo add-apt-repository universe
sudo apt update
sudo apt install --yes python3-pip

pip3 install -r ocs/ocs/cloud/scripts/requirements.txt
