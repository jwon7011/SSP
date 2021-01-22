
###############################################################################
# Program name: linesplit.py
# Version 2
# 
# Date: 5 July 2005
#
# Originally written for Bryan Schmidt, Centre for Vascular Research
#
# Requirements: pdb_distance3a.py, calc.py
#
# Purpose: Used by pdb_distance3a.py to extract the information from
#          the ATOM and SSBOND lines in PDB files.
#
# Acknowledgements: Kenneth Chan
#
###############################################################################

import string

# extracts data from ATOM line

def atomsplit(line):
   if len(line) < 54:
      #print "linesplit.py: PDB File Error - ATOM line too short, should be at least 54 characters"
      return []
   else:
      #return [line[0:6],line[6:11],line[12:16],line[16],line[17:20],line[21],line[22:26],line[26],line[30:38],line[38:46],line[46:54]]
      return [line[12:16].strip(),line[17:20],line[21]+line[22:26].strip(),line[30:38],line[38:46],line[46:54]]
      #[atomname,aminoacid name, chain id+ res no, x,y,z], 6 items in all

# extracts data from SSBOND line
      
def ssbondsplit(line):
   if len(line) < 35:
      #print "linesplit.py: PDB File Error - SSBOND line too short, should be at least 35 characters"
      return []
   else:
      #return [line[0:6],line[7:10],line[11:14],line[15],line[17:21],line[25:28],line[29],line[31:35]]
      return [line[15]+line[17:21].strip(),line[29]+line[31:35].strip()]

def sheetsplit(line):
   if len(line) < 37:
      #print "linesplit.py: PDB File Error - SHEET line too short, should be at least 36 characters"
      return []
   else:
      return [line[22:26].strip(),line[33:37].strip()] # [initial residue number, terminal residue number]

def headersplit(line):
   if len(line) < 65:
      #print "linesplit.py: PDB File Error - HEADER line too short, should be at least 65 characters"
      return []
   else:
      return [line[10:49].strip(), line[62:66].strip()]
   