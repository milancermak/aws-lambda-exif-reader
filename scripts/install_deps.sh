#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
# set -o xtrace

# installs all python libraries

readonly DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly PIP_CACHE=${PIP_CACHE:-$DIR/../pip_cache}

if [[ ! -d $PIP_CACHE ]]; then
    mkdir $PIP_CACHE
fi

find ${DIR}/.. -name 'requirements*.txt' -exec pip install -r '{}' --cache-dir ${PIP_CACHE} \;
