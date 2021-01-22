from fopen import *

pdb_dir = fopen("absolute_path_of_pdb_files")[0].strip()

flist = fopen("pdbaanr")
file  = open("new_files_downloaded_on_pdbaanr","w")

import os

for ff in flist:
    if os.path.exists(pdb_dir+ff.strip()):
        file.write(ff)
