
import fnmatch
import codecs
import bookmark_trim as bmt
import argparse
import logging
try: 
    import subprocess32 as sbp
except: 
    import subprocess as sbp
import os.path as osp
import os


def pdf_trimmer(pdf, stop = False, sr = False):
    """ takes the path of a valid pdf file as pdf and returns the trimmed\
        txt file of its bookmarks as a path file new_txt_pdf, if not successful it returns integer 1.
        If stop is True it does not clean the repretitive words from 
        bookmarks; otherwise it does (this is the default beahvour). \
    """
    try: 
        a = sbp.check_output(["jpdfbookmarks", "-d", pdf]) 
    except sbp.CalledProcessError:
        logging.warning("Unable to read or extract bookmarks of file %s" % pdf)
        return 1
   
    o = osp.splitext(osp.realpath(pdf))
    txt_pdf = '_'.join([o[0], ".txt"]) 
    f = file(txt_pdf, "w")
    f.write(a)
    f.close()

    bmt.bookmark_trim(txt_pdf, stop = stop, sr = sr)
    u = osp.splitext(osp.realpath(txt_pdf))
    new_txt_pdf = u[0] + '_new' + u[1]
    sbp.call(["rm", txt_pdf])
    
    return new_txt_pdf


def pdf_bookmarker(pdf, txt):
    """ 
       Makes txt as bookmarks of pdf.
    """
    o = osp.splitext(osp.realpath(pdf))
    new_pdf = '_'.join([o[0], "new", o[1]]) 
    sbp.call(["jpdfbookmarks", "-a", txt, "-o",\
            new_pdf, pdf])
    
    head_pdf = osp.split(pdf)[1][:10] 
    if osp.isfile(new_pdf):
        logging.info("Successfully trimmed the bookmarks of %s" % head_pdf)
        sbp.call(["rm", pdf])
        sbp.call(["mv", new_pdf, pdf])
         
    
def pdf_compress(pdf):
    """ Tries to optimize the pdf file, in case of success it overrides 
        the existing pdf; otherwise, does nothing. 
    """    
    o = osp.splitext(osp.realpath(pdf))
    head_pdf = osp.split(pdf)[1][:10] 
    new_pdf = '_'.join([o[0], "new", o[1]]) 
    try:
        sbp.call(["gs",\
                  "-o", new_pdf,\
                  "-sDEVICE=pdfwrite",\
                   "-dNOPAUSE",\
                   "-q",\
                   "-dPdfSize=/screen",\
                   pdf])
    except sbp.CalledProcessError:
        logging.warning("Unsucessful attempt to compress %s \n" % head_pdf)
    if osp.isfile(new_pdf) & (osp.getsize(new_pdf) < osp.getsize(pdf)):
        logging.info("Sucessfuly compressed the file: %s" % head_pdf) 
        sbp.call(["rm", pdf])
        sbp.call(["mv", new_pdf, pdf])
    else:
        logging.warning("The compression of %s  was not sucessful!" % head_pdf)
        logging.warning("Returned the original file..")
        sbp.call(["rm", new_pdf])


def djvu_handler(pdf):

    djvu = osp.splitext(pdf)[0] + '.djvu'
    sbp.call(["pdf2djvu", "-o", djvu, "--fg-colors=black",\
            "--loss-level=10", pdf])


def dependency_checker(djvu = False, jpdf = True, gs = True):    

    if djvu == True:
        try:
            sbp.call(["pdf2djvu", "--version"])
        except:
            raise ValueError("You should have pdf2djvu (part of DjvuLibre)\
                             installed! \n")
    else:

        if jpdf == True:
            try:
                sbp.call(["jpdfbookmarks", "-v"])
            except:
                raise ValueError("You should have jpdfbookmarks\
                                 installed!\n")
        if gs == True:
            try:
                sbp.call(["gs", "-v"])
            except:
                raise ValueError("You should have ghostscript installed!\n")


