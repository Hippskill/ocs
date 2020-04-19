#!/bin/bash -e

pip3 install -r requirements.txt

echo 'echo $GIT_PASSWORD' > .git-askpass
chmod +x .git-askpass

GIT_PASSWORD="diqnin-cocxaX-8bykda" GIT_ASKPASS=./.git-askpass git clone https://ocs-bot@github.com/Hippskill/ocs.git

