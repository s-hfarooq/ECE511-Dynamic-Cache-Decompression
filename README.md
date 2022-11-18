# ECE511-Dynamic-Cache-Decompression

UIUC ECE 511 Fall 2022 Research Project

Hassan Farooq (hfaroo9), Spenser Fong (sfong5), Timothy Vitkin (tvitkin2)

## Compile gem5

### Install required packages

    sudo apt install build-essential git m4 scons zlib1g zlib1g-dev \
    libprotobuf-dev protobuf-compiler libprotoc-dev libgoogle-perftools-dev \
    python3-dev python-is-python3 libboost-all-dev pkg-config


Install pydot with `python3 -m pip install pydot`

`sudo apt install graphviz`

Install scons with `python3 -m pip install scons==3.1.2`


### Compile

    scons build/X86/gem5.opt

and 

    scons build/RISCV/gem5.opt