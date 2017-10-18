Name:		irfan
Version:	4.50
Release:	1
Summary:	an amazing graphics viewer from another operating system

Group:		Applications/Graphics
License:	Installer is CC-BY-SA, application is freeware
URL:		http://bgstack15.wordpress.com
Source0:	irfan.tgz

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	noarch
#BuildRequires:	
Requires:	wine >= 1.3
Requires(pre):	bgscripts >= 1.1-20, curl, p7zip

Provides:	application(irfanview.desktop)

%description
Irfanview is an amazing graphics application for a different platform. Using wine, you can run irfanview on Linux.

%prep
#%setup -q
%setup

%build

%install
#%make_install
rm -rf %{buildroot}
rsync -a . %{buildroot}/ --exclude='**/.*.swp'

# Make symlinks
for word in irfan;
do
   ln -sf ../share/%{name}/${word}.sh %{buildroot}%{_bindir}/${word}
done

# Run install script
if test -x %{buildroot}%{_datarootdir}/%{name}/install-irfanview.sh;
then
   %{buildroot}%{_datarootdir}/%{name}/install-irfanview.sh || exit 1
else
   :
fi

%clean
rm -rf %{buildroot}

%post
# rpm post 2017-01-24
# Deploy icons
which xdg-icon-resource 1>/dev/null 2>&1 && {

   # Deploy default application icons
   for theme in hicolor locolor Numix-Circle;
   do
      shape=square
      case "${theme}" in Numix-Circle) shape=circle;; Lubuntu) shape=Lubuntu;; esac

      # Deploy scalable application icons
      cp -p %{_datarootdir}/%{name}/inc/icons/apps/irfan-${shape}.svg %{_datarootdir}/icons/${theme}/scalable/apps/irfan.svg

      # Deploy size application icons
      for size in 16 24 32 48 64;
      do
         xdg-icon-resource install --context apps --size "${size}" --theme "${theme}" --novendor --noupdate %{_datarootdir}/%{name}/inc/icons/apps/irfan-${shape}-${size}.png irfan &
      done
   done

   # Deploy custom application icons
   # custom: Numix-Circle apps 48 uses svg
   cp -p %{_datarootdir}/%{name}/inc/icons/%{name}-circle.svg %{_datarootdir}/icons/Numix-Circle/48/apps/irfan.svg &
   # custom: Lubuntu uses svg for size 48
   cp -p %{_datarootdir}/%{name}/inc/icons/%{name}-lubuntu.svg %{_datarootdir}/icons/Lubuntu/apps/48/irfan.svg &
   # default
   cp -p %{_datarootdir}/%{name}/inc/icons/%{name}-square-48.png %{_datarootdir}/icons/hicolor/48x48/apps/irfan.png
   cp -p %{_datarootdir}/%{name}/inc/icons/%{name}-square.svg %{_datarootdir}/icons/hicolor/scalable/apps/irfan.svg

   # Update icon caches
   xdg-icon-resource forceupdate &
   for word in hicolor locolor Numix-Circle Numix Lubuntu elementary-xfce;
   do
      touch --no-create %{_datarootdir}/icons/${word}
      gtk-update-icon-cache %{_datarootdir}/icons/${word} &
   done

} 1>/dev/null 2>&1

# Deploy desktop file
desktop-file-install --rebuild-mime-info-cache %{_datarootdir}/%{name}/irfanview.desktop 1>/dev/null 2>&1

# Remove wine viewer things
for user in bgstack15 bgstack15-local Bgstack15;
do
   for word in "application/pdf=wine-extension-pdf.desktop;" "image/gif=wine-extension-gif.desktop;" "image/jpeg=wine-extension-jpe.desktop;wine-extension-jfif.desktop;" "image/png=wine-extension-png.desktop;";
   do
      /usr/share/bgscripts/updateval.py --apply /home/"${user}"/.local/share/applications/mimeinfo.cache "${word}" "" 1>/dev/null 2>&1
   done
done

# Set default application
for user in root ${SUDO_USER} Bgstack15 bgstack15 bgstack15-local;
do
{
   ! getent passwd "${user}" && continue
   while read line;
   do
      which xdg-mime && {
         #su "${user}" -c "xdg-mime install %{_datarootdir}/%{name}/inc/nonedefined.xml &"
         su "${user}" -c "xdg-mime default irfanview.desktop ${line} &"
      }
      which gio && {
         su "${user}" -c "gio mime  ${line} irfanview.desktop &"
      }
      #which update-mime-database && {
      #   case "${user}" in
      #      root) update-mime-database %{_datarootdir}/mime & ;;
      #      *) su "${user}" -c "update-mime-database ~${user}/.local/share/mime &";;
      #   esac
      #}
   done <<'EOW'
image/jpeg
image/gif
image/png
image/tiff
image/bmp
EOW
} 1>/dev/null 2>&1
done
exit 0

%preun
# rpm preun 2017-01-02
# if I ever need preun Remove mimetype definitions, check freefilesync.rpm
exit 0

