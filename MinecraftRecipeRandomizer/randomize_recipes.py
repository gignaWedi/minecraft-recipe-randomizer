#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import random
import io
import zipfile
import json
import sys


# In[2]:


seed = random.randrange(sys.maxsize)

if len(sys.argv) >= 2:
    try:
        seed = int(sys.argv[1])
    except Exception:
        print('The seed "{}" is not an integer.'.format(sys.argv[1]))
        exit()

else:
    print('If you want to use a specific randomizer seed integer, use: "python randomize.py <seed>"')
    print('Using Seed: {}'.format(seed))

random.seed(seed)
datapack_name = 'random_recipes_{}'.format(seed)
datapack_desc = 'Recipe Randomizer, Seed: {}'.format(seed)

datapack_filename = datapack_name + '.zip'


# In[3]:


print('Generating datapack...')
file_list = []
remaining = []

for dirpath, dirnames, filenames in os.walk('recipes'):
    for filename in filenames:
        file_list.append(os.path.join(dirpath, filename))
        remaining.append(os.path.join(dirpath, filename))  

file_dict = {}

for file in file_list:
    i = random.randint(0, len(remaining)-1)
    
    file1 = open(file, "r")
    file2 = open(remaining[i], "r")
    
    f1 = json.load(file1)
    f2 = json.load(file2)
    
    file1.close()
    file2.close()
    
    f1["result"] = f2["result"]
    
    file_dict[file] = f1
    
    del remaining[i]


# In[4]:


zipbytes = io.BytesIO()
zip = zipfile.ZipFile(zipbytes, 'w', zipfile.ZIP_DEFLATED, False)


# In[5]:


for f in file_dict:
    zip.writestr(os.path.join("data/minecraft/", f), json.dumps(file_dict[f]))
zip.writestr('pack.mcmeta', json.dumps({'pack':{'pack_format':1, 'description':datapack_desc}}, indent=4))
zip.writestr('data/minecraft/tags/functions/load.json', json.dumps({'values':['{}:reset'.format(datapack_name)]}))
zip.writestr('data/{}/functions/reset.mcfunction'.format(datapack_name), 'tellraw @a ["",{"text":"Recipe randomizer by gignaWedi (inspired by SethBling)","color":"blue"}]')

zip.close()


# In[6]:


seed


# In[7]:


with open(datapack_filename, 'wb') as file:
    file.write(zipbytes.getvalue())
print("\b"*22 + "Done!" + " "*18)
print('Created datapack "{}"'.format(datapack_filename))

