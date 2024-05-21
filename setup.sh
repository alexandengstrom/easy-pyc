#!/bin/bash

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

chmod +x "$PROJECT_DIR/epyc"

if [[ ":$PATH:" != *":$PROJECT_DIR:"* ]]; then
    echo "export PATH=\"\$PATH:$PROJECT_DIR\"" >> ~/.bashrc
fi