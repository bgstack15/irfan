#!/bin/bash
test -x /usr/share/bgscripts/framework.sh && . /usr/share/bgscripts/framework.sh
test -x /usr/share/bgscripts/bgscripts.bashrc && . /usr/share/bgscripts/bgscripts.bashrc --noclear --nodeps

# Definitions
package="irfan"
installdir=/usr/share/irfan/irfanview
ini_source=${RPM_BUILD_ROOT}/usr/share/${package}/inc/i_view32.ini
ini_dest=${RPM_BUILD_ROOT}/usr/share/${package}/irfanview/i_view32.ini
devtty=/dev/pts/2

# Install software
exec 2>${devtty}; exec 1>${devtty}
if ! test -x /usr/share/irfan/inc/winetricks;
then
   echo "Fatal error: could not find the customized winetricks. Nothing else can happen."
else
   # make the directory
   mkdir -p "${installdir}"; chmod 0777 "${installdir}"
   # so use the customized winetricks
   sudo su -c "DISPLAY=:0 /usr/share/irfan/inc/winetricks -q irfanview --optout"
fi

# Initialize config file
if test -f "${ini_source}";
then
   /bin/cp -p "${ini_source}" "${ini_dest}" && { echo "Initialized the config file."; }
fi
chmod 0666 "${ini_source}" "${ini_dest}" 

exec 1>&-; exec 2>&-
