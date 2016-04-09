
A bunch of command-line helper functions for pdf and djvu files (possibly the whole files in a directory). It can:

+ Trim and collapse the bookmarks of the files in the directory. 

+ Compress the `pdf` files in the directory, using `ghostscript`.

+  The 'trim', washes the redundant words, i.g., 'Chapter', 'Section', 'Appendix', ... from the bookmark titles. You can have your own collection of stop-words. (See more about this in help: `pdf.sh -h`). You can disable the trimming.

   Usage: 
   
* First `git clone` the repository, `cd` to the cloned directory make `pdfb.sh` file executable: `cmod +x pdfb.sh` (For your convenience make a smylink to `pdfb.sh` on your environmet path).
Now, for example: 


   `pdfb.sh pdf-dir -so`
   
   will trim the bookmarks, without optimizing the pdf file. This requires [`jpdfbookmarks`](http://flavianopetrocchi.blogspot.com/) on your machine.

* To Compress and trim the pdf files with default stop_words. This needs `ghostscript` on your machine (which by default is available on almost all distributions):

    `pdfb.sh pdf-dir`

* To trim the word "dummy" from the beginging of bookmark titles:

    `pdfb.sh pdf-dir -w dummy`

* To use optimization without trimming bookmarks:
 
    `pdfb.sh  pdf-dir -s`

+ Pdf2djvu for all the files of a directory (this is just a wrapper for the pdf2djvu utility for [LizardTech](https://www.lizardtech.com/) (so, it should be available on your machine). Also it picks some very specific parameters for `pdf2djvu` utility which I found generally useful for converting black-white pdfs to djvu, so use at your own risk.

    `python djvub.py pdf-dir`

+ To just trim the word "dummy" without optimization:

    `pdfb.sh pdf-dir -so -w dummy`
