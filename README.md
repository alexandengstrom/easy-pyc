# easy-pyc
EasyPyC is a simple build script designed for small C and C++ projects. It automates the process of compilation, linking process and running the executable without needing to create a Makefile. It will search for source and header files in the current directory and try to figure out how it should be compiled by itself. To make this work, we assume there is only one main function in the current directory. Note that this is not suitable for real projects.

## Setup
To setup the project. First clone the repo:
```bash
git clone git@github.com:alexandengstrom/easy-pyc.git
```
Navigate to the project directory:
```bash
cd easy-pyc
```
Run the setup script:
```bash
bash setup.sh
```

## Usage
After running the setup script, the command `epyc` can be used in the terminal to compile and run C and C++ projects.
