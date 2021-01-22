#!/Python26/python


import sys,os,cgi,random,time
sys.path.append('D:\\xampp\\htdocs\\python\\SSP')
#from mod_python import apache,util
from time import gmtime, strftime
import run
from fopen import *
import xlrd
from cgi import parse_qs, escape

def application(environ, start_response):
    status = '200 OK'
    log = open("D:\\xampp\\htdocs\\python\\SSP\\iplog.txt",'a')
    if environ['REQUEST_METHOD'] == 'GET':
        d = parse_qs(environ['QUERY_STRING'])
        pdb = d.get('pdb', [''])[0]
        pdb = escape(pdb)
        ip = environ['REMOTE_ADDR']
        date =strftime("%a, %d-%b-%Y, %H:%M:%S,", gmtime())
        log.write(date)
        if len(ip) > 0:
           log.write(ip+",")
        log.write(pdb+",R\n")
        log.close()
        if pdb:
           if len(pdb) != 4:
              return "Invalid PDB"
           plist = []
           arg = ["basic_analysis.py"]
           plist.append(pdb)
           pdb_dir = fopen("D:\\xampp\\htdocs\\python\\SSP\\absolute_path_of_pdb_files")[0].strip()        ## EDIT
           full_list = os.listdir(pdb_dir)
           full_list.remove("dsspout")
           for i in plist:
                 found = 0
                 for j in full_list:
                     if j.find(i.lower())!=-1:
                        found = 1
                        arg.append(pdb_dir+j)
                        break
           if len(arg) < 2:
              noSS = open("D:\\xampp\\htdocs\\python\\SSP\\files_not_containing_ssbonds")
              for i in noSS:
                  if i.find(pdb) != -1:
                     noSS.close()
                     return "PDB does not contain disulfides"
              noSS.close()
              return "PDB file not found in database"
           write_path = run.main("basic_analysis",arg,10)
           #filename = "http://129.94.84.111/python/Analyses/"+os.path.basename(write_path)
           book = xlrd.open_workbook(write_path)
           sh = book.sheets()
           output = ""
           for s in sh:
              if s.nrows > 1:
                 for r in range(s.nrows):
                     for c in range(s.ncols):
                        try:
                            output += str(s.cell_value(r,c))+"\t"
                        except UnicodeEncodeError:
                            output += s.cell_value(r,c).encode('utf-8').strip()+"\t"
                     output += "\n"
           if len(output) == 0:
                  output="No Disulfides"
        else:
           output= "Invalid argument"
    response_headers = [('Content-Type', 'text/plain'),('Content-Length', str(len(output)))]
    start_response(status, response_headers)
    return [output]



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


