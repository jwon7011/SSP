import sys, time, os, string, random
#common_files = ".\common_files"
#sys.path.append(common_files)

from fopen import *
from cysteine import *
from pyExcelerator import *

font0 = Font()
font0.bold = True
style0 = XFStyle()
style0.font = font0

import analysis
# runs the analysis

def main(analysis_type, command_variables, threshold):
    pdb_dir = fopen("D:\\xampp\\htdocs\\python\\SSP\\absolute_path_of_pdb_files")[0].strip()                   ## EDIT
    dssp_dir = None
    #dssp_dir = "..\\pdb_files\\dsspout\\"
    #pdb_dir = "..\\pdb_files\\"
    x = Workbook()

    x.add_sheet("X-RAY")
    x.add_sheet("X-RAY 2")
    x.add_sheet("X-RAY 3")
    x.add_sheet("NMR averaged model")
    x.add_sheet("NMR multiple models 1")
    x.add_sheet("NMR multiple models 2")
    x.add_sheet("Other")
    date_ = time.strftime("%d%b%Y_%H%M%S")
    write_path = "D:\\xampp\\htdocs\\python\\Analyses\\"+str(int(random.random()*100000000))+"_"+date_+".xls"
    inA = 0
    if len(command_variables) == 2:
       if command_variables[1] == '-A':
          date_ = time.strftime("%d_%b_%Y")
          write_path = "D:\\xampp\\htdocs\\python\\Analyses\\disulfide_analysis_"+date_+".xls"
          command_variables.pop(1)
          inA = 1
    ## EDIT
    #x.save(write_path)
    #x.save("..\\Analyses\\test.xls")

    # file pdb1a5n is missing, possibly because 1a5n does not contain ssbonds (correct)
    #"pdb1tdy.ent","pdb1a5n.ent","pdb1cb6.ent","pdb2ac5.ent"

    #for file in [pdb_dir+name for name in ["pdb1kdg.ent", "pdb1kdk.ent", "pdb1kdm.ent", "pdb1kdq.ent", "pdb1kdu.ent", "pdb1kdv.ent", "pdb1kdy.ent", "pdb1kdz.ent", "pdb1ke1.ent", "pdb1ke2.ent", "pdb1keb.ent", "pdb1keg.ent", "pdb1kek.ent", "pdb1kel.ent", "pdb1kem.ent", "pdb1ken.ent", "pdb1keo.ent", "pdb1kex.ent", "pdb1kf2.ent", "pdb1kf3.ent", "pdb1kf4.ent", "pdb1kf5.ent", "pdb1kf7.ent"]]:
    #    run(file,x)

    #try:
    #    open("..\\Analyses\\basic_analysis_"+time.strftime("%a_%d_%b_%Y")+".xls","r")
    #except IOError:

    #for file in os.listdir(pdb_dir):
    #for file in ["pdb1axi.ent"]:
    #    run(pdb_dir+file,x)
    #n = len(os.listdir(pdb_dir))
    erfile = open("D:\\xampp\\htdocs\\python\\Errors\\error_"+analysis_type+"_"+date_+".log","w")               ## EDIT
    runlist = None
    #check command parameters
    if len(command_variables) < 2:
        #command_variables.pop(0)
        #run_list = []
        run_list = os.listdir(pdb_dir)
        run_list.remove("dsspout")
    elif len(command_variables) >= 2:
        command_variables.pop(0)
        run_list = []
        for i in command_variables:
            if i.find("\\") == -1:
               i = ".\\"+i
            if i.lower().find('.ent') != -1 or i.lower().find('.pdb') != -1:
               if not os.path.isfile(i):
                  erfile.write("The file "+i+" was not found.")
                  sys.exit(1)
               run_list.append(i)
               pdb_dir = ""
               dssp_dir = pdb_dir+os.path.dirname(i)+"\\dsspout"
    else:
         run_list = []
         run_list = command_variables[:]


    print "Checking DSSP files... "
    if dssp_dir == None:
       dssp_dir = pdb_dir+os.path.dirname(run_list[0])+"\\dsspout"
    if not os.path.isdir(dssp_dir):
       dssplist = []
    else:
       dssplist = os.listdir(dssp_dir)
    newlist = {}
    for j in dssplist:
        newlist[j.split(".")[0].split("_")[0]] = 1
    print len(newlist)
    print len(run_list)
    for i in run_list:
          found = 0
          print i[:-3].split("\\")[-1].rstrip(".")
          if newlist.has_key(i[:-3].split("\\")[-1].rstrip(".")):
             found = 1
          if found == 0:
             if not os.path.isdir(pdb_dir+os.path.dirname(i)+"\\dsspout"):
                os.mkdir(pdb_dir+os.path.dirname(i)+"\\dsspout")
             outpath= pdb_dir+os.path.dirname(i)+"\\dsspout"+"\\"
             erfile.write("python create_dssp.py "+pdb_dir+os.path.dirname(i)+"\\"+os.path.basename(i)+" "+outpath)
             os.system("python D:\\xampp\htdocs\python\SSP\create_dssp.py "+pdb_dir+os.path.dirname(i)+"\\"+os.path.basename(i)+" "+outpath)
             print "CREATE "
    print "Done"

