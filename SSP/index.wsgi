#!/Python26/python


import sys,os,cgi,random,time
sys.path.append('D:\\xampp\\htdocs\\python\\SSP')
#from mod_python import apache,util
from time import gmtime, strftime
import run
from fopen import *
import xlrd

htmls="""\
<html>
    <script type="text/javascript" src="Frame.js">

    </script>
<SCRIPT TYPE="text/javascript">
<!--
function fill(ssp)
{
   ssp.pdblist.value = "3FCS";
}
//-->
</SCRIPT>
<body bgcolor="white">
<form enctype="multipart/form-data" method="post">
<table border="1" cellpadding="3" cellspacing="0">
    <tr>
        <td valign="top">
            <table>
                <tr>
                    <td colspan="3">
                        <strong><font color=red size=2></font></strong></td>
                </tr>
                <tr>
                    <td colspan="3">
                        <strong>
                        <font face="Arial" size=2 color=#000000>Input PDB Entry Code (one per line):</font></strong></td>
                </tr>
                <tr>
                    <td colspan="3">
                        <textarea name="pdblist" rows=10></textarea></td>
                </tr>
                <tr>
                    <td colspan="3">
                    </td>
                </tr>
                <tr>
                    <td colspan="3">
                        <font face="Arial" size=2 color=#000000><strong>Input PDB file (.pdb or .ent):<br />
                        </strong></font><font face="Arial" size=2><em>for multiple files upload ZIP file (.zip or .gz) containing PDB files</em></font></td>
                </tr>
                <tr>
                    <td colspan="3">
                        <input name="PDBfile" type="file" /></td>
                </tr>
                <tr>
                    <td align="right" colspan="3"><HR>
                    </td>
                </tr>
                <tr>
                    <td align="left" colspan="2">
                        <input id="Submit1" type="submit" value="Submit" size="30" />
                        <input id="Reset1" type="reset" value="Reset" size="30" />
                    </td>
                    <td align="right" colspan="1">
                        <input id="Example" type="button" value="Example" size="30" onClick="fill(this.form)"/>
                        </td>
                </tr>
            </table>
        </td>
    </tr>
</table>
</form>
<!-- Start of StatCounter Code -->
<script type="text/javascript">
var sc_project=4095968; 
var sc_invisible=1; 
var sc_partition=49; 
var sc_click_stat=1; 
var sc_security="dbf9904e"; 
</script>

<script type="text/javascript" src="http://www.statcounter.com/counter/counter.js"></script><noscript><div class="statcounter"><a title="web stats" href="http://www.statcounter.com/free_web_stats.html" target="_blank"><img class="statcounter" src="http://c.statcounter.com/4095968/0/dbf9904e/1/" alt="web stats" ></a></div></noscript>
<!-- End of StatCounter Code -->
</body>
</html>
"""

