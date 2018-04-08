# Readme for Irfanview rpm
irfan is a GNU/Linux package for Irfanview, which is a feature-packed image viewer for Windows. Irfanview is freeware, so this package downloads from the official website the compiled binaries. No source code is available for Irfanview.

Irfan depends on wine to operate correctly on GNU/Linux.

Visit the Irfanview home page at [http://www.irfanview.com/](http://www.irfanview.com/).

# Unique characteristics of this package
My packages tend to wrap the whole application inside the /usr/share/%{name}/app directory. I like to keep it all self-contained on my filesystem.
This package bundles in icons for certain themes and also includes desktop and mime information. 

# Using irfan
To send multiple files from the command line to irfan at once, you might need to one of these commands:

    find . -print0 | xargs -0 /usr/share/irfan/irfan.sh
    find . | xargs -d'\n' /usr/share/irfan/irfan.sh
If there are spaces in the filenames, it will break parsing unless you use the null character (use the *-print0* and *-0*) as a separator.

# Building irfan
A build dependency is my [bgscripts](https://github.com/bgstack15/bgscripts) package.

Download this wrapper package source and run the pack utility.

    package=irfan
    thisver=4.51-1
    mkdir -p ~/rpmbuild/{SOURCES,RPMS,SPECS,BUILD,BUILDROOT}
    cd ~/rpmbuild/SOURCES
    git clone https://github.com/bgstack15/irfan "${package}-${thisver}"
    cd "${package}-${thisver}"
    usr/share/irfan/build/pack rpm

The build script will fetch the official binaries from its [homepage](http://www.irfanview.com/) and check it against its sha256sum against [usr/share/irfan/inc/sha256sum.txt](usr/share/irfan/inc/sha256sum.txt).

The generated rpm will be in ~/rpmbuild/RPMS/noarch.

### Test environments
* Fedora 24-27 Cinnamon and xfce
* Ubuntu 16.04, 16.10, Lxde

# Maintaining this package

## On the mirror server
For a new release from upstream, you have to derive the sha256sum and add it to the sha256sum.txt file. It is recommended to store a local copy of the upstream release files.

    thisver=450
    cd /mnt/public/www/smith122/repo/patch/irfan
    curl -O -J -e "http://irfanview.info/files/iview${thisver}.zip" "http://irfanview.info/files/iview${thisver}.zip"
    curl -O -J -e "http://irfanview.info/files/irfanview_plugins_${thisver}.zip" "http://irfanview.info/files/irfanview_plugins_${thisver}.zip"
    sha256sum *zip > sha256sum.txt

## On the rpmbuild server
For a new version release, download the latest sha256sum file from the maintainer server. And then pull up the list of files that need to be manually updated for version numbers.

    cd ~/rpmbuild/SOURCES/irfan-4.51-1/usr/share/irfan
    curl http://albion320.no-ip.biz/smith122/repo/patch/irfan/sha256sum.txt > ./inc/sha256sum.txt
    vi $( cat build/files-for-versioning.txt )

# Authors
Irfan Skiljan [http://www.irfanview.com/](http://www.irfanview.com)
Bgstack15 [https://bgstack15.wordpress.com](https://bgstack15.wordpress.com)

# License
Irfanview is closed-source (freeware). All the value-add parts of the irfan package are [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

# Credits
Icon derived from a source at http://www.onlinewebfonts.com/icon, licensed CC BY 3.0

# Bugs
On some systems, wine uses a font set that is hard to read in the dialogs, but irfan is still mostly usable. This bug is not present when using wine 1.3.33 in PlayOnLinux, but I was not able to reproduce the effect with wine 1.8, because I don't know what I'm doing.

# References
## Weblinks
1. Irfanview and all plugins [http://www.irfanview.com/download_sites.htm](http://www.irfanview.com/download_sites.htm) 
2. Bgscripts package [https://github.com/bgstack15/bgscripts](https://github.com/bgstack15/bgscripts)
3. Palemoon rpm [https://github.com/bgstack15/palemoon-rpm](https://github.com/bgstack15/palemoon-rpm)

# Changelog
* Tue Nov 29 2016 B Stack <bgstack15@gmail.com>
- initial package built

* Wed Nov 30 2016 B Stack <bgstack15@gmail.com>
- install functionality fully built

* Thu Dec  1 2016 B Stack <bgstack15@gmail.com>
- 4.42-3
- Official first release across different Fedora versions

* Fri Dec  2 2016 B Stack <bgstack15@gmail.com>
- 4.42-4
- fixed scriptlets to configure mime defaults for my standard users
- fixed scriptlets and install script to be POSIX sh

* Tue Dec  6 2016 B Stack <bgstack15@gmail.com>
- 4.42-5
- fixed rpm install scriptlet

* Tue Jan  3 2017 B Stack <bgstack15@gmail.com>
- 4.44-1
- Fixed icon install/uninstall portions
- Updated the install-irfan.sh script to match the install-ffs from freefilesync package
- build generate-icons.sh for converting svg files to png

* Mon Jan 23 2017 B Stack <bgstack15@gmail.com> 4.44-2
- rewrote installation to use a customized winetricks installation

* Tue Jan 24 2017 B Stack <bgstack15@gmail.com> 4.44-3
- Updating normal installer to match the fixes made for 4.44-2 which was not published.
- Added readme to root dir for github visitors
- rewrote icon deployment to match bgscripts template

* Fri Jan 27 2017 B Stack <bgstack15@gmail.com> 4.44-4
- Changed path conversion to use winepath which works way better than manual sed commands.
- Rewrote irfan.sh to allow tgz and zip file and directory expansion.

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

* Wed Feb 21 2018 B Stack <bgstack15@gmail.com> 4.50-2
- Modernized package directory layout and build process and scriptlets/maintainer scripts
- Updated package dependencies to be more tolerant of possible wine versions

* Sun Apr  8 2018 B Stack <bgstack15@gmail.com> 4.51-1
- Update to use latest upstream
