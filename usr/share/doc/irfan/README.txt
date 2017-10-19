Irfan README
###Readme
Irfanview is an image viewer for Windows. Irfan is an rpm that wraps around the application so, with wine, the application will run on Linux.
http://www.irfanview.com/

To send multiple files from the command line to irfan at once, you might need to one of these commands:
find . -print0 | xargs -0 /usr/share/irfan/irfan.sh
find . | xargs -d'\n' /usr/share/irfan/irfan.sh
If there are spaces in the filenames, it will break parsing unless you use the null character as a separator.

###Authors
Irfan Skiljan http://www.irfanview.com/
bgstack15@gmail.com http://bgstack15.wordpress.com/

###Install
wine
   Wine should be configured to mount z:\ as the linux / (root) directory for Irfanview to operate correctly when directly opening files.

###Test environments
Korora 24 Xfce
Korora 24 Cinnamon
Fedora 25 Cinnamon
Lubuntu 16.10 Lxde
Irfanview 4.50 and all plugins http://www.irfanview.com/download_sites.htm 

###License
Irfanview is closed-source (freeware). Everything else is either GPL or CC-BY-SA4.0.

###Credits
Icon derived from a source at http://www.onlinewebfonts.com/icon, licensed CC BY 3.0

###Bugs
The font is weird in the dialogs, but is still mostly usable. This bug is not present when using wine 1.3.33 in PlayOnLinux, but I was not able to reproduce the effect with wine 1.8, because I don't know what I'm doing.

###How to maintain this package
####On the mirror server

    # Download the latest irfanview version from:
    cd /mnt/public/www/smith122/repo/rpm/irfan/
    thisver=450
    curl -O -J -e http://irfanview.info/files/iview${thisver}.zip http://irfanview.info/files/iview${thisver}.zip 
    curl -O -J -e http://irfanview.info/files/irfanview_plugins_${thisver}.zip http://irfanview.info/files/irfanview_plugins_${thisver}.zip
    # You need to collect the sha256sum for each iview442.zip and irfanview_plugins_442.zip files and put them into the usr/share/irfan/inc/sha256sum.txt file.
    sha256sum iview*.zip irfanview_plugins*.zip > sha256sum.txt

####On the rpmbuild server
    curl http://albion320.no-ip.biz/smith122/repo/rpm/irfan/sha256sum.txt > ~/rpmbuild/SOURCES/irfan-4.50-1/usr/share/irfan/inc/sha256sum.txt

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

###Changelog
* Wed Mar 15 2017 B Stack <bgstack15@gmail.com> 4.44-5
- Fixed the devtty issue in irfan.sh
- Updated the install script for the smith122rpm repo

* Sun Jun  4 2017 B Stack <bgstack15@gmail.com> 4.44-6
- Updated deb package dependencies for ubuntu 16.04
-  wine instead of wine-stable
-  p7zip-full instead of p7zip

* Wed Oct 18 2017 B Stack <bgstack15@gmail.com> 4.50-1
- Bumped version to latest upstream version
- Rearranged directory structure to match current standards
