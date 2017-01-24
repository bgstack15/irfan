### Overview
irfan is a GNU/Linux package for Irfanview.
It contains the instructions to download and install the Irfanview binaries. It also bundles in icons for different themes, and desktop and mime information. 
For the description of the package itself, view usr/share/irfan/docs/README.txt.

### Building
The recommended way to build an rpm is:

    mkdir -p ~/rpmbuild/SOURCES ~/rpmbuild/RPMS ~/rpmbuild/SPECS ~/rpmbuild/BUILD ~/rpmbuild/BUILDROOT
    mkdir -p ~/rpmbuild/SOURCES/irfan-4.44-3/
    cd ~/rpmbuild/SOURCES/irfan-4.44-3
    git init
    git pull https://github.com/bgstack15/irfan master
    usr/share/irfan/inc/pack rpm

The generated rpm will be in ~/rpmbuild/RPMS/noarch
