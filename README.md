# SSP (Disulfide Bond Analysis Tool)

Wong and Hogg (2010) **Analysis of disulfide bonds in protein structures.** _J Thromb Haemost_ 8:2345 (https://doi.org/10.1111/j.1538-7836.2010.03894.x)

This repository contains the SSP (disulfide bond analysis tool) python web application, the webpage and a difficult to find precompile apache module for mod_wsgi.  
  
**Requirements:**
- Python 2.7
- XAMPP 32 bit

## Setting up SSP tool
1. Create SSP folder (for example to C:\htdocs\SSP).
2. Create directories:
 - ../Analysis
 - ../Errors
 - ../upload
 - ../../pdb_files
 - ../../pdb_files/dsspout 
   
Other directory locations can be used but more paths would have to be modified in the scripts.  
Paths in scripts and files that have to be modified include:
 - absolute_path_of_dssp_files
 - absolute_path_of_pdb_files
 - create_dssp.py - line 30, 58
 - analysis.py - line 31
 - index.wsgi - line 5, 108, 146, 407, 422, 536
 - run.py - line 18, 33, 38, 59, 106, 107, 234

3. Install Python2.7 (32 bit)
4. pip2 install pyExcelerator
5. Install wget for windows (http://gnuwin32.sourceforge.net/packages/wget.htm). Make sure that it is accessible from the command prompt.
6. Install 7zip (https://www.7-zip.org/download.html). Make sure 7z.exe is accessible from the command prompt
7. run UpdatePDB2.bat from a command prompt (this will take a while)
8. run run_all.bat from a command prompt (this will take a hour or more on the first run). It is possible that it doesn't run to completion because it found some errors in a PDB file. This could be due to a corrupt download in the last step or a real invalid PDB file. For the latter, the file has to be removed from the PDB directory. This can be added to the top of the run_all.bat file, a copy of examples are already there. If you get a message that the task has been completed successfully then it means the SSP tool is setup correctly.

## Setting SSP up to run from apache
9. Install xampp (32 bit). The lastest version with 32 bit should be 7.3.2 (https://sourceforge.net/projects/xampp/files/XAMPP%20Windows/7.3.2/)
10. Install VC9 for python (https://download.microsoft.com/download/7/9/6/796EF2E4-801B-4FC4-AB28-B59FBF6D907B/VCForPython27.msi)
11. pip2 install mod_wsgi (open command prompt as Administrator and type "pip install mod-wsgi")
12. Copy mod_wsgi-py27-VC9.so from Apache24-win32-VC9 in mod_wsgi-windows-4.4.12.tar.gz (included in the SSP zip package) to apache modules folder (i.e. X:\xampp\modules).
13. setup apache httpd.conf to load mod_wsgi and access appropriate directories (see example included in SSP zip package).
14. Start up apache. Should be able to access the SSP tool from a browser using https://localhost/SSP

## Setting up SSP webpage
15. Unpack disulfideanalysis (for example to C:\htdocs\disulfideanalyis).
16. Change URL path to point to SSP web tool in search.html line 56

## Setting up Windows task scheduler
17. Add tasks to run once per month: SSP\updatePDB2.bat, then ~1 hour later SSP\run_all.bat, then ~2 hours later disulfide_analysis\task_schedular
