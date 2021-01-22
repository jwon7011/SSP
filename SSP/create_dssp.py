import sys,os, time,string
common_files = "..\\common_files"
sys.path.append(common_files)

from fopen import *
#pdb_dir = fopen("absolute_path_of_pdb_files")[0].strip()


#if os.path.exists("..\\pdb_files\\dsspout\\") == False:
#   os.mkdir("..\\pdb_files\\dsspout\\")

#pdblist = [f for f in os.listdir("..\\pdb_files\\") if f[-3:] == "ent"]

#erfile = open("C:\\xampp\\htdocs\\python\\Errors\\error.log","w")

pdblist = []
if len(pdblist) == 0:
   pdblist.append(sys.argv[1])

for pdb in pdblist:
   f = open(pdb)
   num_mod = 1
   for line in f:
       if line[0:5] == "MODEL":
            num_mod += 1
   i = 1
   f.close()
   print num_mod
   if num_mod == 1:
      os.system("D:\\xampp\\htdocs\\python\\SSP\\DSSPCMBI.EXE "+pdb+" > "+sys.argv[2]+os.path.basename(pdb).split(".")[0]+".dssp")
      print pdb.split(".")[0]+".dssp created"
   else:
      mod_num = 0
      curmodel = 0
      last_mod = -1
      while i < num_mod:
         f = open(pdb,'r')
         o = open(".\\tmp.pdb",'w')
         inmodel = 0
         endmodel = 0
         for line in f:
             if endmodel:
                break
             if line[0:5] == "MODEL":
                curmodel = int(line[6:].strip())
                #print curmodel
                inmodel = 1
             if (last_mod == -1 or curmodel > last_mod) and inmodel:
                o.write(line)
                if line[0:6] == "ENDMDL":
                   endmodel = 1
                   #print last_mod
                   last_mod = curmodel
             if not(inmodel):
                o.write(line)
         o.close()
         f.close()
         os.system("D:\\xampp\\htdocs\\python\\SSP\\DSSPCMBI.EXE "+".\\tmp.pdb"+" > "+sys.argv[2]+os.path.basename(pdb).split(".")[0]+"_"+str(curmodel)+".dssp")
         os.system("del /Q .\\tmp.pdb")
         #erfile.write(sys.argv[2]+os.path.basename(pdb).split(".")[0]+"_"+str(i)+".dssp created")
         i = i +1

