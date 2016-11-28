#!/bin/sh
# File: /usr/share/irfan/inc/install-irfanview.sh
# Author: bgstack15
# Startdate: 2016-11-28 10:46
# Title: Script that Installs irfanview
# Purpose: Downloads and installs irfanview from official source
# Package: irfan
# History:
# Usage: Is called during the rpm [install/build/something] phase of the irfan package. Also generally available.
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
      echo "Config file reports version number ${line}"
      iver="${line}"
   fi
done < "${infile}"
sourcefile="http://irfanview.info/files/iview${iver//./}.zip"
pluginssourcefile="http://irfanview.info/files/irfanview_plugins_${iver//./}.zip"

# Fetch irfanview source itself
touch "${temp_iview}" 2>/dev/null || { echo "Cannot modify ${temp_iview}. Run as root, perhaps. Aborted."; exit 1; }
echo "Fetching ${sourcefile}"
if ! test -x "$( which curl 2>/dev/null)";
then
   # try wget maybe?
   echo "Please install curl. Aborted."
   exit 1
fi
curl "${sourcefile}" --progress-bar --referer "${sourcefile}" > "${temp_iview}"

# Fetch plugins source
touch "${temp_plugins}" 2>/dev/null || { echo "Cannot modify ${temp_iview}. Run as root, perhaps. Aborted."; exit 1; }
echo "Fetching ${pluginssourcefile}"
curl "${pluginssourcefile}" --progress-bar --referer "${pluginssourcefile}" > "${temp_plugins}"

# Confirm both files were fetched and larger than 1000 bytes for a decently sized 404 page
if ! test -f "${temp_iview}" || test "$( stat -c "%s" "${temp_iview}" 2>/dev/null)" -lt 1000;
then
   echo "Irfanview zip failed to download: ${temp_iview}. Aborted."
   exit 1
else
   if ! test -f "${temp_plugins}" || test "$( stat -c "%s" "${temp_plugins}" 2>/dev/null)" -lt 1000;
   then
      echo "Plugins zip failed to download: ${temp_plugins}. Aborted."
      exit 1
   fi
fi

# Extract irfanview
echo "Extracting irfanview"
if ! test -x "$( which 7z 2>/dev/null)";
then
   # try wget maybe?
   echo "Please install 7zip. Try package p7zip. Aborted."
   exit 1
fi
7z x -o"${outdir}" -y "${temp_iview}" && rm -rf "${temp_iview}" 2>/dev/null || { echo "Unable to extract for some reason. Aborted."; exit 1; }

# Extract plugins
echo "Extracting plugins"
7z x -o"${outdir}/Plugins" -y "${temp_plugins}" && rm -rf "${temp_plugins}" 2>/dev/null || { echo "Unable to extract plugins. You might experience limited functionality."; }

# Initialize i_view32.ini
if test -f "${ini_source}";
then
   /bin/cp -p "${ini_source}" "${ini_dest}" 2>/dev/null
fi
chmod 0666 "${ini_dest}" 2>/dev/null

# Provide final status notification
echo "irfan ${iver} successfully installed."
exit 0
