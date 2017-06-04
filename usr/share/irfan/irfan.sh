#!/bin/sh
# File: /usr/share/irfan/irfan.sh
# Author: bgstack15@gmail.com
# Startdate: 2016-01-29
# Title: Wrapper script for passing files to Irfanview
# Purpose: Converts file paths to a wine format and also handles compressed files
# History: 2016-01-29 Initial quick script written. It used a bunch of sed commands to transform paths to a wine format.
# Usage: irfan /path/to/image /another/image/file
# Reference:
#    Ideas for zip expansion and winepath https://github.com/Zykr/IrfanViewLinux/blob/master/irfanview
# Improve:
export WINEPREFIX=$HOME/.wine
devtty=/dev/null

irfanversion="2017-06-04a"

# Define functions
expandword() {
   # call: expandword "${word}"
   # if file, add it
   # if directory, expand it
   # if tarball, extract it and operate on the directory like normal
   local _word="$( echo "${@}" | sed -e 'sF\/\/F\/Fg;' )"
   if test -d "${_word}";
   then
      # loop through all files in the directory
      for _newword in "${_word}"/*;
      do
         expandword "${_newword}";
      done
   elif test -f "${_word}";
   then
      # file exists so check if tarball
      case "${_word}" in
         *.tgz|*.tar.gz)
            # extract it and expand the temporary directory
            _tmpdir="$( mktemp -d )"; alltempdirs="${alltempdirs} ${_tmpdir}"
            echo "tmpdir ${_tmpdir}" 1>${devtty}
            tar -zx -C "${_tmpdir}" -f "${_word}" 1>${devtty} 2>&1
            expandword "${_tmpdir}"
            ;;
         *.zip)
            _tmpdir="$( mktemp -d )"; alltempdirs="${alltempdirs} ${_tmpdir}"
            echo "tmpdir ${_tmpdir}" 1>${devtty}
            echo "7za e -w${_tmpdir} ${_word}" 1>${devtty} 2>&1
            ( cd "${_tmpdir}"; 7za e "${_word}" 1>${devtty} 2>&1; )
            expandword "${_tmpdir}"
            ;;
         *)
            # assume it is readable and add it to list of files to open
            echo "File ${_word}" 1>${devtty}
            thisfile="$( getwinepath "${_word}" )"
            irfanfiles="${irfanfiles} \"${thisfile}\""
            ;;
      esac
   fi
}

getwinepath() {
   # call: getwinepath "$foo"
   winepath -w "${@}"
}

# Define variables
alltempdirs=""
exec_name="i_view32.exe"
exec_path="/usr/share/irfan/irfanview/i_view32.exe"

# prepare files
irfanargs=
irfanfiles=

for word in "${@}";
do
   expandword "${word}"
done
irfanfiles="${irfanfiles## }"

# run wine
cd $WINEPREFIX
echo "${irfanfiles}" | xargs echo wine "${exec_path}" ${irfanargs} > ${devtty}
echo "${irfanfiles}" | xargs wine "${exec_path}"  ${irfanargs} &

wait $( pgrep -P $$ ${exec_name} )
for thistempdir in ${alltempdirs};
do
   rm -rf "${thistempdir}" 1>${devtty}
done
