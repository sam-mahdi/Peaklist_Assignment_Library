import re
import os
def sparky2nmrstar_parameters(terminal_line):
    seq_directory=os.getcwd()
    NHSQC_directory=os.getcwd()
    HNCA_directory=os.getcwd()
    HNCACB_directory=os.getcwd()
    HNCO_directory=os.getcwd()
    HNCOCA_directory=os.getcwd()
    CHSQC_directory=os.getcwd()
    HBHACONH_directory=os.getcwd()
    CCH_TOCSY_directory=os.getcwd()
    HCCH_TOCSY_directory=os.getcwd()
    save_directory=os.getcwd()
    bmrb_directory=os.getcwd()
    sequence_file=(re.search('-seq (\w+\.\w+)',terminal_line)).group(1)
    save_file=(re.search('-out (\w+\.\w+)',terminal_line)).group(1)
    NHSQC_file=(re.search('-nhsqc (\w+\.\w+)',terminal_line))
    HNCA_file=(re.search('-hnca (\w+\.\w+)',terminal_line))
    HNCACB_file=(re.search('-hncacb (\w+\.\w+)',terminal_line))
    HNCO_file=(re.search('-hnco (\w+\.\w+)',terminal_line))
    HNCOCA_file=(re.search('-hncoca (\w+\.\w+)',terminal_line))
    CHSQC_file=(re.search('-chsqc (\w+\.\w+)',terminal_line))
    HBHACONH_file=(re.search('-hbhaconh (\w+\.\w+)',terminal_line))
    CCH_TOCSY_file=(re.search('-cch_tocsy (\w+\.\w+)',terminal_line))
    HCCH_TOCSY_file=(re.search('-hcch_tocsy (\w+\.\w+)',terminal_line))
    bmrb_file=(re.search('-bmrb (\w+\.\w+)',terminal_line))
    standard_deviation_value=float((re.search('-std (\w+\.\w+)',terminal_line)).group(1))
    if NHSQC_file is None:
        NHSQC_file=()
    else:
        NHSQC_file=NHSQC_file.group(1)
    if HNCA_file is None:
        HNCA_file=()
    else:
        HNCA_file=HNCA_file.group(1)
    if HNCACB_file is None:
        HNCACB_file=()
    else:
        HNCACB_file=HNCACB_file.group(1)
    if HNCO_file is None:
        HNCO_file=()
    else:
        HNCO_file=HNCO_file.group(1)
    if HNCOCA_file is None:
        HNCOCA_file=()
    else:
        HNCOCA_file=HNCOCA_file.group(1)
    if CHSQC_file is None:
        CHSQC_file=()
    else:
        CHSQC_file=CHSQC_file.group(1)
    if HBHACONH_file is None:
        HBHACONH_file=()
    else:
        HBHACONH_file=HBHACONH_file.group(1)
    if CCH_TOCSY_file is None:
        CCH_TOCSY_file=()
    else:
        CCH_TOCSY_file=CCH_TOCSY_file.group(1)
    if HCCH_TOCSY_file is None:
        HCCH_TOCSY_file=()
    else:
        HCCH_TOCSY_file=HCCH_TOCSY_file.group(1)
    if bmrb_file is None:
        bmrb_file=()
    else:
        bmrb_file=bmrb_file.group(1)
    return sequence_file,seq_directory,NHSQC_file,HNCA_file,HNCACB_file,HNCO_file,HNCOCA_file,NHSQC_directory,HNCA_directory,HNCACB_directory,HNCO_directory,HNCOCA_directory,CHSQC_file,CHSQC_directory,HBHACONH_file,HBHACONH_directory,CCH_TOCSY_file,CCH_TOCSY_directory,HCCH_TOCSY_file,HCCH_TOCSY_directory,save_file,save_directory,standard_deviation_value,bmrb_file,bmrb_directory
