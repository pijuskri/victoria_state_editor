import re
from pathlib import Path
from os import listdir
from os.path import isfile, join, expanduser
from functools import partial

mod = '2880089689 Victorian Flavor Mod'

path = Path(expanduser(Path('~/Documents/Paradox Interactive/Victoria 3/mod'))) / mod / "map_data/state_regions/"

onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
for filepath in onlyfiles:
    if filepath == "99_seas.txt": continue
    with open(path/filepath, 'r') as file:
        text = file.read()

    def capitalize_long(match, length):
        word = match.group(0)
        #print(word)
        mod = re.sub(r'(\s+\w+ = )(\d+)', lambda x: x.group(1)+str(int(int(x.group(2))*1.5)), word)
        #mod = re.findall(r'\s+\w+ = (\d+)', word)
        #print(mod)
        return mod
    r1 = re.compile(r"capped_resources = {(?:\n\s+\w+ = \d+)+\n\s+}")
    
    #print(r.findall(text))
    text = r1.sub(partial(capitalize_long, length=3), text)
    r2 = re.compile(r'(resource = {\n\s+type = [\s\w\n"]+undiscovered_amount = )(\d)+\n\s+}')
    text = r2.sub(lambda x: x.group(1)+str(int(x.group(2))*2), text)

    #with open(path/filepath, 'w') as file:
    #    file.write(text)
    with open("./test.txt", 'w') as file:
         file.write(text)