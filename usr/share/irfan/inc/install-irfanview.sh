#!/bin/sh
# File: /usr/share/irfan/install-irfanview.sh
# Author: bgstack15
# Startdate: 2016-11-28 10:46
# Title: Script that Installs irfanview
# Purpose: Downloads and installs irfanview from official source
# Package: irfan
# History: 2016-12-06 modified to work properly during the rpm install phase, which is part of building the rpm and not actually deploying the rpm to a system.
#    2017-01-02 referenced freefilesync.rpm file install-ffs.sh
#    2017-01-23 made more generic and updated for bgscripts's new location
#    2017-03-15 updated to smith122rpm location
#    2017-10-18 updated to match new directory structure
# Usage: Is used during the rpm build phase. It is also generally available.
# Reference:
# Improve:

# Definitions
package="irfan"
infile=${RPM_BUILD_ROOT}/usr/share/${package}/inc/${package}_ver.txt
outdir=${RPM_BUILD_ROOT}/usr/share/${package}/irfanview
pver="" # dynamically defined by /usr/share/${package}/inc/${package}_ver.txt
temp_sw=${RPM_BUILD_ROOT}/usr/share/${package}/source/iview.zip
temp_plugins=${RPM_BUILD_ROOT}/usr/share/${package}/source/irfanview_plugins.zip
ini_source=${RPM_BUILD_ROOT}/usr/share/${package}/inc/i_view32.ini
ini_dest=${RPM_BUILD_ROOT}/usr/share/${package}/irfanview/i_view32.ini
sha256sumfile=${RPM_BUILD_ROOT}/usr/share/${package}/inc/sha256sum.txt

# Functions
getsource() {
   # call: getsource http://sourcefile /tmp/destfile
   # will be fatal failure
   # will check the sha256sum file to ensure good download
   _gssource="${1}"
   _gstemp="${2}"
   echo "Fetching ${_gssource}"
   # get published sha256sum of good file
   _tmp=$( echo "${_gssource}" | sed -e 's!^.*\/!!' )
   _goodsha=$( awk "\$2 == \"${_tmp}\" {print;}" ${sha256sumfile} 2>/dev/null | cut -d' ' -f1 )
   touch "${_gstemp}" 2>/dev/null || { echo "Cannot modify ${_gstemp}. Run as root, perhaps. Aborted."; exit 1; }
   _attempts=0
   _state="";
   while test ${_attempts} -le 5;
   do
      curl "${_gssource}" --progress-bar --refer "${_gssource}" > "${_gstemp}"
      # verify good download
      if ! test -f "${_gstemp}" || test "$( stat -c "%s" "${_gstemp}" 2>/dev/null)" -lt 1000 || ! test "$( sha256sum "${_gstemp}" | cut -d' ' -f1 )" = "${_goodsha}";
      then
         case "${_attempts}" in
            #1) . ~/.bashrc 1>/dev/null 2>&1;; # was breaking weirdly on some interal definition
            2) test "$( ps -p $$ | xargs | awk '{print $NF}')" = "bash" && test -x /usr/share/bgscripts/bgscripts.bashrc && . /usr/share/bgscripts/bgscripts.bashrc --noglobalprofile 1>/dev/null 2>&1;;
            3) unset http_proxy; unset https_proxy; _gssource=$( echo "${_gssource}" | sed -e 's!'"${source1search}"'!'"${source1replace}"'!;' 2>/dev/null );;
            5) echo "File failed to download: ${_gssource}. Aborted." && exit 1;;
         esac
      else
         break
      fi
      _attempts=$(( _attempts + 1 ))
   done
}

extract() {
   # determine if tgz/tar.gz or other (use 7zip)
   # call: extract "${outdir}" -y "${temp_sw}"
   # available vars: ${command_7z}
   _outdir="${1}"
   _y="${2}" # should be a dash y
   _temp_sw="${3}"
   case "${_temp_sw##*.}" in
      tar|gz|tgz) # use tar -zxf
         tar -zx -C "${_outdir}" -f "${_temp_sw}"
         ;;
      *) # use command_7z
         ${command_7z} x -o"${_outdir}" "${_y}" "${_temp_sw}"
         ;;
   esac
}

# Ensure target directories exists
if ! test -d "${outdir}/../source";
then
   mkdir -p "${outdir}/../source" || { echo "Unable to make directory ${outdir}. Aborted."; exit 1; }
fi

# Get software version to install.
if ! test -f "${infile}";
then
   echo "Is ${package} package installed? Check ${infile}. Aborted."
   exit 1
fi
while read line;
do
   line=$( echo "${line}" | sed -e 's/^\s*//;s/\s*$//;/^[#$]/d;s/\s*[^\]#.*$//;' )
   if test -n "${line}";
   then
      echo "Config file reports version number ${line}."
      pver="${line}"
   fi
done < "${infile}"
tmp1=$( echo "${pver}" | tr -d '.' )
sourcefile="http://irfanview.info/files/iview${tmp1}.zip"
pluginssourcefile="http://irfanview.info/files/irfanview_plugins_${tmp1}.zip"
source1search='\(www\.\)?irfanview\.info\/files'
source1replace='albion320\.no-ip\.biz\/smith122\/repo\/rpm\/irfan'

# Check dependencies
if ! test -x "$( which curl 2>/dev/null)";
then
      # try wget maybe?
   echo "Please install curl. Aborted."
   exit 1
fi
command_7z=""
if ! test -x "$( which 7z 2>/dev/null)";
then
   if ! test -x "$( which 7za 2>/dev/null)";
   then
      # try wget maybe?
      echo "Please install 7zip. Try package p7zip. Aborted."
      exit 1
   else
      command_7z="$( which 7za 2>/dev/null)";
   fi
else
   # 7z is valid
   command_7z="$( which 7z 2>/dev/null)";
fi

# Fetch software source itself
getsource "${sourcefile}" "${temp_sw}"

# Fetch plugins source
getsource "${pluginssourcefile}" "${temp_plugins}"

# Extract software
echo "Extracting ${package}."
extract "${outdir}" -y "${temp_sw}" 1>/dev/null 2>&1 && rm -rf "${temp_sw}" "${temp_sw%%.*z}.tar" 2>/dev/null || { echo "Unable to extract for some reason. Aborted."; exit 1; }

# Extract plugins
echo "Extracting plugins."
extract "${outdir}/Plugins" -y "${temp_plugins}" 1>/dev/null 2>&1 && rm -rf "${temp_plugins}" "${temp_plugins%%.*z}.tar" 2>/dev/null || { echo "Unable to extract plugins. You might experience limited functionality."; }

# Adjust permissions on the directories
chmod -R 0755 "${outdir}/Plugins" "${outdir}/Languages" "${outdir}/Toolbars"

# Initialize config file
if test -f "${ini_source}";
then
   /bin/cp -p "${ini_source}" "${ini_dest}" 2>/dev/null && { echo "Initialized the config file."; }
fi
chmod 0666 "${ini_source}" "${ini_dest}" 2>/dev/null

# Provide final status notification
echo "${package} ${pver} successfully installed."
exit 0
