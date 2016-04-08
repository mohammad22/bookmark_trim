
A bunch of command-line helper functions for pdf and djvu files (possibly the whole files in a directory). It can:

+ Trim and collapse the bookmarks of the files in the directory. 

+ Compress the `pdf` files in the directory, using `ghostscript`.

+  The 'trim', washes the redundant words, i.g., 'Chapter', 'Section', 'Appendix', ... from the bookmark titles. You can have your own collection of stop-words. (See more about this on help `pdf.sh -h`). You can alos disable the trimming functionality.

   Usage: 
   
* First `git clone` the repository, `cd` to that directory and do `cmod +x pdfb.sh`. Then make a smylink to the `pdfb.sh` on your environment path.
Now, for example: 


   `pdfb.sh path-to-pdf-file-or-directory -so`
   
   will trim the bookmarks. This functionality requires `jpdfbookmarks` on your machine.

* To Compress and trim the pdf files. This one needs `ghostscript` on your machine:

    `pdfb.sh path-to-pdf-file-or-directory -sw . `

* To use optimization without trimming bookmarks:
 
    `pdfb.sh  path-to-padf-file-or-directory -s`

+ Pdf2djvu for all the files of a directory (this is just a wrapper for the pdf2djvu utility for LizardTech, so it is needed to be installed). Also it picks some very specific parameters for `pdf2djvu` utility which I found generally useful for converting black-white pdfs to djvu, so use at your own risk.

    `python djvub.py path-to-the-pdf-files`

