

import sys, time, os, string
#common_files = "./common_files"
#sys.path.append(common_files)

##from helix import *
##from bsheet import *
##from turn import *
## dssp webpage http://cubic.bioc.columbia.edu/services/DSSPcont/DSSPcont.html

from fopen import *
from cysteine import *
from pyExcelerator import *


#Special chars : Added by Anushi
var_angstrom = u'\u212B'
var_alpha = u'\u03B1'
superscript_2 = u"\u00B2"



spaceandcaps = ". "+string.letters[26:]
font0 = Font()
font0.bold = True
style0 = XFStyle()
style0.font = font0


pdb_dir = fopen("D:\\xampp\\htdocs\\python\\SSP\\absolute_path_of_pdb_files")[0].strip()                ## EDIT
#pdb_dir = "..\\pdb_files\\"
#dssp_dir = fopen("C:\\xampp\\htdocs\\python\\SSP\\absolute_path_of_dssp_files")[0].strip()

##dsspline = "  #  RESIDUE AA STRUCTURE BP1 BP2  ACC     N-H-->O    O-->H-N    N-H-->O    O-->H-N    TCO  KAPPA ALPHA  PHI   PSI    X-CA   Y-CA   Z-CA "

import calc,math,string

dsspmarker = '  #  RESIDUE AA STRUCTURE BP1 BP2  ACC     N-H-->O    O-->H-N    N-H-->O    O-->H-N    TCO  KAPPA ALPHA  PHI   PSI    X-CA   Y-CA   Z-CA \n'

def run(fnam,book,errorfile,dist=10,histogram={},lys_arg=False,his=False,asp_glu=False,trp=False,phe=False,tyr=False):
    dssp_dir = os.path.dirname(fnam)+"\\dsspout\\"
    list = fopen(fnam)

##    os.system("DSSPCMBI.EXE "+pdb_dir+fnam+" > out")
##    tempout = fopen("out").index(dsspline)

    special_analysis = lys_arg or his or asp_glu or trp or phe or tyr
    if special_analysis == True:
        charged_aa_list = []
        distance = float(dist)
        if phe or tyr:
            if phe:
                phe_or_tyr = "PHE"
            else:
                phe_or_tyr = "TYR"


    metal_list = ["CU", "FE", "MO", "NI", "MN", "CO", "HG", "CD", "W"]
    ss = {}
    cyss = []
    curmod = []
    metals = []
    results_list = []
    organism = "NOT GIVEN"
#    header = "HEADER NOT GIVEN"
#     filename = "NOT GIVEN"
    try:
        header = list[0][10:50].strip()
        filename = list[0][62:66].strip()
    except IndexError:
        header = "HEADER NOT GIVEN"
        filename = "NOT GIVEN"
        
    expdta = "EXPDATA NOT GIVEN"
    resolution = "NOT GIVEN"
    rfactor = "NOT GIVEN"
    compound = "COMPOUND NOT GIVEN"
    compound_prev = "NOT GIVEN"
    
