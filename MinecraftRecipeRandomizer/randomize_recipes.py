#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import random
import io
import zipfile
import json
import sys
import argparse


# In[2]:

parser = argparse.ArgumentParser(
	description='Modless Recipe Randomizer for 1.14'
)

parser.add_argument("--seed", type=int, default=random.randrange(sys.maxsize), help="sets seed for datapack")
parser.add_argument("--hard", action = "store_const", const=True, default=False, help="disables starter recipes")

args = parser.parse_args()

seed = args.seed
hard = args.hard

random.seed(seed)
datapack_name = 'random_recipes_{}'.format(seed)


datapack_desc = 'Recipe Randomizer, Seed: {}'.format(seed)

if hard:
	datapack_name += "_hard"
	datapack_desc += ", Hard Mode"
	

datapack_filename = datapack_name + '.zip'


# In[3]:


print('Generating datapack...')
file_list = []
remaining = []

file_dict = {}

for dirpath, dirnames, filenames in os.walk('recipes'):
	if dirpath != "recipes\starter_recipes":
		for filename in filenames:	
			file_list.append(os.path.join(dirpath, filename))
			remaining.append(os.path.join(dirpath, filename))


if not hard:				
	for dirpath, dirnames, filenames in os.walk('recipes\starter_recipes'):
		for filename in filenames:
			file = os.path.join(dirpath, filename)
			file_dict[file] = json.load(open(file, "r"))
		
for file in file_list:
	i = random.randint(0, len(remaining)-1)
    
	file1 = open(file, "r")
	file2 = open(remaining[i], "r")
    
	f1 = json.load(file1)
	f2 = json.load(file2)
    
	file1.close()
	file2.close()
    
	
	if type(f1["result"]) == type(f2["result"]):
		f1["result"] = f2["result"]
	else:
		try:
			f1["result"] = f2["result"]["item"]
		except:
			f1["result"]["item"] = f2["result"]
    
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

