class turn:
    def __init__ (self):
        self.seq         = []
        self.turnID      = []
        self.initResName = []
        self.initChainID = []
        self.initSeqNum  = []
        #self.initICode   = []
        self.endResName  = []
        self.endChainID  = []
        self.endSeqNum   = []
        #self.endICode    = []
    def addturn(self,line):
        self.seq           .append(line[9:10])
        self.turnID        .append(line[11:14])
        self.initResName   .append(line[15:18])
        self.initChainID   .append(line[19])
        self.initSeqNum    .append(int(line[20:24]))
        #self.initICode     .append(line[24])
        self.endResName    .append(line[26:29])
        self.endChainID    .append(line[30])
        self.endSeqNum     .append(int(line[31:35]))
        #self.endICode      .append(line[35])
    def contains(self,chain,seq):
        group = []
        for begin_ch,end_ch,begin_seq,end_seq,num,id_ in zip(self.initChainID,self.endChainID,self.initSeqNum,self.endSeqNum,self.seq,self.turnID):
            if begin_ch <= chain and chain <= end_ch:
                if begin_seq <= seq and seq <= end_seq:
                    group.append((num,id_,0))
        return group

