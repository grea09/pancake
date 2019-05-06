#!/usr/bin/python3

import sys
import getopt
import ruamel.yaml

yaml = ruamel.yaml.YAML()

data = {}

optlist, args = getopt.getopt(sys.argv[1:], 'o:')
print(args)
print(optlist)

for f in args:
  print(f)
  with open(str(f)) as fp:
    data = {**data, **(yaml.load(fp))}
yaml.dump(data,file(optlist['-o'], 'w'))

