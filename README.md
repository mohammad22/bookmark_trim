
A bunch of command-line helper functions for pdf and djvu files (possibly the whole files in a directory). It can:

+ Trim and collapse the bookmarks of the files in the directory. 
  The 'trim' functionality, washes the redundant words like 'Chapter', 'Section', 'Appendix' from the bookmark titles. You can have your own collection of stop-words to be washed from bookmark titles which should be declared as parameter on command line (See help of the command line function). You can alos disable the trimming functionality.

   If you have smylinked the file `pdfb.sh` in your path then:
   `pdfb.sh -so path-to-pdf-file-or-directory`
   will trim the bookmarks. This functionality requires `jpdfbookmarks` on your machine.

+ Compress and trim the pdf files. This one needs `ghostscript` on your machine:
`pdfb.sh path-to-pdf-file-or-directory`

+ Pdf2djvu for all the files of a directory (this is just a wrapper for the pdf2djvu utility for LizardTech, so it is needed to be installed). Also it picks some very specific parameters for `pdf2djvu` utility which I found generally useful for converting black-white pdfs to djvu, so use at your own risk.

`python djvub.py path-to-the-pdf-files`

