import re
import os
import codecs
import sys
import os.path as osp
import argparse
import fnmatch

def expand_l(word, a):
    """ based on word, splits all the nested strings in a, each is replaced with the list of splitted strings."""
    for i, x in enumerate(a): 
        if type(x) == str:
            x = x.split(word)
            a[i] = x
        elif type(x) == list:
            expand_l(word, x)

def unitype_l(t, l):
    """returns True if every element of the list l is of type t, otherwise returns False""" 
    if len(l) == 1: return type(l[0]) == t
    elif len(l) > 1: return (type(l[0]) == t) and unitype_l(t, l[1:len(l)])
    else: return False
 
def contract_l(word, a):
    """returns a contracted version of a, all the nested lists of a containing only strings are contracted with word in between"""
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
    """ appends a concatenation of the word plus the last element of the list a into list a, and repeats this procedure 20 times """ 
    l = len(a)
    if l < 20:
        a.append(a[l - 1] + word)
        rec_l(a, word)

def max_match(s, t):
    """ returns the maximum index i such that the string s contains pattern t[i]. If there is no match it returns -1. """   
    a = -1
    while fnmatch.fnmatch(s, '*' + t[a + 1] + '*'): a = a + 1
    return a

def n_tab(a, i):
    """ Retruns the number of tabs in the ith bookmark of a.
    """
    tt = ['\t']
    rec_l(tt, '\t') 
    return max_match(a[i][0][0], tt)

def is_deeper(a, i, j):
    """ for i > j is true if the tabs in ith  bookmark is more than jth; otherwise it is false.   
    """
    if (i - j) >= 1:
        return n_tab(a, i) > n_tab(a, j)
    else:
        return False

def is_child(a, i, j):
    """ for i > j, is true if i-th line of the bookmark a is a child of j-th; False otherwise. for i = j it is true, otherwise it is false.
    """
    if (i - j) > 1:
        return (is_child(a, i - 1, j) and is_deeper(a, i, j))
    elif i == (j + 1):
        return is_deeper(a, i, j) 
    elif i == j:
        return True
    else: 
        return False

def youngest_child(a, j, **info): 
    """ In the bookmark a, returns the greastest  i such that the i-th line is a child of j. If j has no child, returns j (unless a is empty which then returns -1). At each state info = {'Y': Y, 'O': O} we know O <= youngest < Y. 
    """
    Y = info['Y'] 
    O = info['O']
    l = O + ((Y - O) / 2)
    
    if Y == -1: return Y
    elif l == O: return O
    elif is_child(a, l, j): O = l
    else: Y = l  
    
    return youngest_child(a, j, Y = Y, O = O)

def redundant_parent(a, i):
    """
    Returns a tuple (B, Youngest); where B is True if bookmark i and i+1 are essentially the parents of the same set of childs; otherwise it is False. And Youngest is the index of the Youngest child of i if this index is greater than i, otherwise it is i + 1.  
    """

    y = youngest_child(a, i, Y = len(a) - 1, O = i)
    yy = max(y, i + 1)
    B = False
    
    if i < (len(a) - 2) and\
       is_child(a, i + 1, i) and\
       is_child(a, i + 2, i + 1) and\
       y == youngest_child(a, i + 1, Y = len(a) - 1, O = i + 1): 
        B = True

    return (B, yy)

def clean_redundant_parent(a, i):
    """ If bookmark i is redundant parent, then it will be eliminated from \
            bookmark a. one tab will be droped from all its childs.\
            It returns the index of the youngest child of i if it is greater than i otherwise returns i + 1.
    """
    Redundancy_i = redundant_parent(a, i)
    if Redundancy_i[0]:
        for j in range(i + 1, Redundancy_i[1] + 1):
            a[j][0][0] = a[j][0][0][1:]    
      
        del a[i] 
        return (Redundancy_i[1] - 1)
    else:
        return Redundancy_i[1]

def clean_redundancy(a, i):
    """ Cleans the potential redundant parent i from a and recursively \
            moves on from there. This is done for at most one nested \
            redundant child of i; the inspection of the childs of childs\
            of i is skipped. Cleaning continues from the youngest child\
            of i (or i + 1; if youngest child of i = i)after that.
    """
    c = clean_redundant_parent(a, i)
    if c < len(a) - 1:
        clean_redundancy(a, c + 1)
        


def bookmark_trim(file1 = None, stop = False, sr = False):
    """ Takes the name of a text file file1 = "f.txt" which should be a bookmark text file created by jpdfbookmark app, creates a trimmed text file file2 = "file_new.txt" in the same path as file1. It also takes the second boolean argument stop; when it's False (the default) it will trim the reptetive words (e.g., Chapter, Section, Part, ...) from the beging of the bookmark texts, otherwise it does nothing."""
    
    u = osp.splitext(file1)
    file2 = u[0] + '_new' + u[1]
    
    f = open(file1, 'r')
    g = open(file2, 'w')
    
    a = []
    
    stop_words = ['Chapter:', 'Chapter', 'Part:', 'Part','Appendix:', 'Appendix', 'Sub-section:','Sub-section', 'Subsection:' ,'Subsection', 'Section:', 'Section', 'Lecture:', 'Lecture']    
    
    
    for line in f: a.append(line)
    f.close()
       
    expand_l('/', a)
    expand_l(' ', a)

    
    for i in range(len(a) - 1):
        if is_deeper(a, i + 1, i): 
            a[i][1][0] = a[i][1][0].replace(',open,', ',closed,')
        else:
            a[i][1][0] = a[i][1][0].replace(',closed,', ',open,')
    
    if stop == False:    
        for i in range(len(a)):
            for word in stop_words:
                a[i][0][0] = re.sub(word, '', a[i][0][0], flags = re.IGNORECASE)
    
    if sr == False:  clean_redundancy(a, 0)

    a = contract_l(' ', a)
    a = contract_l('/', a)   
    
    
    for line in a:
        g.write(line)
    g.close()
    

def main(file1, stop, sr): 
    """To see the documentation, call the command "python bookmark-trim.py -h" from the command line."""
    
    
    bookmark_trim(file1, stop, sr)

if __name__ == '__main__':


    parser = argparse.ArgumentParser(description = "Trims the bookmark text 'file1', and writes the trimmed bookamrk file in a new file 'file1_new'. if the flag --stop (-s) is on, then cleaning selfevident words, e.g., Chapter, Section, Part, ...,  willbe de-activated as well (the opposite is the default). if the flag --stop_redundancy (--sr) is on, then cleaning redundant boojmarks will be stopped (the opposite is the default).")

    parser.add_argument("file1", help = "Name of a text-file. Trims the bookmark in this text file.", type = str)
    parser.add_argument("-s", "--stop", action = "store_true", help = "Stops cleaning self-evident words, e.g., Chapter, section, .. in the beging of bookmarks.")
    parser.add_argument("-sr", "--stop_redundancy", action = "store_true",\
            help = "Stops huristic cleaning the redundant bookmarks, the opposite is the default.")
    args = parser.parse_args()
    
    work_dir = codecs.encode(os.getcwdu(), 'ascii')
    pdf2 = osp.join(work_dir, osp.split(args.file1)[1])        
   
    if osp.isfile(args.file1):
        pdf = osp.realpath(args.file1)
    elif osp.isfile(pdf2): 
        pdf = pdf2
    else:
        raise ValueError('Invalid file or directory: %s\n' % pdf)
    
    
    if osp.exists(pdf):
        main(pdf, args.stop, args.stop_redundancy)
    else: 
        print("The filename %s should refer to an existinf file!\n " % pdf)
