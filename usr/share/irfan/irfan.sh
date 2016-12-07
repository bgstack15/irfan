#!/bin/sh -x
# for Irfan rpm
# packaged 2016-01-27 bgstack15@gmail.com
export WINEPREFIX=$HOME/.wine
devtty=/dev/pts/3
echo "currentdir=$( pwd )" > ${devtty}

# prepare files
irfanargs=
irfanfiles=
if test -n "$1";
then
   for word in "$@";
   do
      echo "word=${word}" > ${devtty}
      #thisfile="$( printf "${word}" | sed -e '/^.$/d;' -e "s!^\.\?!$( pwd )\/!;" -e 's/^/z:/;' -e 's!\/!\\!g;' -e 's!\\\+!\\!g;' )"
      thisfile="$( printf "${word}" | sed -e '/^.$/d;s!^\.!!;' )"
      echo "${thisfile}" | grep -qiE "^/" && : || thisfile="$( printf "%s%s" "$( pwd )/" "${thisfile}" )"
      thisfile="$( echo "${thisfile}" | sed -e 's!^!z:/!;s!\/!\\!g;s!\\\+!\\!g;' )"
      echo "thisfile=${thisfile}" > ${devtty}
      if test ! -d "${word}";
      then
         echo "${thisfile}" > ${devtty}
         irfanfiles="${irfanfiles} \"${thisfile}\""
      fi
   done
fi
irfanfiles="${irfanfiles## }"

# run wine
cd $WINEPREFIX
#echo wine /usr/share/irfan/irfanview/i_view32.exe ${irfanargs} "\"${irfanfiles}\"" >${devtty}
#wine /usr/share/irfan/irfanview/i_view32.exe ${irfanargs} "${irfanfiles}"
echo "${irfanfiles}" | xargs echo wine /usr/share/irfan/irfanview/i_view32.exe ${irfanargs} > ${devtty}
echo "${irfanfiles}" | xargs wine /usr/share/irfan/irfanview/i_view32.exe ${irfanargs}