#     for line in list[1:15]:
#         if line[0:10] == "COMPND    ":
#             compound = line[10:]
#         elif line[0:19] == "COMPND   2 MOLECULE":
#             compound_prev = line[20:]
#             compound = compound_prev[:-1]
############################################################
# Secondary structure information
##    helices   = helix()
##    bsheets   = bsheet()
##    turns     = turn()
############################################################
#Stores information from pdb file into memory
    num_mod = 0
    exptype = 0
    newincys = 0
    curatom = 0
    lastatom = -1
    mod_list = []
    for line in list[1:]:
        if line[0:4] == "ATOM":
            curatom = int(line[23:26].strip())
            if lys_arg == True:
                if line[17:20] == "ARG" and line[13:15] == "NH":
                    charged_aa_list.append(line)
                elif line[17:20] == "LYS" and line[13:15] == "NZ":
                    charged_aa_list.append(line)
            # change this to elif if we don't want simultaneous running of different analyses
            elif his == True:
                if line[17:20] == "HIS" and line[13:16] == "ND1":
                    charged_aa_list.append(line)
                elif line[17:20] == "HIS" and line[13:16] == "NE2":
                    charged_aa_list.append(line)
            # change this to elif if we don't want simultaneous running of different analyses
            elif asp_glu == True:
                if line[17:20] == "ASP" and line[13:15] == "OD":
                    charged_aa_list.append(line)
                elif line[17:20] == "GLU" and line[13:15] == "OE":
                    charged_aa_list.append(line)
            elif trp == True:
                if line[17:20] == "TRP" and line[13:15] == "CZ":
                    charged_aa_list.append(line)
                elif line[17:20] == "TRP" and line[13:16] == "CH2":
                    charged_aa_list.append(line)
                elif line[17:20] == "TRP" and line[13:16] == "CE3":
                    charged_aa_list.append(line)
            elif phe or tyr:
                if line[17:20] == phe_or_tyr and line[13:15] == "CD":
                    charged_aa_list.append(line)
                elif line[17:20] == phe_or_tyr and line[13:15]== "CE":
                    charged_aa_list.append(line)
                elif line[17:20] == phe_or_tyr and line[13:15] == "CZ":
                    charged_aa_list.append(line)


                    
            # we are looking for OD1 and OD2 for ARG and OE1 and OE2 for GLU...

            if line[17:20] == "CYS":
                cyss.append(line)
                if not(newincys):
                   if len(mod_list) == 0:
                      curmod.append(num_mod)
                   else:
                      curmod.append(mod_list[len(mod_list)-1])
                   newincys = 1
                   lastatom = curatom
            if curatom != lastatom:
                lastatom = curatom
                newincys = 0
##        elif line[:5] == "HELIX":
##            helices.addhelix(line)
##        elif line[:5] == "SHEET":
##            bsheets.addsheet(line)
##        elif line[:4] == "TURN":
##            turns.addturn(line)
        elif line[0:5] == "MODEL":
            num_mod += 1
            mod_list.append(int(line[6:].strip()))
        elif line[0:6] == "SSBOND":
            ss[line] = []
#        elif line[0:6] == "HEADER":
#            header = line[10:50].strip()
#            filename = line[62:66].strip()
        elif line[0:6] == "SOURCE" and line.find("ORGANISM_SCIENTIFIC") <> -1 and organism=="NOT GIVEN":
             organism = line[32:].strip()[:-1]
        elif line[0:6] == "EXPDTA":
            expdta = line[10:70].strip() 
        elif line[0:21] == "REMARK   2 RESOLUTION" and expdta[0:5] == "X-RAY":
            resolution = line[22:27].strip()
        elif line[0:47] == "REMARK   3   FREE R VALUE                     :":
            rfactor = line[48:].strip()
        elif line[0:10] == "COMPND    ":
            compound = line[10:]
        elif line[0:19] == "COMPND   2 MOLECULE":
            compound_prev = line[20:]
            compound = compound_prev[:-1]

############################################################
# decide which sheet to save to based on type of experimental data

    if expdta.find("NMR") !=-1:
        if num_mod <= 1:
            num_mod = 1
            sheet = book.get_sheet(3)
            #curbook = book[0]
            exptype = 0
        else:
            sheet = book.get_sheet(4)
            #curbook = book[1]
            exptype = 1
    elif expdta.find("X-RAY")!=-1:
            sheet = book.get_sheet(0)
            #curbook = book[2]
            exptype = 2
    else:
            sheet = book.get_sheet(6)
            #curbook = book[3]
            exptype = 3
    #sheet = curbook.get_sheet(0)
    if num_mod == 0:
       num_mod = 1
############################################################

    dssplist = []

    if num_mod == 1 or num_mod == 0:
       dssp = {}
       sstructure = fopen(dssp_dir+ fnam[:-3].split("\\")[-1]+"dssp")
       for l in sstructure:
           dssp[l[5:12].replace(" ","")] = [l[16].replace(" ","0"),l[35:38].strip()]
       dssplist.append(dssp)
    else:
       for i in mod_list:
         dssp = {}
         try:
             sstructure = fopen(dssp_dir+ fnam[:-3].split("\\")[-1].rstrip(".")+"_"+str(i)+".dssp")
         except:
             errorfile.write("Empty DSSP file for"+fnam)
             print "ERR"
             return
         for l in sstructure:
             dssp[l[5:12].replace(" ","")] = [l[16].replace(" ","0"),l[35:38].strip()]
         dssplist.append(dssp)
    if len(dssplist) == 0:
       errorfile.write("Empty DSSP file for"+fnam)
       return
