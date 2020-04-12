FROM gcc:latest as build
COPY src /knapsack_example/src

WORKDIR /knapsack_example
RUN rm -rf build && mkdir build && g++ -O2 -lpthread -std=c++1z src/main.cpp -o build/knapsack

FROM ubuntu:latest

COPY src /knapsack_example/src
COPY run.sh /knapsack_example/run.sh

WORKDIR /knapsack_example

COPY --from=build /knapsack_example/build/knapsack .
CMD ./run.sh
