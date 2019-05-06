#!/usr/bin/python3

import sys
import getopt
import ruamel.yaml

yaml = ruamel.yaml.YAML()

data = {'resources':None}

optlist, args = getopt.getopt(sys.argv[1:], 'o')

for f in args:
  with open(str(f)) as fp:
    yaml_data = yaml.load(fp)
    for i in yaml_data['resources']:
      data['resources'].update({i:yaml_data['resources'][i]})

yaml.dump(data,file(optlist['-o'], 'w'))