# sorts out the cysteines
    cysdict = {}
    for c in cyss:
        tag = c[21]+c[22:27]
        try:
            cysdict[tag].append(c)
        except KeyError:
            cysdict[tag] = [c]

    expectedCys = len(ss)*2

    finalmod = []
    diff = (len(curmod)/num_mod)-expectedCys
    count = 0
    for i in curmod:
         if count < expectedCys-diff:
           finalmod.append(i)
           count+=1
         if count == expectedCys:
           count=0

    ss_keys = ss.keys()
    #print fnam
    #print len(cyss)

##    fuke = open("blaasdfshelix","a")
##    for xcv in helices.getSerial():
##        fuke.write(str(xcv)+"\n")

    tmp_ss = {}
    a = 0
    for cys in ss_keys:                                                         #Modified 10-9-2008 by JWong
        #print cys
        try:
            #print cys
            tmp_ss[cys] = [cysdict[cys[15]+cys[17:22]], cysdict[cys[29]+cys[31:36]]]
            #print tmp_ss[cys]
            if exptype == 1:
              step1 = len(tmp_ss[cys][0])/num_mod                                  #Step is number of atoms in Cys for the file
              step2 = len(tmp_ss[cys][1])/num_mod
            else:
              step1 = 15
              step2 = 15                                                                       #Only the first 6 atoms are important
            #print str(step1)+" "+str(step2)
            counter1=0
            counter2=0
            while len(tmp_ss[cys][0])>counter1 and len(tmp_ss[cys][1])>counter2:
                  if sum([spaceandcaps.find(l[13])+spaceandcaps.find(l[14]) for l in tmp_ss[cys][0][counter1:counter1+6]+tmp_ss[cys][1][counter2:counter2+6]]) ==158:
                    c=tmp_ss[cys][0]
                    temp = []
                    temp.append(cysteine(c[counter1:counter1+6],
                                     [c[0][21:26],len(c),string.join(c).find("ACYS"),string.join(c).find("BCYS"),string.join(c).find("HA"),string.join(c).find("HB"),string.join(c).find("1CYS"),string.join(c).find("2CYS")],
##                                     helix_=helices.contains(c[0][21],int(c[0][22:27])),
##                                     sheet_=bsheets.contains(c[0][21],int(c[0][22:27])),
##                                     turn_ =turns.contains(c[0][21],int(c[0][22:27]))
                                     ) )
                    c=tmp_ss[cys][1]
                    temp.append(cysteine(c[counter2:counter2+6],
                                     [c[0][21:26],len(c),string.join(c).find("ACYS"),string.join(c).find("BCYS"),string.join(c).find("HA"),string.join(c).find("HB"),string.join(c).find("1CYS"),string.join(c).find("2CYS")],
##                                     helix_=helices.contains(c[0][21],int(c[0][22:27])),
##                                     sheet_=bsheets.contains(c[0][21],int(c[0][22:27])),
##                                     turn_ =turns.contains(c[0][21],int(c[0][22:27]))
                                     ))
                    #temp = [cysteine(c[counter1:counter1+6],
                    #                 [c[0][21:26],len(c),string.join(c).find("ACYS"),string.join(c).find("BCYS"),string.join(c).find("HA"),string.join(c).find("HB"),string.join(c).find("1CYS"),string.join(c).find("2CYS")],
##                  #                   helix_=helices.contains(c[0][21],int(c[0][22:27])),
##                  #                   sheet_=bsheets.contains(c[0][21],int(c[0][22:27])),
##                  #                   turn_ =turns.contains(c[0][21],int(c[0][22:27]))
                    #                 ) for c in tmp_ss[cys]]
