#!/bin/sh

DIR="$(dirname "$(readlink -f "$0")")"
python "$DIR/pdfb_trim.py" $*
