import time
import datetime
import shutil
import re
import os

today = datetime.datetime.now()
curr_date = today.strftime("%Y-%m-%d")
month = today.strftime("%b")
year = today.strftime("%Y")

src="D:\\xampp\\htdocs\\python\\disulfideanalysis\\download.html"
dst="D:\\xampp\\htdocs\\python\\disulfideanalysis\\download_copy_"+str(curr_date)+".html"

shutil.copy(src, dst)

fileopen = open( "D:\\xampp\\htdocs\\python\\disulfideanalysis\\download.html", "r" )
file = open("D:\\xampp\\htdocs\\python\\disulfideanalysis\\newfile.html", "w")

for line in fileopen:
    
    match_words=re.search( "(disulfide_analysis)(\w+|\W+)(.zip)", line, re.M|re.I)

    if match_words:
        
        old_word = match_words.group()
        
        new_word="disulfide_analysis_01_"+str(month)+"_"+str(year)+".zip"
        #disulfide_analysis_01_Mar_2014.zip
        line=line.replace(old_word, new_word)
        
        file.write(line)
    else:
        file.write(line)
        
       
fileopen.close()
file.close()

new_dst="D:\\xampp\\htdocs\\python\\disulfideanalysis\\newfile.html"
shutil.copy(new_dst,src)
os.remove(new_dst)