##                    blah = helices.contains(ss[cys][0][0][21],int(ss[cys][0][0][22:27]))
##                    if blah != []:
##                        for zz in blah:
##                            fuke.write(str(zz)+"\n")
#                    for cc in temp:
#                        cc.whoami()
#                        cc.debug1()

                    ss[cys].append(temp)
                    #print len(ss[cys])
                  else:
                     #ss.pop(cys)
                     errorfile.write("Error in "+fnam.split("\\")[-1]+": incorrect cysteine description (too many atoms) at: "+ cys[15]+cys[17:21]+"-"+cys[29]+cys[31:35]+". SS bond deleted.\n")
                  counter1+=step1
                  counter2+=step2
            #if len(ss[cys][0])>=6 and len(ss[cys][1])>=6:
            #    if sum([spaceandcaps.find(l[13])+spaceandcaps.find(l[14]) for l in ss[cys][0][:6]+ss[cys][1][:6]]) == 158:
                    #This hash checks the first six atoms for a match, and store iff if there is match.
                    # This is the only place the cysteine constructor is used, store error values in cysteine in the second argument
                    #Put in secondary structure info in cysteine
            #        temp = [cysteine(c[:6],
            #                         [c[0][21:26],len(c),string.join(c).find("ACYS"),string.join(c).find("BCYS"),string.join(c).find("HA"),string.join(c).find("HB"),string.join(c).find("1CYS"),string.join(c).find("2CYS")],
##                                     helix_=helices.contains(c[0][21],int(c[0][22:27])),
##                                     sheet_=bsheets.contains(c[0][21],int(c[0][22:27])),
##                                     turn_ =turns.contains(c[0][21],int(c[0][22:27]))
            #                         ) for c in ss[cys]]
##                    blah = helices.contains(ss[cys][0][0][21],int(ss[cys][0][0][22:27]))
##                    if blah != []:
##                        for zz in blah:
##                            fuke.write(str(zz)+"\n")
#                    for cc in temp:
#                        cc.whoami()
#                        cc.debug1()

            #       ss[cys] = temp
            #    else:
            #        ss.pop(cys)
            #        errorfile.write("Error in "+fnam.split("\\")[-1]+": incorrect cysteine description (too many atoms) at: "+ cys[15]+cys[17:21]+"-"+cys[29]+cys[31:35]+". SS bond deleted.\n")
            #else:
            #    ss.pop(cys)
            #    errorfile.write("Error in "+fnam.split("\\")[-1]+": incomplete cysteine description (too few atoms) at: "+ cys[15]+cys[17:21]+"-"+cys[29]+cys[31:35]+". SS bond deleted.\n")
        except KeyError:
            ss.pop(cys)
            errorfile.write("Error in "+fnam.split("\\")[-1]+": missing cysteine at: "+ cys[15]+cys[17:21]+"-"+cys[29]+cys[31:35]+". SS bond deleted.\n")
    #maybe we can use sheet.set_first_visible_row(x) ?

    #row_num = len(sheet.get_rows())
############################################################
#The following prints the data into an xls file
    cursheet = sheet
    row_num = len(cursheet.get_rows())
    if len(cursheet.get_rows()) >= 65536 and exptype == 1:
       sheet2 = book.get_sheet(5)
       cursheet = sheet2
       row_num = len(cursheet.get_rows())
       print row_num
       if row_num == 0:
         if special_analysis == True:
            for i,item in enumerate(["PDB ID","Header","Compound","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues "+var_angstrom,"Disulfide bond classification","Model number (NMR only, will default to 0 for non NMR data)","amino acid with +/- charge","strand and residue of AA","atom with +/- charge (X)","number of X","strand and residue of cysteine sulfur (Y) considered","distance between Y and X in Angstroms","Irregularities?","Irregularity type"]):
                cursheet.write(0,i,item,style0)
         else:
            for i,item in enumerate(["PDB ID","Header","Compound","Organism","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility, ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues "+var_angstrom,"Disulfide bond classification","Model number (NMR only, will default to 0 for non NMR data)"]):#,"Irregularities?","Irregularity type"]):
                cursheet.write(0,i,item,style0)
         row_num=1
    if len(cursheet.get_rows()) >= 65536 and exptype == 2:
       sheet2 = book.get_sheet(1)
       if len(sheet2.get_rows()) >= 65536:
             sheet2 = book.get_sheet(2)
       cursheet = sheet2
       row_num = len(cursheet.get_rows())
       print row_num
       if row_num == 0:
         if special_analysis == True:
            for i,item in enumerate(["PDB ID","Header","Compound","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility, ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues "+var_angstrom,"Disulfide bond classification","Model number (NMR only, will default to 0 for non NMR data)","amino acid with +/- charge","strand and residue of AA","atom with +/- charge (X)","number of X","strand and residue of cysteine sulfur (Y) considered","distance between Y and X in Angstroms","Irregularities?","Irregularity type"]):
                cursheet.write(0,i,item,style0)
         else:
            for i,item in enumerate(["PDB ID","Header","Compound","Organism","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility, ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues "+var_angstrom,"Disulfide bond classification","Model number (NMR only, will default to 0 for non NMR data)"]):#,"Irregularities?","Irregularity type"]):
                cursheet.write(0,i,item,style0)
         row_num=1
    #print row_num
    if row_num == 0:
        if special_analysis == True:
            for i,item in enumerate(["PDB ID","Header","Compound","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility, ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues "+var_angstrom,"Disulfide bond classification","Model number (NMR only, will default to 0 for non NMR data)","amino acid with +/- charge","strand and residue of AA","atom with +/- charge (X)","number of X","strand and residue of cysteine sulfur (Y) considered","distance between Y and X in Angstroms","Irregularities?","Irregularity type"]):
                cursheet.write(0,i,item,style0)
        else:
            for i,item in enumerate(["PDB ID","Header","Compound","Organism","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility, ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues, "+var_angstrom,"Disulfide bond classification","Model number (NMR only, will default to 0 for non NMR data)"]):#,"Irregularities?","Irregularity type"]):
                cursheet.write(0,i,item,style0)
        row_num=1
