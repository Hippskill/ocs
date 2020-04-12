FROM gcc:latest as build
COPY src /factorize_example/src

WORKDIR /factorize_example
RUN rm -rf build && mkdir build && g++ -O2 -lpthread -std=c++1z src/main.cpp -o build/factorize

FROM ubuntu:latest

RUN apt --yes update && apt install --yes python3

COPY src /factorize_example/src
COPY run.sh /factorize_example/run.sh

WORKDIR /factorize_example

COPY --from=build /factorize_example/build/factorize .
CMD ./run.sh
