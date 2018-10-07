#!/bin/bash

# Initialize our venv if it wasn't already setup
if [ ! -f venv/bin/python ]; then
  python3 "$1" init
fi

venv/bin/python "$@"
