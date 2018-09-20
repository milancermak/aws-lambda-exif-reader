#!/usr/bin/env bash
set -o errexit
set -o pipefail
set -o nounset
#set -o xtrace

USAGE="Usage: $0 SERVICE_NAME [awscli params]"

if [[ $# == 0 ]]; then
    echo "${USAGE}"
    exit 1
fi

readonly SERVICE_NAME=$1; shift;
readonly AWS_CLI_ARGS=$@
readonly DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly INFRADIR=${DIR}/../infrastructure

function create_stack() {
    local stack=${1}
    local fqsn=${SERVICE_NAME}-${stack} # fully qualified stack name

    echo "Creating ${fqsn} stack"
    echo aws cloudformation ${AWS_CLI_ARGS} create-stack --stack-name ${fqsn} --template-body file://${INFRADIR}/${stack}.yml --parameters ParameterKey=Service,ParameterValue=${SERVICE_NAME} --tags Key=Service,Value=${SERVICE_NAME} --on-failure DELETE
    echo aws cloudformation ${AWS_CLI_ARGS} wait stack-create-complete --stack-name ${fqsn}
    echo "Stack created successfully. Outputs:"
    echo aws cloudformation ${AWS_CLI_ARGS} describe-stacks --stack-name ${fqsn} --query 'Stacks[0].Outputs'
}

create_stack essentials
echo ''
create_stack pipeline
