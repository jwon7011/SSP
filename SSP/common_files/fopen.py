
#<!-- JobDetails Start -->
#<!-- JobFooter Start -->

def cutbetween(list,tag1,tag2):
   n = find_first_position_in_list(list,tag1)
   if n != -1:
      m = find_first_position_in_list(list[n:],tag2)
      return list[n:m+n+1]
   return []

#for a list of strings, return a list including only strings containing tag
def filter(list,tag):
   list_ = []
   for line in list:
      if line.find(tag) !=-1:
         list_.append(line)
   return list_

#Given a list of strings, this function will return a new list of strings
#consisting of the original list with a new list inserted in the stated position
def insert_n_lines_after(list,n,look_for,insert_this):
   k = find_first_position_in_list(list,look_for)
   return list[:k+n+1]+insert_this+list[k+n+1:]

def gopen(fname):
   return [open(fname,"r").readlines(),open(fname,"w")]

def fopen(fname):
   return open(fname,"r").readlines()

def fwrite(fname,list):
   file = open(fname,"w")
   for line in list:
      file.write(line)
   file.close()

#replace function on a list of strings
def lreplace(list,a,b):
   newlist = []
   for line in list:
      newlist.append(line.replace(a,b).rstrip())
   return newlist

def return_between(l,a,b):
   if l.find(a)!=-1 and l[l.find(a)+len(a):].find(b)!=-1:
      return [l[l.find(a)+len(a):l[l.find(a)+len(a):].find(b)+l.find(a)+len(a)]]+return_between(l[l.find(b)+1:],a,b)
   else:
      return []

def kill_between(l,a,b):
   if l.find(a)!=-1 and l[l.find(a):].find(b)!=-1:
      return l[:l.find(a)]+kill_between(l[l.find(b)+len(b):],a,b)
   else:
      return l

def contains_any_instance_of(line,list):
   for item in list:
      if line.find(item)!=-1:
         return 1
   return 0

def find_or(line,list):
   for item in list:
      if item.find(line)!=-1:
         return 1
   return 0

#list must be a list of strings
def find_first_position_in_list(list,look_for):
   i = 0
   for line in list:
      if line.find(look_for) != -1:
         return i
      i=i+1
   return -1

def find_and(line,list):
   for item in list:
      if line.find(item)==-1:
         return 0
   return 1

def print_list(list):
   for line in list:
      print line,

def list_split(list,tag):
   a = []
   while list != []:
      n = find_first_position_in_list(list,tag)
      if n!=-1:
         a.append(list[:n+1])
         list = list[n+1:]
      else:
         a.append(list)
         list = []
   return a

def strip_all(list):
   l = []
   for i in list:
      l.append(i.strip())
   return l
