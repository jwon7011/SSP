import sys,os, time,string
common_files = "./common_files"
sys.path.append(common_files)


from fopen import *
pdb_dir = fopen("absolute_path_of_pdb_files")[0].strip()
#pdb_dir = "../pdb_files"

date_ = time.strftime("%d_%b_%Y")
difference = []
myfilesdict = {}
allfilesdict = {}
dead_files = []

try:
   list = fopen("index.html")
except IOError:
  # var = raw_input("The file index.html file was not found. Should we download the pdb index file from rscb servers? Type yes and press enter to continue with the download, type anything else and press enter to abort.\n")
  # if var == "yes":
#      os.system("wget ftp://ftp.rcsb.org/pub/pdb/data/structures/all/pdb/")
      os.system("wget -e use_proxy=yes -e ftp_proxy=infpapxvip.it.unsw.edu.au:8080 ftp://ftp.pdbj.org/pub/pdb/data/structures/all/pdb/")
      list = fopen("index.html")
  # else:
  #    print "You will need to download the index.html file yourself from ftp://ftp.wwpdb.org/pub/pdb/data/structures/all/pdb/ and place the file in this directory. Alternative you can re-run the script.\n"
  #    sys.exit()

#allfiles = [(line,line.split("\"")[1].split("/")[-1][:-2]) for line in list if line.find("a href") != -1 and line.find(".ent") != -1]
#allfiles = []

for line in list:
   if line.find("a href")!=-1 and line.find(".ent")!=-1:
      f_name = line.split("\"")[1].split("/")[-1]
      f_name_ = string.join(f_name.split(".")[:-1],".")
      allfilesdict[f_name_] = line

allfiles = allfilesdict.keys()

# check what files I have
for file in os.listdir(pdb_dir):
   if file.find(".ent")!=-1:
      myfilesdict[file.replace(".Z","").replace(".z","").replace(".gz","")] = 1

# including files listed in the file- files_not_containing_ssbonds
for file_ in fopen("files_not_containing_ssbonds"):
   myfilesdict[file_.replace(".Z","").replace(".z","").replace(".gz","").strip()] = 1

myfiles = myfilesdict.keys()

for file in allfiles:
   try:
      myfilesdict[file]
   except KeyError:
      difference.append(file)

number_of_dead_files = 0
for file in myfiles:
   try:
      allfilesdict[file]
   except KeyError:
      dead_files.append(file)
      number_of_dead_files += 1

# save this to a log file
# also save all comments to log file...
summary = [time.strftime("\nDownloading pdb files on %a %d %b %Y at %H:%M:%S\n"),
    "Summary: \nNumber of .ent files in current directory = "+str(len(myfiles))+"\n",
    "Number of .ent files in rscb repository   = "+str(len(allfiles))+"\n",
    "Number of new .ent files to download      = "+str(len(difference))+"\n",
    "Number of my .ent files which are no longer on the rscb repository = "+str(number_of_dead_files)+"\n",
    "List of my .ent files which are no longer on the rscb repository:\n",
    string.join(dead_files,", ")+"\n"]

fl = open("files.log","a")
for line in summary:
    print line,
    fl.write(line)

fl.close()

fncs = open("files_not_containing_ssbonds","a")
newpdbs = open("new_files_downloaded_on_"+date_,"w")
os.chdir(pdb_dir)

for file in difference:
   ftp_link = allfilesdict[file].split("\"")[1]
   print ftp_link
   os.system("wget "+ftp_link)
   os.system("7z x "+file+".gz")
   #os.system("gunzip "+file+".gz")
   os.system("del "+file+".gz")
   if open(file).read().find("SSBOND")==-1:
      os.system("del "+file)
      print file,"deleted.\n"
      fncs.write(file+"\n")
   else:
      newpdbs.write(file+"\n")
      #os.system("pwd")
      #os.system("\"../S-S Programs/dssp/dsspcmbi\" "+file+" > ./dsspout/"+file.split(".")[0]+".dssp")
      #os.system("\"..\\S-S Programs\\DSSPCMBI.EXE\" "+file+" > .\\dsspout\\"+file.split(".")[0]+".dssp")
      #print file,"saved.\n", file.split(".")[0]+".dssp created"


#   os.system("ls "+file+".Z new")
#   os.system("gunzip "+file+".Z")
