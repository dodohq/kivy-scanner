import os
import json

STORE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')) 
path = STORE_DIR + '/qwerty.json'
with open(path) as f:   
    data = json.load(f)

l = ['title', 'description', 'cols', 'rows' ]
for i in l:   
    data.pop(i)

null = None
for i in data:
    for j in i:
        j[1] = unicode(None)

with open(path, 'w') as f:
    f.write(json.dumps(data, indent=2, sort_keys=True))
