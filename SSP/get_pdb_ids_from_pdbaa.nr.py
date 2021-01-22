from fopen import *
import os
pdb_dir = fopen("absolute_path_of_pdb_files")[0].strip()

file = open("new_files_downloaded_on_pdbaa.nr","w")

l = fopen("pdbaa.nr")
for lien in l:
   if lien[0] == ">":
      name =  "pdb"+lien[1:5].lower()+".ent"
      if os.path.exists(pdb_dir+name):
         file.write(name+"\n")

