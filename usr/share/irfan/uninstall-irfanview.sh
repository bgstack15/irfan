#!/bin/bash
test -x /usr/share/bgscripts/framework.sh && . /usr/share/bgscripts/framework.sh

# Definitions
package="irfan"
installdir=/usr/share/irfan/irfanview
ini_source=${RPM_BUILD_ROOT}/usr/share/${package}/inc/i_view32.ini
ini_dest=${RPM_BUILD_ROOT}/usr/share/${package}/irfanview/i_view32.ini
devtty=/dev/pts/2

exec 1> ${devtty}; exec 2> ${devtty}

# Bup config if different from package-installed file
if ! cmp "${ini_dest}" "${ini_source}" 1>/dev/null 2>&1;
then
   /bin/cp -p "${ini_dest}" "${ini_source}.$( date "+%Y-%m-%d" ).uninstalled" 2>/dev/null
fi

# Remove software directory
rm -rf "${installdir:-NOTHINGTODEL}" 2>/dev/null && mkdir "${installdir}" 2>/dev/null;

# Provide final status notification
exec 1>&-; exec 2>&-
echo "${package} successfully removed."
exit 0
