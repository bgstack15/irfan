#!/bin/sh
# file: /usr/share/irfan/inc/irfan-vlc.sh
# purpose: to correct filenames if passed to an external editor from wine-irfan.
devtty=/dev/null
a="$@"
vlcargs=
{
for word in "$@";
do
   newword=$( echo "${word##Z:}" | sed 's!\\!\/!g;' )
   vlcargs="${vlcargs} ${newword}"
   #echo "vlcargs=${vlcargs}"
done
vlcargs="${vlcargs## }"
/usr/bin/vlc "${vlcargs}"
} > ${devtty}