#     print "Checking DSSP files... "
#     for i in run_list:
#         dssp_dir = pdb_dir+os.path.dirname(i)+"\\dsspout"
#         if not os.path.isdir(dssp_dir):
#            dssplist = []
#         else:
#            dssplist = os.listdir(dssp_dir)
#         found = 0
#         for j in dssplist:
#             if j.find(i[:-3].split("\\")[-1]) != -1:
#                  found = 1
#                  break;
#         if found == 0:
#             if not os.path.isdir(pdb_dir+os.path.dirname(i)+"\\dsspout"):
#                os.mkdir(pdb_dir+os.path.dirname(i)+"\\dsspout")
#             os.system("D:\\xampp\\htdocs\\python\\SSP\\dsspcmbi.exe "+pdb_dir+os.path.dirname(i)+"\\"+os.path.basename(i)+" > "+pdb_dir+os.path.dirname(i)+"\\dsspout\\"+i[:-3].split("\\")[-1]+"dssp")         ## EDIT
#             print "DSSP -> "+pdb_dir+os.path.basename(i)
#     print "Done"

    #else:
    #    try:
    #        run_list = [z.strip() for z in fopen("new_files_downloaded_on_"+command_variables[1])]
    #    except IOError:
    #        tag = "new_files_downloaded_on_"
    #        print "The file \""+tag+command_variables[1]+"\" does not exist. Possible options are:"
    #        for line in [z for z in os.listdir(".") if z[:24] == tag]:
    #            print line
    #        sys.exit(1)
###
###temp
#    import string
#    run_list = [z.replace(".dssp",".ent") for z in open("dssplist","r").read().split("\n") if z != ""]
#    aer = run_list.index("pdb2gi7.ent")
#    run_list = run_list[aer:]
#    print run_list
#    run_list = ["pdb2gi7.ent"]
###
    #histogram - for analysing relationships between secondary structures and bond types
    hist_ = {}
    #run with specified command parameters in run list
