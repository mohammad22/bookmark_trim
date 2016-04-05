import os
import argparse
import logging
try: 
    import subprocess32 as sbp
except: 
    import subprocess as sbp
import os.path as osp

def pdf_handler(pdf):

    djvu = osp.splitext(pdf)[0] + '.djvu'
    sbp.call(["pdf2djvu", "-o", djvu, "--loss-level=5", "--fg-colors=black", pdf])    

       

if __name__ == "__main__":
    
    #####################################
    ## Command-line argument handling ###
    #####################################

    parser = argparse.ArgumentParser(description = 'djvu handler. The\
            positional argument is: pdf.\
            It should be a valid pdf-file or a directory.\
            These are exclusive options. If pdf is a directory\
            all the pdf files in this  directory will be treated.')
    parser.add_argument('pdf', help = "converts this file or all the files\
            in this directory.")
    args = parser.parse_args()
    
    work_dir = os.getcwdu()
    pdf2 = osp.join(work_dir, osp.split(args.pdf)[1])        
   
    if osp.isfile(args.pdf) or osp.isdir(args.pdf):
        pdf = osp.realpath(args.pdf)
    elif osp.isfile(pdf2) or osp.isdir(pdf2):
        pdf = pdf2

    else:
        raise ValueError('Invalid file or directory: %s\n' % args.pdf)

    
    ##############################
    ## log error handling setup ##
    ##############################
    if osp.isfile(pdf):
        log_path = osp.join(osp.dirname(pdf), "pdf_handler.log")
    else:
        log_path = osp.join(pdf, "pdf_handler.log")

    logging.basicConfig(filename = log_path, filemode = "w",\
            level = logging.DEBUG)


    ###############
    ## The main ###
    ###############

    if osp.isfile(pdf):
        pdf_handler(pdf)
    
    elif osp.isdir(pdf):
        YES = {"YE", "Y", "YES", "YEAH", "YEA"}
        NO = {"NO", "N", "NOPE", "NEY"}
        s = ' ' 
        while not (s.upper() in (YES | NO)):
            s = raw_input("Seriously! treating all the files in this directory? (Y/N):")

        if s.upper() in YES: 
            for f in os.listdir(pdf):
                ff = osp.join(pdf, f) 
                """ for debugging the directory loop
                print "this is path:", ff, "\n"
                raw_input("Press any key to continue...")
                """
                if osp.splitext(ff)[1] == ".pdf":
                    pdf_handler(ff)
        
        elif s.upper() in NO:
            print "Okay! May be next time!\n"
    else: 
        raise SyntaxError("You should determine if this is a file or directory, try with -h option for more info!")