#    print ss[ss.keys()[0]]
##    sstruct = lambda hx,bs,tn : [t for i,t in zip([hx,bs,tn],["helix","sheet","turn"]) if i == True]
    a = 0
    count = 0
    lastpos = 0
    m = 0
    for cys in ss.keys():
          try:
            a = 0
            for mods in ss[cys]:
              if num_mod > 1:
                 #print str(len(curmod))+" "+str(a)+" "+str(len(ss))
                 if a*len(ss) < len(curmod):
                    m = curmod[a*len(ss)]
              if lastpos == len(ss):
                 lastpos = 0
                 count+=1
              lastpos+=1
              ss_struct_1,ss_solvent_acc_1 = dssplist[count][mods[0].residue.strip()+mods[0].strand.strip()]
              ss_struct_2,ss_solvent_acc_2 = dssplist[count][mods[-1].residue.strip()+mods[-1].strand.strip()]
              ss_struct_temp               = [ss_struct_1,ss_struct_2]
              ss_struct_temp.sort()  # sort to eliminate permutation for histogram
              ss_struct_both               = string.join(ss_struct_temp,"")
              if ss_struct_1 == "H":
                 ss_struct_1 = "alpha helix"
              elif ss_struct_1 =="B":
                 ss_struct_1 = "residue in isolated beta-bridge"
              elif ss_struct_1 =="E":
                 ss_struct_1 = "extended strand, participates in beta ladder"
              elif ss_struct_1 == "G":
                 ss_struct_1 = "3-helix (3/10 helix)"
              elif ss_struct_1 == "I":
                 ss_struct_1 = "5 helix (pi helix)"
              elif ss_struct_1 == "T":
                 ss_struct_1 = "hydrogen bonded turn"
              elif ss_struct_1 == "S":
                 ss_struct_1 = "bend"
              else:
                 ss_struct_1 = "loops or irregular"
    
              if ss_struct_2 == "H":
                 ss_struct_2 = "alpha helix"
              elif ss_struct_2 =="B":
                 ss_struct_2 = "residue in isolated beta-bridge"
              elif ss_struct_2 =="E":
                 ss_struct_2 = "extended strand, participates in beta ladder"
              elif ss_struct_2 == "G":
                 ss_struct_2 = "3-helix (3/10 helix)"
              elif ss_struct_2 == "I":
                 ss_struct_2 = "5 helix (pi helix)"
              elif ss_struct_2 == "T":
                 ss_struct_2 = "hydrogen bonded turn"
              elif ss_struct_2 == "S":
                 ss_struct_2 = "bend"
              else:
                 ss_struct_2 = "loops or irregular"
      #        for x in arg_list+lys_list:
      #        for cc in mods:
      #            dst = cc.distance_sq_from_sulfur_to_atom(x)
      #            if dst <= dist**2:
      #                atom_number    = x[6:11].strip()
      #                atom_type      = x[13:16].strip()
      #                aa_type        = x[17:20].strip()
      #                residue        = x[22:27].strip()
      #                strand         = x[20:22].strip()

              # d is the distance between alpha carbons
              d = math.sqrt(calc.distance_sq(mods[0].a_carbon,mods[-1].a_carbon))
              # dss is the distance between sulfur atoms
              dss = math.sqrt(calc.distance_sq(mods[0].sulfur,mods[-1].sulfur))
              # t stores the strain energy and angles
              t = mods[0].distance_to_and_angles(mods[-1])
              strain,angles = t[0],t[-1]

              # Alpha angles 1 and 2 by Anushi
              alpha_angle = mods[0].find_angle(mods[-1])
              alpha_angle_1 = str(alpha_angle[0])
              alpha_angle_2 = str(alpha_angle[1])
              
              # class_ is the type of ssbond
              class_ = calc.classify(angles)
              if special_analysis == True:
                  for pos_atom in charged_aa_list:
                      for cc in mods:
                          dst = cc.distance_sq_from_sulfur_to_atom(pos_atom)
                          if dst <= dist**2:
                              atom_number    = pos_atom[6:11].strip()
                              atom_type      = pos_atom[13:16].strip()
                              aa_type        = pos_atom[17:20].strip()
                              residue        = pos_atom[22:27].strip()
                              strand         = pos_atom[20:22].strip()
  ##                            ss_struct_1    = dssp[mods[0].residue.strip()+mods[0].strand.strip()
  ##                            ss_struct_2    = dssp[mods[-1].residue.strip()+mods[-1].strand.strip()
                              #num_mod = pos+1
                              for i,item in enumerate([l for l in [filename,
                                                                   header,
                                                                   compound,
                                                                   expdta,
                                                                   mods[0].strand,
                                                                   mods[0].residue,
                                                                   ss_struct_1,
                                                                   ss_solvent_acc_1,
  ##                                                                 str(sstruct(mods[0].isHelix,mods[0].isSheet,mods[0].isTurn)),
                                                                   mods[-1].strand,
                                                                   mods[-1].residue,
                                                                   ss_struct_2,
                                                                   ss_solvent_acc_2,
  ##                                                                 str(sstruct(mods[-1].isHelix,mods[-1].isSheet,mods[-1].isTurn)),
                                                                   resolution,rfactor]
                                                                   + angles +
                                                                   [alpha_angle_1,alpha_angle_2]+
                                                                  [strain,d,dss,class_,m]+
                                                                  [aa_type,strand.strip()+" "+residue,
                                                                   atom_type,atom_number,
                                                                   cc.strand_residue().strip(),
                                                                   math.sqrt(dst)]#+
                                                                   #map(str,zip(mods[0].irregularities(),mods[1].irregularities()))
                                                                   
                                                       ]):
                                  cursheet.write(row_num,i,item)
                              row_num +=1
                              a+=2
                              ## stores histogram data
                              try:
                                  histogram[ss_struct_both+class_] = histogram[ss_struct_both+class_] + 1
                              except KeyError:
                                  histogram[ss_struct_both+class_] = 1
              else:
  ##                ss_struct_1    = dssp[mods[0].residue.strip()+mods[0].strand.strip()
  ##                ss_struct_2    = dssp[mods[-1].residue.strip()+mods[-1].strand.strip()
                  #num_mod = pos+1
                  for i,item in enumerate([l for l in [filename,
                                                       header,
                                                       compound,
                                                       organism,
                                                       expdta,
                                                       mods[0].strand,
                                                       mods[0].residue,
                                                       ss_struct_1,
                                                       ss_solvent_acc_1,
  ##                                                     str(sstruct(mods[0].isHelix,mods[0].isSheet,mods[0].isTurn)),
                                                       mods[-1].strand,
                                                       mods[-1].residue,
                                                       ss_struct_2,
                                                       ss_solvent_acc_2,
  ##                                                     str(sstruct(mods[-1].isHelix,mods[-1].isSheet,mods[-1].isTurn)),
                                                       resolution,rfactor]
                                                       + angles +
                                                       [alpha_angle_1,alpha_angle_2]+
                                                      [strain,d,dss,class_,m]#+                                             # ADDED dss for sulfur atom 21-5-2013
                                                      #map(str,zip(mods[0].irregularities(),mods[1].irregularities()))
                                                       
                                           ]):
                      cursheet.write(row_num,i,item)
                  row_num +=1
                  a+=2
                  #print row_num
                  if row_num == 65536 and exptype == 1:
                     sheet2 = book.get_sheet(5)
                     cursheet = sheet2
                     row_num = (cursheet.get_first_visible_row())
                     if row_num == 0:
                          
                       if special_analysis == True:
                          for i,item in enumerate(["PDB ID","Header","Compound","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility, ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues, "+var_angstrom,"Disulfide bond classification","Number of models (NMR only, will default to 0 for non NMR data)","amino acid with +/- charge","strand and residue of AA","atom with +/- charge (X)","number of X","strand and residue of cysteine sulfur (Y) considered","distance between Y and X in Angstroms","Irregularities?","Irregularity type"]):
                              cursheet.write(0,i,item,style0)
                       else:
                          for i,item in enumerate(["PDB ID","Header","Compound","Organism","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility, ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues, "+var_angstrom,"Disulfide bond classification","Number of models (NMR only, will default to 0 for non NMR data)"]):#,"Irregularities?","Irregularity type"]):
                              cursheet.write(0,i,item,style0)
                       row_num=1
                  if row_num == 65536 and exptype == 2:
                     sheet2 = book.get_sheet(1)
                     if len(sheet2.get_rows()) >= 65536:
                           sheet2 = book.get_sheet(2)
                     cursheet = sheet2
                     row_num = (cursheet.get_first_visible_row())
                     if row_num == 0:
                       if special_analysis == True:
                          for i,item in enumerate(["PDB ID","Header","Compound","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility(~Angstroms^2)","Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility(~Angstroms^2)","Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree","Dihedral strain energy, kJ/mol","Distance between alpha-carbon atoms of the Cys residues (Angstroms)","Distance between sulfur atoms of the Cys residues (Angstroms)","Disulfide bond classification","Number of models (NMR only, will default to 0 for non NMR data)","amino acid with +/- charge","strand and residue of AA","atom with +/- charge (X)","number of X","strand and residue of cysteine sulfur (Y) considered","distance between Y and X in Angstroms","Irregularities?","Irregularity type"]):
                              cursheet.write(0,i,item,style0)
                       else:
                          for i,item in enumerate(["PDB ID","Header","Compound","Organism","Experiment","Cys1 chain","Cys1 residue","Cys1 secondary structure","Cys1 solvent accessibility, ~"+var_angstrom+superscript_2,"Cys2 chain","Cys2 residue","Cys2 secondary structure","Cys2 solvent accessibility, ~"+var_angstrom+superscript_2,"Resolution","R-factor","chi1 angle, degree","chi2 angle, degree","chi3 angle, degree","chi2\' angle, degree","chi1\' angle, degree",var_alpha+"1 angle, degree",var_alpha+"2 angle, degree","Dihedral strain energy, kJ/mol","Distance between "+var_alpha+"-carbon atoms of the Cys residues, "+var_angstrom,"Distance between sulfur atoms of the Cys residues "+var_angstrom,"Disulfide bond classification","Model number (NMR only, will default to 0 for non NMR data)"]):#,"Irregularities?","Irregularity type"]):
                              cursheet.write(0,i,item,style0)
                       row_num=1
                  ## stores histogram data
                  try:
                      histogram[ss_struct_both+class_] = histogram[ss_struct_both+class_] + 1
                  except KeyError:
                      histogram[ss_struct_both+class_] = 1
                  except TypeError:
                      errorfile.write("Error in histogram, check "+ss_struct_both+class_+"\n")


          except IndexError:
              errorfile.write("Error in SSBONDS, check "+fnam.split("\\")[-1]+"\n")#,"\noffending strands/residues:",
              #mods[0].whoami(),
              #print len(mods)
          except ZeroDivisionError:
  #            print cys,mods[0].debug1(),mods[1].debug1()
              errorfile.write("Error in SSBOND, two atoms occupy the same coordinate."+fnam.split("\\")[-1]+"\n")#,"\noffending strands/residues:",
              #mods[0].whoami()
              #print len(mods)
          except KeyError:
              errorfile.write("Error in SSBOND label, check "+fnam.split("\\")[-1]+"\n")
    sheet.set_first_visible_row(row_num)
    return histogram

#    book.save("..\\Analyses\\basic_analysis_"+date_+".xls")