#    run_list = ["pdb1gpq.ent","pdb1gps.ent","pdb1gpt.ent","pdb1gpz.ent","pdb1gqb.ent","pdb1gqr.ent","pdb1gqs.ent","pdb1gqv.ent","pdb1gqz.ent","pdb1gr2.ent","pdb1gra.ent","pdb1grn.ent","pdb1grt.ent","pdb1gsk.ent","pdb1gsm.ent","pdb1gsn.ent","pdb1gsp.ent","pdb1gt6.ent","pdb1gtp.ent","pdb1gts.ent","pdb1gtt.ent","pdb1gu2.ent","pdb1gu3.ent","pdb1guj.ent","pdb1gur.ent","pdb1guv.ent","pdb1gv7.ent","pdb1gv8.ent","pdb1gv9.ent","pdb1gvc.ent","pdb1gvk.ent","pdb1gvl.ent","pdb1gvt.ent","pdb1gvu.ent","pdb1gvv.ent","pdb1gvw.ent","pdb1gvx.ent","pdb1gvz.ent","pdb1gw0.ent","pdb1gw2.ent","pdb1gwa.ent","pdb1gwb.ent","pdb1gwd.ent","pdb1gwn.ent","pdb1gwo.ent","pdb1gwt.ent","pdb1gwu.ent","pdb1gx2.ent","pdb1gx8.ent","pdb1gx9.ent","pdb1gxa.ent","pdb1gxd.ent","pdb1gxs.ent","pdb1gxv.ent","pdb1gxx.ent","pdb1gxy.ent","pdb1gxz.ent","pdb1gy0.ent","pdb1gyc.ent","pdb1gyd.ent","pdb1gye.ent","pdb1gyh.ent","pdb1gyo.ent","pdb1gz1.ent","pdb1gz2.ent","pdb1gz7.ent","pdb1gza.ent","pdb1gzb.ent","pdb1gzj.ent","pdb1gzm.ent","pdb1gzp.ent","pdb1gzq.ent","pdb1gzr.ent","pdb1gzy.ent","pdb1gzz.ent","pdb1h02.ent","pdb1h03.ent","pdb1h04.ent","pdb1h0b.ent","pdb1h0d.ent","pdb1h0g.ent","pdb1h0h.ent","pdb1h0i.ent","pdb1h0j.ent","pdb1h0l.ent","pdb1h0z.ent","pdb1h12.ent","pdb1h13.ent","pdb1h14.ent","pdb1h15.ent","pdb1h1b.ent","pdb1h1h.ent","pdb1h1n.ent","pdb1h20.ent","pdb1h22.ent","pdb1h23.ent","pdb1h2b.ent","pdb1h2p.ent","pdb1h2q.ent","pdb1h30.ent","pdb1h34.ent","pdb1h3j.ent","pdb1h3p.ent","pdb1h3t.ent","pdb1h3u.ent","pdb1h3v.ent","pdb1h3w.ent","pdb1h3x.ent","pdb1h3y.ent","pdb1h43.ent","pdb1h44.ent","pdb1h45.ent","pdb1h46.ent","pdb1h49.ent","pdb1h4i.ent","pdb1h4j.ent","pdb1h4p.ent","pdb1h4u.ent","pdb1h4w.ent","pdb1h52.ent","pdb1h53.ent","pdb1h55.ent","pdb1h57.ent","pdb1h58.ent","pdb1h59.ent","pdb1h5a.ent","pdb1h5b.ent","pdb1h5c.ent","pdb1h5d.ent","pdb1h5e.ent","pdb1h5f.ent","pdb1h5g.ent","pdb1h5h.ent","pdb1h5i.ent","pdb1h5j.ent","pdb1h5k.ent","pdb1h5l.ent","pdb1h5m.ent","pdb1h5o.ent","pdb1h5x.ent","pdb1h6m.ent","pdb1h6r.ent","pdb1h6v.ent","pdb1h75.ent","pdb1h76.ent","pdb1h7l.ent","pdb1h7q.ent","pdb1h80.ent","pdb1h81.ent","pdb1h82.ent","pdb1h83.ent","pdb1h84.ent","pdb1h86.ent","pdb1h87.ent","pdb1h8d.ent","pdb1h8i.ent","pdb1h8l.ent","pdb1h8n.ent","pdb1h8o.ent","pdb1h8p.ent","pdb1h8s.ent","pdb1h8u.ent","pdb1h8v.ent","pdb1h8x.ent","pdb1h8y.ent","pdb1h8z.ent","pdb1h91.ent","pdb1h9h.ent","pdb1h9i.ent","pdb1h9l.ent","pdb1h9v.ent","pdb1h9z.ent","pdb1ha0.ent","pdb1ha2.ent","pdb1ha6.ent","pdb1ha8.ent","pdb1ha9.ent","pdb1haa.ent","pdb1hae.ent","pdb1haf.ent","pdb1hag.ent","pdb1hah.ent","pdb1hai.ent","pdb1haj.ent"]
    n = len(run_list)
    typedict={}
    for type_ in ["lys_arg", "his", "asp_glu","trp","phe","tyr"]:
        typedict[type_] = (analysis_type == type_)

    timestart = time.ctime()
    for i,file in enumerate(run_list):
    #for i,file in enumerate(["pdb1w4y.ent"]):
