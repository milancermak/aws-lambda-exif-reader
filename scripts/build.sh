#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace

readonly DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SRCDIR=${DIR}/../src
readonly COREDIR=${SRCDIR}/core
readonly PIP_CACHE=${PIP_CACHE:-$DIR/../pip_cache}

# TODO: make sure this works

# remove __pycache__ dirs
find ${SRCDIR} -type d -name '__pycache__' -exec rm -r '{}' +

# prepare every function for packaging
for FUNCDIR in ${SRCDIR}/functions/*; do
    echo "Preparing package for `basename ${FUNCDIR}`"

    # copy over core dependencies
    if [[ -L ${FUNCDIR}/core ]]; then
        rm ${FUNCDIR}/core
    fi
    cp -r ${COREDIR} ${FUNCDIR}

    # install function's dependencies (alongside core's)
    if [[ -e ${FUNCDIR}/requirements.txt ]]; then
        pip install --upgrade \
            --requirement ${FUNCDIR}/requirements.txt \
            --target ${FUNCDIR}/lib \
            --cache-dir ${PIP_CACHE}
    fi
done