def application(environ, start_response):
    status = '200 OK'
    html = htmls
    arg = ["basic_analysis.py"]
    if environ['REQUEST_METHOD'] == 'POST':
        post_env = environ.copy()
        post_env['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_env,
            keep_blank_values=True
        )
        fileitem = post['PDBfile']
        word = post['pdblist'].value
        THRESHOLD = 10
        #arg = ["basic_analysis.py"]
        notfound = []
        nossbond = []
        log = open("D:\\xampp\\htdocs\\python\\SSP\\iplog.txt",'a')
        ip = environ['REMOTE_ADDR']
        pdblist = word.split("\r\n")
        date =strftime("%a, %d-%b-%Y, %H:%M:%S,", gmtime())
        log.write(date)
        if len(ip) > 0:
           log.write(ip+",")
        for i in pdblist:
           log.write(i+",")
        log.write(fileitem.filename+"\n")
        log.close()

        if len(word) > 0:
               __process_pdblist(word,arg,nossbond,notfound)
        if fileitem.filename:
               newfile = __upload(post)
               if newfile.lower().find('.zip') != -1 or newfile.lower().find('.gz') != -1 or newfile.lower().find('.rar') != -1 or newfile.lower().find('.7z') != -1:
                  os.system("7z e -o"+os.path.dirname(newfile)+" "+newfile)                           ## EDIT
                  os.system("del "+newfile)                                                           ## EDIT
                  ls = os.listdir(os.path.dirname(newfile))
                  for i in ls:
                      if i.lower().find('.pdb') != -1 or i.lower().find('.ent') != -1:
                         if open(os.path.dirname(newfile)+"\\"+i).read().find("SSBOND")==-1:
                            nossbond.append(i)
                            pdblist.append(i)
                         else:
                            arg.append(os.path.dirname(newfile)+"\\"+i)
               if newfile.lower().find('.pdb') != -1 or newfile.lower().find('.ent') != -1:
                  if open(newfile).read().find("SSBOND")==-1:
                     nossbond.append(os.path.basename(newfile))
                     #pdblist.append(os.path.basename(newfile))
                  else:
                     arg.append(newfile)

    if len(arg)== 1:
             _error = "No valid PDB files found, please try again."
             html = htmls
    else:
             write_path = "D:\\xampp\\htdocs\\python\\Analyses\\"       ## EDIT
             write_path = run.main("basic_analysis",arg,THRESHOLD)
             s="""\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-loose.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
<meta http-equiv="content-type" content="text/html; charset=iso-8859-1" />
<title>SSP</title>
    <script type="text/javascript" src="Frame.js"></script>

<style type='text/css'>

/* Scrollable Content Height */
.scrollContent {
 height:100px;
 overflow-x:hidden;
 overflow-y:auto;
}

.scrollContent tr {
 height: auto;
 white-space: nowrap;
}

/* Prevent Mozilla scrollbar from hiding right-most cell content */
.scrollContent tr td:last-child {
 padding-right: 20px;
}

/* Fixed Header Height */
.fixedHeader tr {
 position: relative;
 height: auto;
 /* this fixes IE header jumping bug when mousing over rows in the tbody */
 top: expression( this.parentNode.parentNode.parentNode.scrollTop + 'px' );
}

/* Put border around entire table */
div.TableContainer {
 border: 1px solid #6990dc;
 overflow-y:auto;
}

/* Table Header formatting */
.headerFormat {
 background-color: white;
 color: #292929;
 margin: 3px;
 padding: 1px;
 white-space: pre-wrap;
 word-wrap: break-word;
 white-space: -o-pre-wrap;
 font-family: Helvetica;
 font-size: 10px;
 text-decoration: none;
 font-weight: bold;
}
.headerFormat tr td {
 border: 1px solid #ffd706;
 background-color: #ffd706;
}

/* Table Body (Scrollable Content) formatting */
.bodyFormat tr td {
	color: #000000;
	margin: 3px;
	padding: 1px;
	border: 0px none;
	font-family: Helvetica;
	font-size: 10px;
}

/* Use to set different color for alternating rows */
.alternateRow {
  background-color: #fff1a8;
}

/* Styles used for SORTING */
.point {
 cursor:pointer;
}

td.sortedColumn {
  /*background-color: #c5deff*/;
  background-color: white;
}

tr.alternateRow td.sortedColumn {
  /*background-color: #6990dc*/;
  background-color: #ffd706;
}

.total {
	background-color: #FED362;
	color: #000000;
	white-space: nowrap;
	font-size: 12px;
	text-decoration: none;
}

table.scrollTable tr:hover {
	background-color: #ffd706;
	color: #000000;
	font-style: normal;
}

.hoverMe {
	background-color: #ffd706;
	color: #000000;
	font-style: normal;
}

</style>
<!--[if IE]>
<style type="text/css">
/* IE Specific Style addition to constrain table from automatically growing in height */
div.TableContainer {
 height: 121px; 
 overflow-x:hidden;
 overflow-y:auto;
}
</style>
<![endif]-->

<script type="text/JavaScript" src="../Analyses/sortTable.js"></script>
<script>
// Function to scroll to top before sorting to fix an IE bug
// Which repositions the header off the top of the screen
// if you try to sort while scrolled to bottom.
function GoTop() {
 document.getElementById('TableContainer').scrollTop = 0;
}


</script>

</head>
<body bgcolor="white">
<table border="1" cellpadding="3" cellspacing="0">
    <tr>
        <td valign="top">
            <table>
                 <tr>
                    <td align="left" colspan="4"><p>
                        <font face="Arial" size=3 color=#000000>
                        <b>Analysis complete</b></font>
                        </td>
                        </tr>
                        <tr>
                            <td align="right" colspan="4"><HR>
                            </td>
                        </tr>
                         <tr><td>"""

             s+= __process_output(write_path)

             s+="""</td></tr><tr><td><p><font face="Arial" size=2>Download full results
"""
             filename = os.path.basename(write_path)
             s+="<A href=http://149.171.101.136/python/Analyses/"+filename+">HERE</A>"       ## EDIT
             s+=""" (Excel format .xls)</font></td>
                </tr>
                <tr>
                    <td align="right" colspan="4"><HR>
                    </td>
                </tr>
                <tr>
                    <td colspan="3">
                        <table>
                            <tr>
                                <td>
                                    <table>
                                        <tr>
                                            <td colspan="3">
                        <font face="Arial" size=2 color=#000000><strong>Analysed:</strong></font></td>
                                        </tr>
                                        <tr>
                    <td colspan="3">
                        <textarea id="pdblist" rows="5" cols="10">"""
             for i in arg:
               base = os.path.basename(i)
               start = 0
               if base[:4].find('pdb') != -1:
                  start = 3
               end = len(base)
               if base.lower().find('.ent') != -1 or base.lower().find('.pdb') != -1:
                  end = len(base)-4
               s+=base[start:end].upper()+"\r\n"
             s+="""</textarea></td>
                                        </tr>
                                    </table>
                                </td>
                                <td>
                                    <table>
                                        <tr>
                    <td colspan="3">
                        <font face="Arial" size=2 color=#000000><strong>No SS-Bonds:</strong></font></td>
                                        </tr>
                                        <tr>
                    <td colspan="3">
                        <textarea id="Textarea2" rows="5" cols="10">"""
             for i in nossbond:
               s+=i+"\r\n"
             s+="""</textarea></td>
                                        </tr>
                                    </table>
                                </td>
                                <td>
                                    <table>
                                        <tr>
                    <td colspan="3">
                        <font face="Arial" size=2 color=#000000><strong>Not in database:</strong></font></td>
                                        </tr>
                                        <tr>
                    <td colspan="3">
                        <textarea id="Textarea3" rows="5" cols="10">"""
             for i in notfound:
               s+=i+"\r\n"
             s+="""</textarea></td>
                                        </tr>
                                    </table>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
                <tr>
                    <td colspan="3">
                    <hr />
                    </td>
                </tr>
                <tr>
                     <td align="left" colspan="4">
                         <font face="Arial" size=2>Click <A href=http://149.171.101.136/python/SSP/>here</A> to go back</font></td>
                </tr>
            </table>
        </td>
    </tr>
</table>
<!-- Start of StatCounter Code -->
<script type="text/javascript">
var sc_project=4095968;
var sc_invisible=1;
var sc_partition=49;
var sc_click_stat=1;
var sc_security="dbf9904e";
</script>

<script type="text/javascript" src="http://www.statcounter.com/counter/counter.js"></script><noscript><div class="statcounter"><a title="web stats" href="http://www.statcounter.com/free_web_stats.html" target="_blank"><img class="statcounter" src="http://c.statcounter.com/4095968/0/dbf9904e/1/" alt="web stats" ></a></div></noscript>
<!-- End of StatCounter Code -->
</body>
</html>
"""
             html = s
    response_headers = [('Content-type', 'text/html')]
    start_response(status, response_headers)
    return [html]

