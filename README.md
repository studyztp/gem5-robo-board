# MCU Board Model in gem5

- demo-board
  - contains the se-board that demonstracting a look-alike stm32g4.
- docker-image
  - contains the Dockerfile that builds a docker image for entobench and gem5.
- ento-bench
- gem5
- simple-test
  - contains simple tests for testing the demo board.

# gem5 mini tutorial commands:
commands to ssh and setup the server:
```
ssh [NetID]@brg-rhel8.ece.cornell.edu
source setup-brg.sh 
```
commands for the tutorial experiment
```
module load graphviz/13.1.2 gem5-stable-all/v25.0.0.1 arm-none-eabi/14.3.rel1 

git clone --recurse-submodules --branch gem5-tutorial https://github.com/studyztp/gem5-robo-board.git 
cd gem5-robo-board/ento-bench

cmake -S ${PWD} -B ${PWD}/build -DCMAKE_TOOLCHAIN_FILE=${PWD}/gem5-cmake/arm-gem5.cmake 
cmake --build build --parallel

gem5.opt -re -d cortex-m4-m5out ../demo-board/se_board.py --binary build/benchmark/example/bin/bench-example --processor cortex-m4
gem5.opt -re -d simple-OOO-m5out ../demo-board/se_board.py --binary build/benchmark/example/bin/bench-example --processor simple-OOO
``` 