%postun
# rpm postun 2017-01-24
if test "$1" = "0";
then
{
   # total uninstall
   
   # Remove desktop file
   rm -f %{_datarootdir}/applications/irfanview.desktop
   which update-desktop-database && update-desktop-database -q %{_datarootdir}/applications &

   # Remove icons
   which xdg-icon-resource && {

      # Remove default application icons
      for theme in hicolor locolor Numix-Circle;
      do

         # Remove scalable application icons
         rm -f %{_datarootdir}/icons/${theme}/scalable/apps/irfan.svg

         # Remove size application icons
         for size in 16 24 32 48 64;
         do
            xdg-icon-resource uninstall --context apps --size "${size}" --theme "${theme}" --noupdate irfan &
         done

      done

      # Remove custom application icons
      # custom: Numix-Circle apps 48 uses svg
      rm -f %{_datarootdir}/icons/Numix-Circle/48/apps/irfan.svg
      # custom: Lubuntu uses svg for size 48
      rm -f %{_datarootdir}/icons/Lubuntu/apps/48/irfan.svg
      # default
      rm -f %{_datarootdir}/icons/hicolor/48x48/apps/irfan.png
      rm -f %{_datarootdir}/icons/hicolor/scalable/apps/irfan.svg

      # Update icon caches
      xdg-icon-resource forceupdate &
      for word in hicolor locolor Numix-Circle Numix Lubuntu elementary-xfce;
      do
         touch --no-create %{_datarootdir}/icons/${word}
         gtk-update-icon-cache %{_datarootdir}/icons/${word} &
      done

   }
} 1>/dev/null 2>&1
fi
exit 0

%files
%dir /usr/share/irfan
%dir /usr/share/irfan/source
%dir /usr/share/irfan/inc
%dir /usr/share/irfan/inc/icons
%dir /usr/share/irfan/docs
%dir /usr/share/irfan/docs/debian-irfan
/usr/bin/irfan
%attr(755, -, -) /usr/share/irfan/irfan.sh
%attr(755, -, -) /usr/share/irfan/install-irfanview.sh
/usr/share/irfan/inc/pack
%attr(755, -, -) /usr/share/irfan/inc/localize_git.sh
/usr/share/irfan/inc/icons/irfan-circle-64.png
/usr/share/irfan/inc/icons/irfan-circle-24.png
/usr/share/irfan/inc/icons/irfan-clear-16.png
%attr(755, -, -) /usr/share/irfan/inc/icons/generate-icons.sh
/usr/share/irfan/inc/icons/irfan-lubuntu-24.png
/usr/share/irfan/inc/icons/irfan-square-16.png
/usr/share/irfan/inc/icons/irfan-lubuntu-48.png
/usr/share/irfan/inc/icons/irfan-clear.svg
/usr/share/irfan/inc/icons/irfan-clear-64.png
/usr/share/irfan/inc/icons/irfan-square-32.png
/usr/share/irfan/inc/icons/irfan-square-64.png
/usr/share/irfan/inc/icons/irfan-circle-48.png
/usr/share/irfan/inc/icons/irfan-square-48.png
/usr/share/irfan/inc/icons/irfan-clear-48.png
/usr/share/irfan/inc/icons/irfan-lubuntu-32.png
/usr/share/irfan/inc/icons/irfan-clear-24.png
/usr/share/irfan/inc/icons/irfan-clear-32.png
/usr/share/irfan/inc/icons/irfan-circle-16.png
/usr/share/irfan/inc/icons/irfan-circle-32.png
/usr/share/irfan/inc/icons/irfan-lubuntu.svg
/usr/share/irfan/inc/icons/irfan-circle.svg
/usr/share/irfan/inc/icons/irfan-square-24.png
/usr/share/irfan/inc/icons/irfan-square.svg
/usr/share/irfan/inc/icons/irfan-lubuntu-16.png
/usr/share/irfan/inc/icons/irfan-lubuntu-64.png
%attr(755, -, -) /usr/share/irfan/inc/irfan-vlc.sh
/usr/share/irfan/inc/winetricks
/usr/share/irfan/inc/scrub.txt
%config %attr(666, -, -) /usr/share/irfan/inc/i_view32.ini
/usr/share/irfan/inc/sha256sum.txt
/usr/share/irfan/inc/irfan_ver.txt
%attr(755, -, -) /usr/share/irfan/uninstall-irfanview.sh
/usr/share/irfan/docs/irfan.spec
/usr/share/irfan/docs/files-for-versioning.txt
%doc %attr(444, -, -) /usr/share/irfan/docs/packaging.txt
/usr/share/irfan/docs/irfan-version.txt
/usr/share/irfan/docs/debian-irfan/control
/usr/share/irfan/docs/debian-irfan/prerm
/usr/share/irfan/docs/debian-irfan/postinst
/usr/share/irfan/docs/debian-irfan/preinst
/usr/share/irfan/docs/debian-irfan/conffiles
/usr/share/irfan/docs/debian-irfan/md5sums
/usr/share/irfan/docs/debian-irfan/postrm
%doc %attr(444, -, -) /usr/share/irfan/docs/README.txt
%attr(644, -, -) /usr/share/irfan/irfanview.desktop
/usr/share/irfan/irfanview

%changelog
* Wed Oct 18 2017 B Stack <bgstack15@gmail.com> 4.50-1
- Updated content. See doc/README.txt

* Fri Jan 27 2017 B Stack <bgstack15@gmail.com> 4.44-4
- Changed path conversion to use winepath which works way better than manual sed commands.
- Rewrote irfan.sh to allow tgz and zip file and directory expansion.

* Tue Jan 24 2017 B Stack <bgstack15@gmail.com> 4.44-3
- Updating normal installer to match the fixes made for 4.44-2 which was not published.
- Added readme to root dir for github visitors
- rewrote icon deployment to match bgscripts template

* Mon Jan 23 2017 B Stack <bgstack15@gmail.com> 4.44-2
- rewrote installation to use a customized winetricks installation

* Tue Jan  3 2017 B Stack <bgstack15@gmail.com>
- 4.44-1
- Fixed icon install/uninstall portions
- Updated the install-irfan.sh script to match the install-ffs from freefilesync package
- build generate-icons.sh for converting svg files to png

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
