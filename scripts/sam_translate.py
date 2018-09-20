#!/usr/bin/env python

# Based on https://github.com/awslabs/serverless-application-model/blob/master/bin/sam-translate.py

import argparse
import json
import os

import boto3

from samtranslator.public.translator import ManagedPolicyLoader
from samtranslator.translator.transform import transform
from samtranslator.yaml_helper import yaml_parse


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input-file',
                        help='Location of SAM tamplate to transform')
    parser.add_argument('-o', '--output-file',
                        help='Location of resulting Cloudformation template (in JSON format)')
    args = parser.parse_args()

    cwd = os.getcwd()
    input_file_path = os.path.join(cwd, args.input_file)
    output_file_path = os.path.join(cwd, args.output_file)

    return input_file_path, output_file_path

def main():
    input_file_path, output_file_path = parse_arguments()

    with open(input_file_path) as f:
        sam_template = yaml_parse(f)

    iam = boto3.client('iam')
    cloudformation_template = transform(sam_template,
                                        {},
                                        ManagedPolicyLoader(iam))

    with open(output_file_path, 'w') as f:
        f.write(json.dumps(cloudformation_template, indent=2))

    print(f'Wrote transformed Cloudformation template to {output_file_path}')

if __name__ == '__main__':
    main()
