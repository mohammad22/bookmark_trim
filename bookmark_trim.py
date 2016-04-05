import re
import codecs
import sys
import os.path as osp
import argparse
import fnmatch

def expand_l(word, a):
    
    """ 
    based on word, splits all the nested strings in a, each is replaced 
    with the list of splitted strings.
    """
    for i, x in enumerate(a): 
        if type(x) == str:
            x = x.split(word)
            a[i] = x
        elif type(x) == list:
            expand_l(word, x)

def unitype_l(t, l):
    
    """
    returns True if every element of the list l is of type t, otherwise
    returns False
    """ 
    if len(l) == 1: return type(l[0]) == t
    elif len(l) > 1: return (type(l[0]) == t) and unitype_l(t, l[1: len(l)])
    else: return False
 
def contract_l(word, a):
    
    """
    returns a contracted version of a, all the nested lists of a 
    containing only strings are contracted with word in between
    """
    if unitype_l(str, a): 
        a = word.join(a)
        return a
    else:
        b = []
        for i, x in enumerate(a):
            if type(x) == list: b.append(contract_l(word, x)) 
            else: b.append(x)
        return b

def rec_l(a, word):
    
    """ 
    appends a concatenation of the word plus the last element of the list 
    a into list a, and repeats this procedure 20 times 
    """ 
    l = len(a)
    if l < 20:
        a.append(a[l - 1] + word)
        rec_l(a, word)

def max_match(s, t):
    
    """ returns the maximum index i such that the string s contains pattern
    t[i]. If there is no match it returns -1. 
    """   
    a = -1
    while fnmatch.fnmatch(s, '*' + t[a + 1] + '*'): a = a + 1
    return a
                

def bookmark_trim(file1 = None, stop = False):
    
    """ 
    Creates a trimmed text file file2 = "file_new.txt" in the same path
    as file1. It also takes the second boolean argument stop; when it's
    False (the default) trims the reptetive words (e.g., Chapter, Section,
    Part, ...) from the beging of the bookmark texts, otherwise it does
    nothing.
    """
    
    u = osp.splitext(osp.realpath(file1))
    file2 = u[0] + '_new' + u[1]
    
    f = open(file1, 'r')
    g = open(file2, 'w')
    
    a = []
    
    stop_words = ['Chapter:', 'Chapter', 'Part:', 'Part','Appendix:', 'Appendix', 'Sub-section:','Sub-section', 'Subsection:' ,'Subsection', 'Section:', 'Section']    
    
    tt = ['\t']
    rec_l(tt, '\t') 
    
    for line in f: a.append(clean_tabs(line))

    f.close()
       
    expand_l('/', a)
    expand_l(' ', a)

    
    for i in range(len(a) - 1):
        if max_match(a[i][0][0], tt) < max_match(a[i + 1][0][0], tt):
            a[i][1][0] = a[i][1][0].replace(',open,', ',closed,')
        else:
            a[i][1][0] = a[i][1][0].replace(',closed,', ',open,')
    
    if stop == False:    
        for i in range(len(a)):
            for word in stop_words:
                if not word == 'Appendix':
                    a[i][0][0] = re.sub(word, '', 
                                          a[i][0][0], 
                                          flags = re.IGNORECASE)
                else:
                    pattern = re.compile(r'Appendixes[:|\s]*')
                    if not len(re.findall(pattern, a[i][0][0])) > 0:
                        a[i][0][0] = re.sub(word, '', a[i][0][0], 
                                    flags = re.IGNORECASE)
    
    a = contract_l(' ', a)
    a = contract_l('/', a)   
    
    
    for line in a:
        g.write(line)
    g.close()
  

def clean_tabs(txt):
    """
    Strips all the non-starting tabs from txt.
    """
    pattern = re.compile(r'([^\t]+)(\t+)')
    new_txt = pattern.sub(r'\1 ', txt)
    
    return new_txt


def main(file1, stop): 
    """
    See the documentation, on the command-line "python bookmark-trim.py -h".
    """
    bookmark_trim(file1, stop)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Trims the bookmark text\
            'file1', and writes the trimmed bookamrk file in a new file\
            'file1_new'. if the flag --stop (-s) is on, then cleaning \
            selfevident words, e.g., Chapter, Section, Part, ...,  will be\
            de-activated as well (the opposite is the default).")
    parser.add_argument("file1", help = "Trims the bookmark in this text \
            file.", type = str)
    parser.add_argument("-s", "--stop", action = "store_true", help =\
            "Stops cleaning self-evident words, e.g., Chapter, section, ..\
            in the beging of bookmarks.")
    args = parser.parse_args()
    if osp.exists(args.file1):
        main(args.file1, args.stop)
    else: 
        print "The filename ", args.file1, " should refer to an existing\
                file!\n"