def pdf_handler(pdf, stop = False, stop_optimize = False, sr = False,\
                djvu = False):
    """ Trims the bookmark and compresses the pdf file, if stop is False
        deletes the repetitive words in the bookmarks (the default).
        If it's successful then the pdf file will be overridden; otherwise
        error logs will be written in pdf_handler.log in the current 
        directory. If djvu switches the functionality to make djvu files. 
        """
    if djvu == True:
        djvu_handler(pdf)
    else:     
        ### based on jpdfbookmarks call, decides if we will trim or not ###     
        trim_txt = False    
        
        head_pdf = osp.split(pdf)[1][:10] 
        pdf_txt = pdf_trimmer(pdf, stop = False, sr = False)
        if not pdf_txt == 1: 
            trim_txt = True
        
        if stop_optimize == False:
            pdf_compress(pdf)
       
        if trim_txt == True:
            pdf_bookmarker(pdf, pdf_txt)
            sbp.call(["rm", pdf_txt])


if __name__ == "__main__":
    
    #####################################
    ## Command-line argument handling ###
    #####################################

    parser = argparse.ArgumentParser(description = 'pdf handler (bookmark\
            trimmer, optimization handling, djvu maker) tool for files \
            and directories. This is dependent on the tools: jpdfbookmarks,\
            ghostscript, and pdf2djvu.')
    parser.add_argument('pdf', help = "trims and optimizes \
            the bookmarks in this pdf file (or directory)." )  
    parser.add_argument("--djvu", action = "store_true", help = "Switches\
            the functionality to djvumaker. produces djvu files from\
            pdf files in the directory (or the pdf file). This calls\
            pdf2djvu program from Lizartech djvulibre (it should've been\
            installed in your system.)")
    parser.add_argument("-s", "--stop", action = "store_true", help = "\
            Stop cleaning self-evident words, e.g., Chapter, section, ..\
            in the beging of bookmarks.")
    parser.add_argument("-so", "--stop_optimize", action = "store_true", \
            help = "Stops trying to optimize the pdf file (the default \
            is otherwise).")
    parser.add_argument("-sr", "--stop_redundancy", action = "store_true",\
            help = "Stops cleaning redundant bookmarks (otherwise is the defaults).")
    args = parser.parse_args()
    
    work_dir = codecs.encode(os.getcwdu(), 'ascii')
    pdf2 = osp.join(work_dir, osp.split(args.pdf)[1])        
   
    if osp.isfile(args.pdf) or osp.isdir(args.pdf):
        pdf = osp.realpath(args.pdf)
    elif osp.isfile(pdf2) or osp.isdir(pdf2):
        pdf = pdf2
    else:
        raise ValueError('Invalid file or directory: %s\n' % args.pdf)

    # Checking dependency
    dependency_checker(djvu = args.djvu, jpdf = not(args.stop),\
                       gs = not(args.stop_optimize))

    ##############################
    ## log error handling setup ##
    ##############################
   
    if osp.isfile(pdf):
        log_path = osp.join(osp.dirname(pdf), "pdf_handler.log")
    elif osp.isdir(pdf):
        log_path = osp.join(pdf, "pdf_handler.log")

    logging.basicConfig(filename = log_path, filemode = "w",\
                        level = logging.DEBUG)
    
    ###############
    ##pdf dealing #
    ###############

    if osp.isfile(pdf):
        pdf_handler(pdf, args.stop, args.stop_optimize,\
                    args.stop_redundancy, args.djvu)
    
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
                    pdf_handler(ff, args.stop, args.stop_optimize, \
                                args.stop_redundancy, args.djvu)
        
        elif s.upper() in NO:
            print "Okay! May be next time!\n"
    else: 
        raise SyntaxError("You should determine if this is a file or directory, try with -h option for more info!")

    ######################
    ## Final log report ##
    ######################

    if osp.getsize(log_path) == 0:
        print "The job is done just fine!\n"
        sbp.call(["rm", log_path])
    else:
        warn = 0
        f = open(log_path)
        for line in f: 
            if fnmatch.fnmatch(line.upper(), "*WARNING*"): warn = warn + 1

        f.close()
        if warn == 0:
            print "The job done great, there're no warning!\n"
        else:    
            print "There were some warnings and errors, please look at the log-file %s \n" % osp.split(log_path)[1]


