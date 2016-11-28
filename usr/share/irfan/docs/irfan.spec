# spec file for irfanview 4.42 compiled from template and by hand
# bgscripts15@gmail.com
Name:		irfan
Version:	4.42
Release:	2%{?dist}
Summary:	Irfanview 4.42 packaged for Fedora 24

Group:		Applications/Graphics
License:	Installer is CC-BY-SA
URL:		http://bgstack15.wordpress.com
Source0:	irfan.tgz

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	noarch
#BuildRequires:	
Requires:	wine >= 1.3
PreReq:		bgscripts >= 1.1-18, curl, p7zip
# will need 7z or gunzip or something

%description
Irfanview is an amazing graphics application for a different platform. Using wine, you can run irfanview on Linux.

%prep
#%setup -q
%setup

%build

%install
#%make_install
rsync -a . %{buildroot}/

%clean
rm -rf ${buildroot}

%post
/usr/share/irfan/inc/install-irfanview.sh
desktop-file-install /usr/share/irfan/Irfanview.desktop

%postun
rm -f /usr/share/applications/Irfanview.desktop >/dev/null 2>&1

%files
/usr
/usr/share
/usr/share/irfan
/usr/share/irfan/inc
/usr/share/irfan/inc/irfan_ver.txt
%attr(755, -, -) /usr/share/irfan/inc/install-irfanview.sh
%config %attr(666, -, -) /usr/share/irfan/inc/i_view32.ini
/usr/share/irfan/inc/irfanview64x64.png
/usr/share/irfan/inc/winetricks
%attr(755, -, -) /usr/share/irfan/inc/irfan-vlc.sh
/usr/share/irfan/inc/irfanview32x32.png
/usr/share/irfan/irfanview
/usr/share/irfan/source
%attr(644, -, -) /usr/share/irfan/Irfanview.desktop
%attr(755, -, -) /usr/share/irfan/irfan.sh
/usr/share/irfan/docs
%doc %attr(444, -, -) /usr/share/irfan/docs/packaging.txt
%doc %attr(444, -, -) /usr/share/irfan/docs/README.txt
/usr/share/irfan/docs/irfan.spec
/usr/share/irfan/docs/packaging.orig
