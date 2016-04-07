
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


def pdf_trimmer(pdf, stop = False, stop_optimize = False, stop_words):
    """ takes the path of a valid pdf file as pdf and trims its bookmarks
        and optimizes if asked.
        If stop is True it does not clean the repetitive words of the
        bookmarks; otherwise it does (this is the default behaviour).
        If stop_optimize is True it does not try to optimize the pdf file
        otherwise it tries to optimize (which is the default).
    """
    try:
        a = sbp.check_output(["jpdfbookmarks", "-d", pdf]) 
        worked = True 
    except:
        logging.warning("No trimming! something's wrong with the bookmarks\
                of: %s", osp.split(pdf)[1][:10] + '...')
        worked = False

    if worked == True:            
        o = osp.splitext(osp.realpath(pdf))
        txt_pdf = '_'.join([o[0], ".txt"]) 
        f = file(txt_pdf, "w")
        f.write(a)
        f.close()
        """Creating a trimmed bookmark file txt_pdf[-.txt]_new.txt
        """
        bmt.bookmark_trim(txt_pdf, stop = stop, stop_words = stop_words)
        new_pdf = '_'.join([o[0], "new", o[1]]) 
        u = osp.splitext(osp.realpath(txt_pdf))
        new_txt_pdf = u[0] + '_new' + u[1]
        
        ## Optimize the pdf file (if asked for it).
        if stop_optimize == False:
            pdf_compress(pdf)
        
        ## Creating the new trimmed bookmarks     
        sbp.call(["jpdfbookmarks", "-a", new_txt_pdf, "-o", new_pdf,\
                    pdf])

        if osp.isfile(new_pdf):
            worked = True 
        else:    
            logging.warning("Could not edit bookmarks! Most likely the file\
                    is encrypted..")
            worked = False
        
        if worked == True:
            sbp.call(["rm", pdf])
            sbp.call(["mv", new_pdf, pdf])
            sbp.call(["rm", txt_pdf])
            sbp.call(["rm", new_txt_pdf])
            logging.info("Sucessfully trimmed the bookmarks of %s", \
                    osp.split(pdf)[1][:10] + '...')
        else:
            sbp.call(["rm", txt_pdf])
            sbp.call(["rm", new_txt_pdf])


def pdf_compress(pdf):
    """ Tries to optimize the pdf file, in case of success it overrides 
        the existing file; otherwise, it does nothing. 
    """    
    o = osp.splitext(osp.realpath(pdf))
    new_pdf = '_'.join([o[0], "new", o[1]]) 
    sbp.call(["gs",\
              "-o", new_pdf,\
              "-sDEVICE=pdfwrite",\
               "-dNOPAUSE",\
               "-q",\
               "-dPdfSize=/screen",\
               pdf])
    if osp.isfile(new_pdf) & (osp.getsize(new_pdf) < osp.getsize(pdf)):
        logging.info("Sucessfuly compressed the file: %s", \
                osp.split(pdf)[1][:10] + '...') 
        sbp.call(["rm", pdf])
        sbp.call(["mv", new_pdf, pdf])
    else:
        logging.warning("The compression of %s was not sucessful!",\
                osp.split(pdf)[1][:10] + '...')
        sbp.call(["rm", new_pdf])

       

if __name__ == "__main__":
    
    #####################################
    ## Command-line argument handling ###
    #####################################

    parser = argparse.ArgumentParser(description = 'pdf handler (bookmark,\
            optimization handling). The positional argument is: pdf.\
            It should be a valid pdf-file or a directory.\
            These are exclusive options. If pdf is a directory\
            all the pdf files in this  directory will be treated.')
    parser.add_argument('pdf', help = "trims and tries to optimize \
            the bookmarks in this pdf file (or directory)." )  
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-s", "--stop", action = "store_true", help = "Stops cleaning self-evident words, e.g., Chapter, section, .. in the beging of bookmarks.")
    group.add_argument("-w","--stop_words", metavar = 'stop_words', nargs ='+', default=None, help='list of stop_words to trim from the begining of the bookmark titles, this option is chosen and is set to ".", then the default will be used:\n [Chapter, Section, Subsection, Part, Appendix].' )
 
    parser.add_argument("-so", "--stop_optimize", action = "store_true", \
            help = "Stops trying to optimize the pdf file (the default)\
            is otherwise.")
    args = parser.parse_args()

   

    work_dir = os.getcwd()
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
        pdf_trimmer(pdf, args.stop, args.stop_optimize, args.stop_words)
    
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
                    pdf_trimmer(ff, args.stop, args.stop_optimize, args.stop_words)
        
        elif s.upper() in NO:
            print "Okay! May be next time!\n"
    else: 
        raise SyntaxError("You should determine if this is a file or directory, try with -h option for more info!")

