Name:		irfan
Version:	4.42
#Release:	3%{?dist}
Release:	6
Summary:	Irfanview 4.42, a graphics viewer

Group:		Applications/Graphics
License:	Installer is CC-BY-SA, application is freeware
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
if test -x %{buildroot}/usr/share/irfan/install-irfanview.shWORKHERE;
then
   %{buildroot}/usr/share/irfan/install-irfanview.sh || exit 1
else
   :
fi

%clean
rm -rf ${buildroot}

%post
# Deploy icons
which xdg-icon-resource 1>/dev/null 2>&1 && {
   for num in 16 24 32 48 64;
   do
      for thistheme in hicolor locolor Numix-Circle;
      do
      thisshape=square
      case "${thistheme}" in
         Numix-Circle) thisshape=round;;
      esac
      xdg-icon-resource install --context apps --size "${num}" --theme "${thistheme}" --novendor --noupdate %{buildroot}/usr/share/irfan/inc/icons/irfan-${num}-${thisshape}.png irfan 1>/dev/null 2>&1
      done
   done
   test -d %{_datarootdir}/icons/hicolor/scalable/ && cp -p %{buildroot}/usr/share/irfan/inc/icons/irfan.svg %{_datarootdir}/icons/hicolor/scalable/ 1>/dev/null 2>&1
   xdg-icon-resource forceupdate 1>/dev/null 2>&1
}

# Deploy desktop file
desktop-file-install --rebuild-mime-info-cache %{buildroot}/usr/share/irfan/irfanview.desktop 1>/dev/null 2>&1

# Remove wine viewer things
for thisuser in bgstack15 bgstack15-local Bgstack15;
do
   for word in "application/pdf=wine-extension-pdf.desktop;" "image/gif=wine-extension-gif.desktop;" "image/jpeg=wine-extension-jpe.desktop;wine-extension-jfif.desktop;" "image/png=wine-extension-png.desktop;";
   do
      /usr/bgscripts/updateval.py --apply /home/"${thisuser}"/.local/share/applications/mimeinfo.cache "${word}" "" 1>/dev/null 2>&1
   done
done
# Set default application
for thisuser in root ${SUDO_USER} Bgstack15 bgstack15 bgstack15-local;
do
   ! getent passwd "${thisuser}" 1>/dev/null 2>&1 && continue
   while read line;
   do
      which gvfs-mime 1>/dev/null 2>&1 && su "${thisuser}" -c "gvfs-mime --set \"${line}\" irfanview.desktop 1>/dev/null 2>&1"
      which xdg-mime 1>/dev/null 2>&1 && su "${thisuser}" -c "xdg-mime default irfanview.desktop \"${line}\" 1>/dev/null 2>&1"
   done <<'EOW'
image/jpeg
image/gif
image/png
image/tiff
image/bmp
EOW
done
exit 0

%preun
exit 0

%postun
if test "$1" = "0";
then
   # total uninstall
   
   # Remove desktop file
   rm -f %{_datarootdir}/applications/irfanview.desktop >/dev/null 2>&1 ||:
   if ( which update-desktop-database 1>/dev/null );
   then
      update-desktop-database -q %{_datarootdir}/applications
   fi

   # Remove icons
   which xdg-icon-resource 1>/dev/null 2>&1 && {
      for num in 16 24 32 48 64;
         do
         for thistheme in hicolor locolor Numix-Circle;
         do
         thisshape=square
         case "${thistheme}" in
            Numix-Circle) thisshape=round;;
         esac
         xdg-icon-resource uninstall --context apps --size "${num}" --theme "${thistheme}" --noupdate irfan 1>/dev/null 2>&1
         done
      done
      rm -f %{_datarootdir}/icons/hicolor/scalable/irfan.svg 1>/dev/null 2>&1
      xdg-icon-resource forceupdate 1>/dev/null 2>&1
   }
fi

%files
/usr
/usr/share
/usr/share/irfan
/usr/share/irfan/inc
/usr/share/irfan/inc/irfan_ver.txt
%config %attr(666, -, -) /usr/share/irfan/inc/i_view32.ini
/usr/share/irfan/inc/irfanview64x64.png
/usr/share/irfan/inc/sha256sum.txt
/usr/share/irfan/inc/scrub.txt
/usr/share/irfan/inc/winetricks
%attr(755, -, -) /usr/share/irfan/inc/irfan-vlc.sh
/usr/share/irfan/inc/irfanview32x32.png
%attr(755, -, -) /usr/share/irfan/inc/localize_git.sh
%attr(755, -, -) /usr/share/irfan/install-irfanview.sh
%attr(644, -, -) /usr/share/irfan/irfanview.desktop
/usr/share/irfan/irfanview
%attr(755, -, -) /usr/share/irfan/uninstall-irfanview.sh
/usr/share/irfan/source
%attr(755, -, -) /usr/share/irfan/irfan.sh
/usr/share/irfan/docs
%doc %attr(444, -, -) /usr/share/irfan/docs/packaging.txt
%doc %attr(444, -, -) /usr/share/irfan/docs/README.txt
/usr/share/irfan/docs/debian
/usr/share/irfan/docs/debian/md5sums
/usr/share/irfan/docs/debian/prerm
/usr/share/irfan/docs/debian/control
/usr/share/irfan/docs/debian/preinst
/usr/share/irfan/docs/debian/postinst
/usr/share/irfan/docs/debian/conffiles
/usr/share/irfan/docs/debian/postrm
/usr/share/irfan/docs/irfan.spec
/usr/share/irfan/docs/files-for-versioning.txt
%changelog
* Tue Dec  6 2016 B Stack <bgstack15@gmail.com>
- 4.42-5
- fixed rpm install scriptlet

* Fri Dec  2 2016 B Stack <bgstack15@gmail.com>
- 4.42-4
- fixed scriptlets to configure mime defaults for my standard users
- fixed scriptlets and install script to be POSIX sh

* Thu Dec  1 2016 B Stack <bgstack15@gmail.com>
- 4.42-3
- Official first release across different Fedora versions

* Wed Nov 30 2016 B Stack <bgstack15@gmail.com>
- install functionality fully built

* Tue Nov 29 2016 B Stack <bgstack15@gmail.com>
- initial package built
