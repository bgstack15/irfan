#!/bin/sh
# File: /usr/share/irfan/install-irfanview.sh
# Author: bgstack15
# Startdate: 2016-11-28 10:46
# Title: Script that Installs irfanview
# Purpose: Downloads and installs irfanview from official source
# Package: irfan
# History:
# Usage: Is called during the rpm install phase of the irfan package. Also generally available.
# Reference:
# Improve:

# Definitions
infile=/usr/share/irfan/inc/irfan_ver.txt
outdir=/usr/share/irfan/irfanview
iver="" # dynamically defined by /usr/share/irfan/inc/irfan_ver.txt
temp_iview=/usr/share/irfan/source/iview.zip
temp_plugins=/usr/share/irfan/source/irfanview_plugins.zip
ini_source=/usr/share/irfan/inc/i_view32.ini
ini_dest=/usr/share/irfan/irfanview/i_view32.ini
sha256sumfile=/usr/share/irfan/inc/sha256sum.txt

# Functions
getsource() {
   # call: getsource http://sourcefile /tmp/destfile
   # will be fatal failure
   # will check the sha256sum file to ensure good download
   _gssource="${1}"
   _gstemp="${2}"
   echo "Fetching ${_gssource}"
   # get published sha256sum of good file
   _goodsha=$( awk -e "\$2 == \"${_gssource##*/}\" {print;}" sha256sumfile 2>/dev/null )
   touch "${_gstemp}" 2>/dev/null || { echo "Cannot modify ${_gstemp}. Run as root, perhaps. Aborted."; exit 1; }
   _attempts=0
   _state="";
   while test ${_attempts} -lt 5;
   do
      curl "${_gssource}" --progress-bar --refer "${_gssource}" > "${_gstemp}"
      # verify good download
      if ! test -f "${_gstemp}" || test "$( stat -c "%s" "${_gstemp}" 2>/dev/null)" -lt 1000 || ! test "$( sha256sum "${_gstemp}" | cut -d' ' -f1 )" = "${_goodsha}";
      then
         case "${_attempts}" in
            #1) . ~/.bashrc 1>/dev/null 2>&1;; # was breaking weirdly on some interal definition
            2) test -x /usr/bgscripts/bgscripts.bashrc && . /usr/bgscripts/bgscripts.bashrc --noglobalprofile 1>/dev/null 2>&1;;
            3) unset http_proxy; unset https_proxy; _gssource=$( echo "${_gssource}" | sed -e 's/\(www\.\)\?irfanview\.info\/files/mirror\.example\.com\/bgscripts\/irfanview/;' 2>/dev/null );;
            5) echo "File failed to download: ${_gssource}. Aborted." && exit 1;;
         esac
      else
         exit 0 # valid because inside a function
      fi
      (( _attempts = _attempts + 1 ))
   done
}

# Ensure target directories exists
if ! test -d "${outdir}/source";
then
   mkdir -p "${outdir}/source" || { echo "Unable to make directory ${outdir}. Aborted."; exit 1; }
fi

# Get irfanview version to install.
if ! test -f "${infile}";
then
   echo "Is irfan package installed? Check ${infile}. Aborted."
   exit 1
fi
while read line;
do
   line=$( echo "${line}" | sed -e 's/^\s*//;s/\s*$//;/^[#$]/d;s/\s*[^\]#.*$//;' )
   if test -n "${line}";
   then
      echo "Config file reports version number ${line}."
      iver="${line}"
   fi
done < "${infile}"
sourcefile="http://irfanview.info/files/iview${iver//./}.zip"
pluginssourcefile="http://irfanview.info/files/irfanview_plugins_${iver//./}.zip"

# Check dependencies
if ! test -x "$( which curl 2>/dev/null)";
then
      # try wget maybe?
   echo "Please install curl. Aborted."
   exit 1
fi
if ! test -x "$( which 7z 2>/dev/null)";
then
   # try wget maybe?
   echo "Please install 7zip. Try package p7zip. Aborted."
   exit 1
fi

# Fetch irfanview source itself
getsource "${sourcefile}" "${temp_iview}"

# Fetch plugins source
getsource "${pluginssourcefile}" "${temp_plugins}"

# Extract irfanview
echo "Extracting irfanview."
7z x -o"${outdir}" -y "${temp_iview}" 1>/dev/null 2>&1 && rm -rf "${temp_iview}" 2>/dev/null || { echo "Unable to extract for some reason. Aborted."; exit 1; }

# Extract plugins
echo "Extracting plugins."
7z x -o"${outdir}/Plugins" -y "${temp_plugins}" >/dev/null 2>&1 && rm -rf "${temp_plugins}" 2>/dev/null || { echo "Unable to extract plugins. You might experience limited functionality."; }

# Adjust permissions on the directories
chmod -R 0755 "${outdir}/Plugins" "${outdir}/Languages" "${outdir}/Toolbars"

# Initialize i_view32.ini
if test -f "${ini_source}";
then
   /bin/cp -p "${ini_source}" "${ini_dest}" 2>/dev/null && { echo "Initialized the i_view32.ini file."; }
fi
chmod 0666 "${ini_dest}" 2>/dev/null

# Provide final status notification
echo "irfan ${iver} successfully installed."
exit 0
