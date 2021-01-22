class helix:
    def __init__ (self):
        self.serNum      = []
        self.helixID     = []
        self.initResName = []
        self.initChainID = []
        self.initSeqNum  = []
        #self.initICode   = []
        self.endResName  = []
        self.endChainID  = []
        self.endSeqNum   = []
        #self.endICode    = []
        self.helixClass  = []
        #self.length      = []
    def addhelix(self,line):
        self.serNum        .append(line[7:10])
        self.helixID       .append(line[11:14])
        self.initResName   .append(line[15:18])
        self.initChainID   .append(line[19])
        self.initSeqNum    .append(int(line[21:25]))
        #self.initICode     .append(line[25])
        self.endResName    .append(line[27:30])
        self.endChainID    .append(line[31])
        self.endSeqNum     .append(int(line[33:37]))
        #self.endICode      .append(line[37])
        self.helixClass    .append(line[38:40])
        #self.length        .append(line[71:76])
    def contains(self,chain,seq):
        group = []
        for begin_ch,end_ch,begin_seq,end_seq,num,id_,class_ in zip(self.initChainID,self.endChainID,self.initSeqNum,self.endSeqNum,self.serNum,self.helixID,self.helixClass):
            if begin_ch <= chain and chain <= end_ch:
                if begin_seq <= seq and seq <= end_seq:
                    group.append((num,id_,class_))
        return group
    def getSerial(self):
        return [self.serNum,self.initChainID,self.initSeqNum,self.endChainID,self.endSeqNum]
