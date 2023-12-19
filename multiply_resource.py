import re
from pathlib import Path
from os import listdir
from os.path import isfile, join, expanduser
from functools import partial
import os
import shutil
from collections.abc import Callable

mod = '2880089689 Victorian Flavor Mod'

vic3_path = Path(expanduser(Path('~/Documents/Paradox Interactive/Victoria 3')))
path = vic3_path / 'mod' / mod / "map_data/state_regions/"
backup_path = vic3_path / 'backup' / mod / "map_data/state_regions/"

multiply_dict = {'bg_logging': 1.7}
def multiply_resource_count(to_multiply_dict: dict[str, float]=multiply_dict, default=1) -> Callable[[str, str], str]:
    def func(original_val: str, resource_name: str) -> str:
        to_multiply = default
        if resource_name in to_multiply_dict: to_multiply = to_multiply_dict[resource_name]
        return str(int(int(original_val)*to_multiply))
    return func
    
def modify_resource_count(text, func: Callable[[str, str], str]=multiply_resource_count(), capped=True):
    def replace_resources(match):
        word = match.group(0)

        mod = re.sub(r'(\s+)(\w+)( = )(\d+)', lambda x: x.group(1)+x.group(2)+x.group(3)+func(x.group(4), x.group(2)), word)

        return mod
    r1 = re.compile(r"capped_resources = {(?:\n\s+\w+ = \d+)+\n\s+}")
    
    if capped: text = r1.sub(partial(replace_resources), text)
    r2 = re.compile(r'(resource = {\n\s+type = "(\w+)"\n\s+undiscovered_amount = )(\d+)(\n\s+})')
    text = r2.sub(lambda x: x.group(1)+func(x.group(3), x.group(2))+x.group(4), text)
    return text

mined_resources = ['bg_coal_mining', 'bg_logging', "bg_oil_extraction", 'bg_iron_mining', 'bg_fishing', 'bg_sulfur_mining', 'bg_lead_mining']
def add_resources_to_discover(text):
    def replace_resources(match):
        word = match.group(1)

        resources = [(submatch.group(1), submatch.group(2)) \
         for submatch in re.finditer(r'\s+(\w+) = (\d+)', word) \
           if submatch.group(1) in mined_resources]

        #print(resources)
        output = match.group(0)
        for resource in resources:
            st = f"""\tresource = {{\n""" + \
                f"""\t\ttype = \"{resource[0]}\"\n""" + \
                f"""\t\tundiscovered_amount = {resource[1]}\n""" + \
                """\t}\n"""
            output = output + st

        return output
    r1 = re.compile(r"capped_resources = {\n((?:\s+\w+ = \d+\n\s+)+)}\n")
    #r1 = re.compile(r"STATE_\w+ = {[\w\W]+capped_resources = {\n((?:\s+\w+ = \d+\n\s+)+)}\n")
    #r1 = re.compile(r"STATE_\s+capped_resources = {(\n\s+\w+ = \d++\n\s+)+}")
    
    text = r1.sub(partial(replace_resources), text)
    return text

if not os.path.exists(vic3_path):
    raise Exception("Victoria 3 directory not found")

isExist = os.path.exists(backup_path)
if not isExist:
    #os.makedirs(backup_path)
    shutil.copytree(path, backup_path)


shutil.rmtree(path)
shutil.copytree(backup_path, path)

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
for filepath in onlyfiles:
    if filepath == "99_seas.txt": continue
    with open(path/filepath, 'r') as file:
        text = file.read()

    text = modify_resource_count(text, capped=True)
    text = add_resources_to_discover(text)

    with open(path/filepath, 'w') as file:
        file.write(text)
    #with open("./test.txt", 'w') as file:
    #     file.write(text)