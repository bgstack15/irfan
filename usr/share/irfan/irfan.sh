#!/bin/sh
# for Irfan rpm
# packaged 2016-01-27 bgstack15@gmail.com
export WINEPREFIX=$HOME/.wine
cd $WINEPREFIX
devtty=/dev/null

# prepare files
irfanargs=
if [[ -n "$@" ]];
then
   for word in "$@";
   do
      fullfilename="$( printf "z:${word}" | sed 's!\/!\\!g;' )"
      echo "${fullfilename}" > ${devtty}
      irfanargs="${irfanargs} ${fullfilename}"
   done
fi
irfanargs="${irfanargs## }"

# run wine
wine /usr/share/irfan/irfanview/i_view32.exe "${irfanargs}"
