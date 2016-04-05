#!/bin/sh

DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

python $DIR\/pdfb_trim.py $*
