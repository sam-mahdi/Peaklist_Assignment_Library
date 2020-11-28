import re

def custom_percent_parameters(terminal_line):
    ALA=re.search('-ALA (\w+)',terminal_line)
    ARG=re.search('-ARG (\w+)',terminal_line)
    ASN=re.search('-ASN (\w+)',terminal_line)
    ASP=re.search('-ASP (\w+)',terminal_line)
    CYS=re.search('-CYS (\w+)',terminal_line)
    GLN=re.search('-GLN (\w+)',terminal_line)
    GLU=re.search('-GLU (\w+)',terminal_line)
    GLY=re.search('-GLY (\w+)',terminal_line)
    HIS=re.search('-HIS (\w+)',terminal_line)
    ILE=re.search('-ILE (\w+)',terminal_line)
    LEU=re.search('-LEU (\w+)',terminal_line)
    LYS=re.search('-LYS (\w+)',terminal_line)
    MET=re.search('-MET (\w+)',terminal_line)
    PHE=re.search('-PHE (\w+)',terminal_line)
    PRO=re.search('-PRO (\w+)',terminal_line)
    SER=re.search('-SER (\w+)',terminal_line)
    THR=re.search('-THR (\w+)',terminal_line)
    TRP=re.search('-TRP (\w+)',terminal_line)
    TYR=re.search('-TYR (\w+)',terminal_line)
    VAL=re.search('-VAL (\w+)',terminal_line)
    if ALA is None:
        ALA=0
    else:
        ALA=int(ALA.group(1))
    if ARG is None:
        ARG=0
    else:
        ARG=int(ARG.group(1))
    if ASN is None:
        ASN=0
    else:
        ASN=int(ASN.group(1))
    if ASP is None:
        ASP=0
    else:
        ASP=int(ASP.group(1))
    if CYS is None:
        CYS=0
    else:
        CYS=int(CSY.group(1))
    if GLN is None:
        GLN=0
    else:
        GLN=int(GLN.group(1))
    if GLU is None:
        GLU=0
    else:
        GLU=int(GLU.group(1))
    if GLY is None:
        GLY=0
    else:
        GLY=int(GLY.group(1))
    if HIS is None:
        HIS=0
    else:
        HIS=int(HIS.group(1))
    if ILE is None:
        ILE=0
    else:
        ILE=int(ILE.group(1))
    if LEU is None:
        LEU=0
    else:
        LEU=int(LEU.group(1))
    if LYS is None:
        LYS=0
    else:
        LYS=int(LYS.group(1))
    if MET is None:
        MET=0
    else:
        MET=int(MET.group(1))
    if PHE is None:
        PHE=0
    else:
        PHE=(PHE.group(1))
    if PRO is None:
        PRO=0
    else:
        PRO=int(PRO.group(1))
    if SER is None:
        SER=0
    else:
        SER=int(SER.group(1))
    if THR is None:
        THR=0
    else:
        THR=int(THR.group(1))
    if TRP is None:
        TRP=0
    else:
        TRP=int(TRP.group(1))
    if TYR is None:
        TYR=0
    else:
        TYR=int(TYR.group(1))
    if VAL is None:
        VAL=0
    else:
        VAL=int(VAL.group(1))
    return ALA,ARG,ASN,ASP,CYS,GLN,GLU,GLY,HIS,ILE,LEU,LYS,MET,PHE,PRO,SER,THR,TRP,TYR,VAL
