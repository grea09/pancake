#!/usr/bin/python3

import sys
import argparse
import ruamel.yaml

yaml = ruamel.yaml.YAML()

data = {}

parser = argparse.ArgumentParser()
parser.add_argument("inputs", nargs='+', type=str, help="Merged YAML file path")
parser.add_argument("-o", "--output", type=str, help="Merged YAML file path")
args = parser.parse_args()

for f in args.inputs:
  with open(str(f)) as fp:
    data = {**data, **(yaml.load(fp))}
yaml.dump(data,open(args.output, 'w'))

