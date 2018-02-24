#!/bin/sh
# File: /usr/share/irfan/inc/uninstall-irfanview.sh
# Author: bgstack15
# Startdate: 2016-11-29 08:58
# Title: Script that uninstalls irfanview
# Purpose: Removes the irfanview that was downloaded and installed
# Package: irfan
# History:
#    2017-01-02 updated
#    2018-02-20 deprecated, but still available
# Usage: In case you want to clean up manually. This is no longer used by the rpm/deb build utility.
# Reference: install-irfanview.sh
# Improve:

# Definitions
package="irfan"
infile=/usr/share/${package}/inc/irfan_ver.txt
outdir=/usr/share/${package}/irfanview
pver="" # dynamically defined by /usr/share/irfan/inc/irfan_ver.txt
temp_sw=/usr/share/${package}/source/iview.zip
temp_plugins=/usr/share/${package}/source/irfanview_plugins.zip
ini_source=/usr/share/${package}/inc/i_view32.ini
ini_dest=/usr/share/${package}/irfanview/i_view32.ini

# Bup config if different from package-installed file
if ! cmp "${ini_dest}" "${ini_source}" 1>/dev/null 2>&1;
then
   /bin/cp -p "${ini_dest}" "${ini_source}.$( date "+%Y-%m-%d" ).uninstalled" 2>/dev/null
fi

# Remove software directory
rm -rf "${outdir:-NOTHINGTODEL}" 2>/dev/null && mkdir "${outdir}" 2>/dev/null;

# Provide final status notification
echo "irfan successfully removed."
exit 0
