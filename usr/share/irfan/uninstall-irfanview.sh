#!/bin/sh
# File: /usr/share/irfan/uninstall-irfanview.sh
# Author: bgstack15
# Startdate: 2016-11-29 08:58
# Title: Script that uninstalls irfanview
# Purpose: Removes the irfanview that was downloaded and installed
# Package: irfan
# History:
# Usage: Is called during the rpm uninstall phase iff it is not being upgraded. Also generally available
# Reference: install-irfanview.sh
# Improve:

# Definitions
infile=/usr/share/irfan/inc/irfan_ver.txt
outdir=/usr/share/irfan/irfanview
iver="" # dynamically defined by /usr/share/irfan/inc/irfan_ver.txt
temp_iview=/usr/share/irfan/source/iview.zip
temp_plugins=/usr/share/irfan/source/irfanview_plugins.zip
ini_source=/usr/share/irfan/inc/i_view32.ini
ini_dest=/usr/share/irfan/irfanview/i_view32.ini

# Bup i_view32.ini if different from reference ini
if ! cmp "${ini_dest}" "${ini_source}" 2>/dev/null;
then
   /bin/cp -p "${ini_source}" "${ini_dest}.$( date "+%Y-%m-%d" ).uninstalled" 2>/dev/null
fi

# Remove irfanview directory
rm -rf "${outdir:-NOTHINGTODEL}" 2>/dev/null && mkdir "${outdir}" 2>/dev/null;

# Provide final status notification
echo "irfan successfully removed."
exit 0