def __process_pdblist(pdblist,arg,nossbond,notfound):
    plist = pdblist.split("\r\n")
    print plist
    pdb_dir = fopen("D:\\xampp\\htdocs\\python\\SSP\\absolute_path_of_pdb_files")[0].strip()        ## EDIT
    full_list = os.listdir(pdb_dir)
    full_list.remove("dsspout")
    for i in plist:
        if len(i) != 4:
           notfound.append(i)
        else:
           found = 0
           for j in full_list:
               if j.find(i.lower())!=-1:
                  found = 1
                  arg.append(pdb_dir+j)
                  break
           if found == 0:
               if len(i) >=1:
                  noSS = open("D:\\xampp\\htdocs\\python\\SSP\\files_not_containing_ssbonds")
                  found2 = 0
                  for j in noSS:
                      if j.find(i.lower()) != -1:
                         nossbond.append(i.upper())
                         found2 = 1
                         break
                  noSS.close()
                  if found2 == 0:
                     notfound.append(i.upper())
                     
def __process_output(write_path):
       book = xlrd.open_workbook(write_path)
       sh = book.sheets()
       output = """
<table cellpadding="0" cellspacing="0" border="0"><tr><td><div id="TableContainer" class="TableContainer" style="height:250px;">

<table class="scrollTable">
  <thead class="fixedHeader headerFormat" >
      <tr class="title">
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="50"><b>PDB ID</b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="50"><b>Cys1 chain</b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="50"><b>Cys1 residue</b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="180"><b>Cys1 secondary <br>structure</b> <img src="../Analyses/none.gif" border="0" /></td>

       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="110"><b>Cys1 solvent accessibilty, &Aring;<sup>2</sup></b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="50"><b>Cys2 chain</b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="50"><b>Cys2 residue</b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="180"><b>Cys2 secondary <br>structure</b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="110"><b>Cys2 solvent accessibilty, &Aring;<sup>2</sup></b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="80"><b>Strain energy, kJ/mol</b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="150"><b>Alpha-carbon distance, &Aring;</b> <img src="../Analyses/none.gif" border="0" /></td>
       <td class="point" onclick="GoTop(); sortTable(this,0); HoverRow();" title="Sort" align="center" width="50"><b>Classification</b> <img src="../Analyses/none.gif" border="0" /></td>

      </tr>
  </thead>"""
       output+="""<tbody class="scrollContent bodyFormat" style="height:170px;">
       """
       odd = 1
       rows = [0,5,6,7,8,9,10,11,12,22,23,25]
       for s in sh:
          if s.nrows > 1:
               for r in range(1,s.nrows):
                   if odd == 1:
                      output+="""<tr class="alternateRow">
                      """
                      odd = 0
                   else:
                      output+="<tr>\n"
                      odd = 1
                   for c in range(s.ncols):
                       i = -1
                       try:
                           i = rows.index(c)
                       except ValueError:
                           i = -1 # no match
                       if i != -1:
                           output += "<td align=\"center\">"+__textToSymb(str(s.cell_value(r,c)))+"</td>\n"
                   output += "</tr>\n"
       output+="""
</tbody>
 </table>
 
</div></td></tr></table>
"""
       return output