#        print type(hist_)
        print pdb_dir+file
        hist_ = analysis.run(pdb_dir+file,
                     x,
                     erfile,
                     dist=threshold,
                     histogram = hist_,
                     lys_arg = typedict["lys_arg"],
                     his = typedict["his"],
                     asp_glu = typedict["asp_glu"],
                     trp = typedict["trp"],
                     phe = typedict["phe"],
                     tyr = typedict["tyr"])
        m = int((i+1)/float(n)*10000)/100.0
        print str(m)+"% complete"

    timefinish1 = time.ctime()
    print "\nResults file is being saved. Please do not close the program window.\n"
    ##################################################################
    ##The histogram bit
    def histcmp(a,b):
       return (hist_[a] < hist_[b])*2-1
    #fffff = open("histogram_","w")
    #hkeys = hist_.keys()[:]
    #hkeys.sort(histcmp)
    #x.add_sheet("Histogram")
    #histosheet = x.get_sheet(4)

    #histosheet.write(0,0,"Secondary structure 1",style0)
    #histosheet.write(0,1,"Secondary structure 2",style0)
    #histosheet.write(0,2,"Disulfide Bond type",style0)
    #histosheet.write(0,3,"Count",style0)
    #for row,h in enumerate(hkeys):
    #    fffff.write(str(h)+" "*(21-len(h))+str(hist_[h])+"\n")
    #    histosheet.write(row+1,0,h[0])
    #    histosheet.write(row+1,1,h[1])
    #    histosheet.write(row+1,2,h[2:])
    #    histosheet.write(row+1,3,hist_[h])
    #fffff.close()
    ##################################################################

    realactive = x.get_active_sheet()
    firstactive = 6
    sheet = x.get_sheet(0)
    if sheet.row(0).get_str_count() > 0:
       firstactive = 0
    sheet.set_first_visible_row(0)
    sheet = x.get_sheet(1)
    if sheet.row(0).get_str_count() > 0 and firstactive > 1:
       firstactive = 1
    sheet.set_first_visible_row(0)
    sheet = x.get_sheet(2)
    if sheet.row(0).get_str_count() > 0  and firstactive > 2:
       firstactive = 2
    sheet.set_first_visible_row(0)
    sheet = x.get_sheet(3)
    if sheet.row(0).get_str_count() > 0 and firstactive > 3:
       firstactive = 3
    sheet.set_first_visible_row(0)
    sheet = x.get_sheet(4)
    if sheet.row(0).get_str_count() > 0 and firstactive > 4:
       firstactive = 3
    sheet.set_first_visible_row(0)
    sheet = x.get_sheet(5)
    sheet.set_first_visible_row(0)
    if sheet.row(0).get_str_count() > 0 and firstactive > 5:
       firstactive = 5
    sheet.set_first_visible_row(0)
    sheet = x.get_sheet(6)
    sheet.set_first_visible_row(0)

    x.set_active_sheet(firstactive)
    x.save(write_path)
    if inA:
       os.system("7z a -tzip -mx=9 D:\\xampp\\htdocs\\python\\Analyses\\disulfide_analysis_"+date_+".zip "+write_path)
    print "\nAnalysis complete and results saved.\n"
    timefinish2 = time.ctime()
    erfile.close()

    print "start    =",timestart
    print "prcessed =",timefinish1
    print "saved    =",timefinish2
    #sorting and printing of histogram
    #gives descending sort
    #write histogram to spreadsheet

    #cys["SSBOND   7 CYS A 1348    CYS A 1380"]

    return write_path