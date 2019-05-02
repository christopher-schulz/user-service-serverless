#!/usr/bin/env bash

set -e
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 STAGE" >&2
    echo "Example: $0 dev" >&2
    exit 1
fi

STAGE=$1

pipenv lock -r > requirements.txt

sls deploy --stage $1

rm requirements.txt
