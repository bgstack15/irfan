Irfan README
###Readme
Irfanview is an image viewer for Windows. Irfan is an rpm that wraps around the application so, with wine, the application will run on Linux.
http://www.irfanview.com/

###Authors
Irfan Skiljan http://www.irfanview.com/
bgstack15@gmail.com http://bgstack15.wordpress.com/

###Install
wine
   Wine should be configured to mount z:\ as the linux / (root) directory for Irfanview to operate correctly when directly opening files.

###Build environment
Korora 24 Xfce
Wine 1.9
Irfanview 4.42 and all plugins http://www.irfanview.com/download_sites.htm 

###License
Irfanview is closed-source (freeware). Everything else is either GPL or CC-BY-SA4.0.

###Credits
Icon derived from a source at http://www.onlinewebfonts.com/icon, licensed CC BY 3.0

###Bugs
The font is weird in the dialogs, but is still mostly usable. This bug is not present when using wine 1.3.33 in PlayOnLinux, but I was not able to reproduce the effect with wine 1.8, because I don't know what I'm doing.

###How to maintain this package
You need to collect the sha256sum for each iview442.zip and irfanview_plugins_442.zip files and put them into the usr/share/irfan/inc/sha256sum.txt file.
####On the mirror server
cd /mnt/mirror/bgscripts/irfanview
shopt -s extglob
sha256sum !(sha256sum.txt) > sha256sum.txt
####On the rpmbuild server
curl http://mirror/bgscripts/irfanview/sha256sum.txt > ~/rpmbuild/irfan-4.42-3/usr/share/irfan/inc/sha256sum.txt

###Future use
# Mimetype list, probably ~/.local/share/applications/mimeapps.list
[Default Applications]
image/png=irfanview.desktop
image/jpeg=irfanview.desktop
image/tiff=irfanview.desktop
image/bmp=irfanview.desktop
image/gif=irfanview.desktop
# possible locations
/usr/share/applications/gnome-mimeapps.list
/usr/share/applications/mimeapps.list
/usr/share/applications/xfce-mimeapps.list
/usr/share/applications/kde-mimeapps.list
/usr/share/applications/x-cinnamon-mimeapps.list
/usr/share/applications/mimeinfo.cache
~/.local/share/applications/mimeinfo.cache
