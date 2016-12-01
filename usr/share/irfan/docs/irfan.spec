# spec file for irfanview 4.42 compiled from template and by hand
# bgscripts15@gmail.com
Name:		irfan
Version:	4.42
Release:	3%{?dist}
Summary:	Irfanview 4.42 packaged for Fedora 24

Group:		Applications/Graphics
License:	Installer is CC-BY-SA
URL:		http://bgstack15.wordpress.com
Source0:	irfan.tgz

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	noarch
#BuildRequires:	
Requires:	wine >= 1.3
Requires(pre):	bgscripts >= 1.1-20, curl, p7zip

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
/usr/share/irfan/install-irfanview.sh || exit 1
desktop-file-install --rebuild-mime-info-cache /usr/share/irfan/irfanview.desktop
#/usr/share/irfan/install-irfanview.sh || exit 1

# Remove wine viewer things
/usr/bgscripts/updateval.py --apply /home/bgstack15-local/.local/share/applications/mimeinfo.cache "application/pdf=wine-extension-pdf.desktop;" "" >/dev/null 2&>1
/usr/bgscripts/updateval.py --apply /home/bgstack15-local/.local/share/applications/mimeinfo.cache "image/gif=wine-extension-gif.desktop;" "" >/dev/null 2&>1
/usr/bgscripts/updateval.py --apply /home/bgstack15-local/.local/share/applications/mimeinfo.cache "image/jpeg=wine-extension-jpe.desktop;wine-extension-jfif.desktop;" "" >/dev/null 2&>1
/usr/bgscripts/updateval.py --apply /home/bgstack15-local/.local/share/applications/mimeinfo.cache "image/png=wine-extension-png.desktop;" "" >/dev/null 2&>1 ||:
# Set default application
while read line;
do
   ( which gvfs-mime >/dev/null 2>&1) && gvfs-mime --set "${line}" irfanview.desktop 1>/dev/null 2>&1
   ( which xdg-mime >/dev/null 2>&1) && xdg-mime default irfanview.desktop "${line}" 1>/dev/null 2>&1
done <<'EOW'
image/jpeg
image/gif
image/png
image/tiff
image/bmp
EOW
exit 0

%preun
if test "$1" = "0";
then
   # total uninstall
   /usr/share/irfan/uninstall-irfanview.sh ||:
fi

%postun
if test "$1" = "0";
then
   # total uninstall
   rm -f /usr/share/applications/irfanview.desktop >/dev/null 2>&1 ||:
   if ( which update-desktop-database 1>/dev/null );
   then
      update-desktop-database -q /usr/share/applications
   fi
fi

%files
/usr
/usr/share
/usr/share/irfan
/usr/share/irfan/docs
/usr/share/irfan/docs/files-for-versioning.txt
/usr/share/irfan/docs/irfan.spec
%doc %attr(444, -, -) /usr/share/irfan/docs/packaging.txt
%doc %attr(444, -, -) /usr/share/irfan/docs/README.txt
%attr(755, -, -) /usr/share/irfan/irfan.sh
%attr(755, -, -) /usr/share/irfan/uninstall-irfanview.sh
%attr(755, -, -) /usr/share/irfan/install-irfanview.sh
/usr/share/irfan/inc
/usr/share/irfan/inc/winetricks
%config %attr(666, -, -) /usr/share/irfan/inc/i_view32.ini
/usr/share/irfan/inc/scrub.txt
/usr/share/irfan/inc/sha256sum.txt
/usr/share/irfan/inc/irfanview32x32.png
%attr(755, -, -) /usr/share/irfan/inc/irfan-vlc.sh
/usr/share/irfan/inc/irfan_ver.txt
%attr(755, -, -) /usr/share/irfan/inc/localize_git.sh
/usr/share/irfan/inc/irfanview64x64.png
%attr(644, -, -) /usr/share/irfan/irfanview.desktop
%changelog
* Wed Nov 30 2016 B Stack <bgstack15@gmail.com>
- install functionality fully built

* Tue Nov 29 2016 B Stack <bgstack15@gmail.com>
- initial package built
