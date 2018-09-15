#!/usr/bin/env bash

function print_green () {
  printf "\033[92m${1}\033[0m\n"
}

function print_blue () {
  printf "\033[94m${1}\033[0m\n"
}

PROJECT_PATH=$(dirname $(dirname ${0}))

PIP_BIN=$(which pip)

if [ ! ${?} -eq 0 ]; then
  print_blue 'Installing "pip"...'
  curl https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
  python /tmp/get-pip.py

  PIP_BIN=$(which pip)
fi

which flake8 > /dev/null

if [ ! ${?} -eq 0 ]; then
  print_blue 'Installing "flake8"...'
  ${PIP_BIN} install flake8 flake8-commas
fi

cp ./hooks/pre-commit ./.git/hooks

DOT_ENV=${PROJECT_PATH}/.env

if [ ! -f ${DOT_ENV} ]; then
  print_blue 'Creating ".env" file...'
  echo "SECRET_KEY=$(python ${PROJECT_PATH}/scripts/generate_secret_key.py)" > ${DOT_ENV}
fi

print_green 'All good!'