def __textToSymb(text):
    if text == "extended strand, participates in beta ladder":
       return "strand"
    if text[0] == '.':
       return text[1:]
    if __is_number(text):
       if text.find('.') == 1:
          return text[:6]
       if text.find('.') == 2:
          return text[:7]
       if text.find('.') == 3:
          return text[:8]
    return text
    
def __is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

# Generator to buffer file chunks
def __fbuffer(f, chunk_size=10000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk

def __upload(req):
   
   try: # Windows needs stdio set for binary mode.
      import msvcrt
      msvcrt.setmode (0, os.O_BINARY) # stdin  = 0
      msvcrt.setmode (1, os.O_BINARY) # stdout = 1
   except ImportError:
      pass

   # A nested FieldStorage instance holds the file
   fileitem = req['PDBfile']

   # Test if the file was uploaded
   if fileitem.filename:

      # strip leading path from file name to avoid directory traversal attacks
      fname = os.path.basename(fileitem.filename)
      # build absolute path to files directory
      date_ = time.strftime("%d%b%Y")
      path = "D:\\xampp\\htdocs\\python\\upload\\"                                          ## EDIT
      path+=date_+"\\"
      path+=str(int(random.random()*100000000))
      os.makedirs(path)
      dir_path = path
      f = open(os.path.join(dir_path, fname), 'wb', 10000)

      # Read the file in chunks
      for chunk in __fbuffer(fileitem.file):
         f.write(chunk)
      f.close()
      message = 'The file "%s" was uploaded successfully' % fname

   else:
      message = 'No file was uploaded'
   
   return os.path.join(dir_path, fname)


