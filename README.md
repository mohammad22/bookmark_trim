
A bunch of command-line helper functions for pdf and djvu files (possibly the whole files in a directory). It can:

+ Trim and collapse the bookmarks of the files in the directory ().  

   If you have smylinked the file `pdfb.sh` in your path then:
   `pdfb.sh -so path-to-pdf-file-or-directory`
   will trim the bookmarks. This functionality requires `jpdfbookmarks` has been installed on your machine.

+ Compress and trim the pdf files. This one needs `ghostscript` to available on your machine:
`pdfb.sh path-to-pdf-file-or-directory`

+ Pdf2djvu for all the files of a directory (this is just a wrapper for the pdf2djvu utility for LizardTech, so it is needed to be installed). Also it picks some very specific parameters for `pdf2djvu` utility which I found generically useful for converting black-white pdf-to-djvu, so use at your own risk.

`python djvub.py path-to-the-pdf-files`

