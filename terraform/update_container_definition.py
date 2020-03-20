import json
import os
from pathlib import Path

cwd=Path(__file__).parent

definition_file=open(cwd.joinpath('service/data-collector-container-definition.json'))
definition=json.load(definition_file)

print(cwd.joinpath('base'))
os.system('cd %s & terraform output -json base > base_outputs.json' %
    cwd.joinpath('base'))

pass