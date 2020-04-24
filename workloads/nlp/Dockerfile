FROM ubuntu:bionic

RUN apt update --yes && \
  apt install --yes python3 && \
  apt install --yes python3-pip && \
  apt-get --yes install libboost-dev libboost-program-options-dev libboost-system-dev libboost-thread-dev libboost-math-dev libboost-test-dev libboost-python-dev zlib1g-dev cmake

RUN pip3 install numpy pandas joblib sklearn gensim vowpalwabbit

COPY src /nlp_example/src
COPY input /nlp_example/input
COPY run.sh /nlp_example/run.sh

WORKDIR /nlp_example

CMD ./run.sh
