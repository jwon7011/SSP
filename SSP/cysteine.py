
import calc,math

def cmp(l1,l2):
   return (l1[13:20] > l2[13:20])*2-1

class cysteine:
   def __init__ (self,list,irr=[],helix_=[],sheet_=[],turn_=[]):
      self.irreg    = irr
      self.cys = list
      list.sort(cmp)
      self.carbon   = list[0]
      self.a_carbon = list[1]
      self.b_carbon = list[2]
      self.nitrogen = list[3]
      self.oxygen   = list[4]
      self.sulfur   = list[5]
      self.strand   = self.carbon[21]
      self.residue  = self.carbon[22:27].strip()
      self.helix = helix_
      self.isHelix = self.helix != []
      self.sheet = sheet_
      self.isSheet = self.sheet != []
      self.turn  = turn_
      self.isTurn = self.turn != []
   def strand_residue(self):
      return self.strand+" "+self.residue
   def whoami(self):
      print self.strand,self.residue
   def distance_to_and_angles(self,cys2):
      a = calc.strain2(map(calc.coord,[self.nitrogen,self.a_carbon,self.b_carbon,self.sulfur,cys2.sulfur,cys2.b_carbon,cys2.a_carbon,cys2.nitrogen]))
      return [a[0],[aa*180/math.pi for aa in a[1]]]

   # Method added by Anushi : 26/05/2015
   def find_angle(self,cys2):
      a = calc.alpha_angle(map(calc.coord,[self.b_carbon,self.sulfur,cys2.sulfur]))
      b = calc.alpha_angle(map(calc.coord,[self.sulfur,cys2.sulfur,cys2.b_carbon]))
      return [a*180/math.pi,b*180/math.pi]
   
   def distance_sq_from_sulfur_to_atom(self,line):
      return calc.distance_sq(self.sulfur,line)
   def irregularities(self):
       return [str(sum([z == -1 for z in self.irreg[2:]])!=len(self.irreg)-2),str(self.irreg)]
   def debug1(self):
      coord = lambda s : [s[30+8*i:30+8*(i+1)] for i in range(3)]
      atomlist = [self.nitrogen,self.a_carbon,self.b_carbon,self.sulfur]
      for atom in atomlist:
         print atom
      print  [[float(c) for c in coord(atom)] for atom in atomlist]



#ATOM    538  N   CYS A  72      31.281  -0.974  11.494  1.00 10.38           N  
#ATOM    539  CA  CYS A  72      30.864  -0.181  12.646  1.00  8.31           C  
#ATOM    540  C   CYS A  72      29.477   0.381  12.402  1.00  8.92           C  
#ATOM    541  O   CYS A  72      29.064   0.585  11.232  1.00  7.77           O  
#ATOM    542  CB  CYS A  72      31.897   0.885  13.005  1.00  8.16           C  
#ATOM    543  SG  CYS A  72      33.276   0.174  13.962  1.00  8.35           S  

