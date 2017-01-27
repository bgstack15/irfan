#!/bin/sh
# File: /usr/share/irfan/irfan.sh
# Author: bgstack15@gmail.com
# Startdate: 2016-01-29
# Title: Wrapper script for passing files to Irfanview
# Purpose: Converts file paths to a wine format and also handles compressed files
# History: 2016-01-29 Initial quick script written. It used a bunch of sed commands to transform paths to a wine format.
#    2017-01-17 
# Usage: irfan /path/to/image /another/image/file
# Reference:
#    https://github.com/Zykr/IrfanViewLinux/blob/master/irfanview
# Improve:
#    handle zip/tar files
#    write a function that expands file list.
export WINEPREFIX=$HOME/.wine
devtty=/dev/pts/3

# prepare files
irfanargs=
irfanfiles=
if test -n "$1";
then
   for word in "$@";
   do
      echo "File ${word}" > ${devtty}
      thisfile="$( winepath -w "${word}" )"
      irfanfiles="${irfanfiles} \"${thisfile}\""
   done
fi
irfanfiles="${irfanfiles## }"

# run wine
cd $WINEPREFIX
echo "${irfanfiles}" | xargs echo wine /usr/share/irfan/irfanview/i_view32.exe ${irfanargs} > ${devtty}
echo "${irfanfiles}" | xargs wine /usr/share/irfan/irfanview/i_view32.exe ${irfanargs}
