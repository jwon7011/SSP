class bsheet:
    def __init__ (self):
        self.strand      = []
        self.sheetID     = []
        self.numStrands  = []
        self.initResName = []
        self.initChainID = []
        self.initSeqNum  = []
        #self.initICode   = []
        self.endResName  = []
        self.endChainID  = []
        self.endSeqNum   = []
        #self.endICode    = []
        self.sense       = []
        self.curAtom     = []
        self.curResName  = []
        self.curChainID  = []
        self.curResSeq   = []
        self.curICode    = []
        self.prevAtom    = []
        self.prevResName = []
        self.prevChainId = []
        self.prevResSeq  = []
        self.prevICode   = []
    def addsheet(self,line):
        self.strand        .append(line[7:10])
        self.sheetID       .append(line[11:14])
        self.numStrands    .append(line[14:16])
        self.initResName   .append(line[17:20])
        self.initChainID   .append(line[21])
        self.initSeqNum    .append(int(line[22:26]))
        #self.initICode     .append(line[26])
        self.endResName    .append(line[28:31])
        self.endChainID    .append(line[32])
        self.endSeqNum     .append(int(line[33:37]))
        #self.endICode      .append(line[37])
        self.sense         .append(line[38:40])
        self.curAtom       .append(line[41:45])
        self.curResName    .append(line[45:48])
        self.curChainID    .append(line[49])
        self.curResSeq     .append(line[50:54])
        self.curICode      .append(line[54])
        self.prevAtom      .append(line[56:60])
        self.prevResName   .append(line[60:63])
        self.prevChainId   .append(line[64])
        self.prevResSeq    .append(line[65:69])
        self.prevICode     .append(line[69])
    def contains(self,chain,seq):
        group = []
        for begin_ch,end_ch,begin_seq,end_seq,num,id_,sense in zip(self.initChainID,self.endChainID,self.initSeqNum,self.endSeqNum,self.strand,self.sheetID,self.sense):
            if begin_ch <= chain and chain <= end_ch:
                if begin_seq <= seq and seq <= end_seq:
                    group.append((num,id_,sense))
        return group

