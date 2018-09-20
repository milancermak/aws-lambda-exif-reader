#!/bin/bash
set -eu

readonly DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly INFRASTRUCTURE_DIR="$DIR/../infrastructure"

EXIT_STATUS=0

find $INFRASTRUCTURE_DIR -name '*.yml' -print0 | xargs -0 -n1 cfn-lint --template || EXIT_STATUS=$?

exit $EXIT_STATUS
