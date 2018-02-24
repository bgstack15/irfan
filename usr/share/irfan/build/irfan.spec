%define dummy_package 0
%define devtty "/dev/pts/5"
Name:		irfan
Version:	4.50
Release:	2
Summary:	an amazing graphics viewer from another operating system

Group:   Applications/Graphics
License:	Freeware, CC-BY-SA 4.0
URL:		http://bgstack15.wordpress.com
Source0:	irfan.tgz
Source1: http://www.irfanview.info/files/iview450.zip
Source2: http://www.irfanview.info/files/irfanview_plugins_450.zip

Packager:	Bgstack15 <bgstack15@gmail.com>
Buildarch:	noarch
#BuildRequires:	
Requires:	(wine >= 1.3 or /usr/bin/wine)
Requires(pre):	bgscripts >= 1.1-20, curl, p7zip

Provides:	application(irfanview.desktop)

%description
Irfanview is an amazing graphics application for a different platform. Using wine, you can run irfanview on Linux.

%prep
# rpm prep 2018-02-21
#%setup -q
%setup

# the deb gets special insertions to get the SOURCE variables.

%if !%{dummy_package}
   pushd .%{_datadir}/%{name}/app
   7z x %{SOURCE1} 
   cd Plugins ; 7z x %{SOURCE2} ; cd ..
   # Adjust permissions on the directories
   chmod -R 0755 Plugins Languages Toolbars
   popd
   # deb needs the GETFILES command here
   # and takes two lines
%endif

exit 0

%build
# rpm build 2018-02-20
exit 0

%install
# rpm install 2018-02-19
#%make_install
rm -rf %{buildroot}
rsync -a . %{buildroot}/ --exclude='**/.*.swp' --exclude='**/.git'

# Symlink to custom ini file
! test -L .%{_datadir}/%{name}/app/i_view32.ini && ln -sf ../inc/i_view32.ini .%{_datadir}/%{name}/app/

# Solve the readme problem
find %{buildroot} -maxdepth 1 -name 'README.md' -exec rm -f {} \; 2>%{devtty} || :

exit 0

%clean
rm -rf %{buildroot}
exit 0

%post
# rpm post 2018-02-21

# make the config file world-writable
find %{_datadir}/%{name} -type f -regex '.*i_view32.ini.*' -exec chmod 0666 {} + 2>%{devtty}

# Deploy icons
which xdg-icon-resource 1>%{devtty} 2>&1 && {

   # Deploy default application icons
   for theme in hicolor locolor Numix-Circle Lubuntu ;
   do
      shape=square
      case "${theme}" in Numix-Circle) shape=circle;; Lubuntu) shape=Lubuntu;; esac

      # Deploy scalable application icons
      cp -p %{_datadir}/%{name}/inc/icons/apps/irfan-${shape}.svg %{_datadir}/icons/${theme}/scalable/apps/irfan.svg

      # Deploy size application icons
      for size in 16 24 32 48 64 ;
      do
         xdg-icon-resource install --context apps --size "${size}" --theme "${theme}" --novendor --noupdate %{_datadir}/%{name}/inc/icons/apps/irfan-${shape}-${size}.png irfan &
      done
   done

   # Deploy custom application icons
   # custom: Numix-Circle apps 48 uses svg
   cp -p %{_datadir}/%{name}/inc/icons/apps/%{name}-circle.svg %{_datadir}/icons/Numix-Circle/48/apps/irfan.svg &
   # custom: Lubuntu uses svg for size 48
   cp -p %{_datadir}/%{name}/inc/icons/apps/%{name}-lubuntu.svg %{_datadir}/icons/Lubuntu/apps/48/irfan.svg &
   # default
   cp -p %{_datadir}/%{name}/inc/icons/apps/%{name}-square-48.png %{_datadir}/icons/hicolor/48x48/apps/irfan.png
   cp -p %{_datadir}/%{name}/inc/icons/apps/%{name}-square.svg %{_datadir}/icons/hicolor/scalable/apps/irfan.svg

   ## Deploy default mimetype icons
   #for theme in hicolor Numix Lubuntu elementary-xfce ;
   #do
   #
   #   # Deploy scalable mimetype icons
   #   cp -p %{_datarootdir}/%{name}/gui/icons/mimetypes/application-x-custom-${theme}.svg %{_datarootdir}/icons/${theme}/scalable/mimetypes/application-x-custom.svg
   #
   #   # Deploy size mimetype icons
   #   for size in 16 24 32 48 64 ;
   #   do
   #      xdg-icon-resource install --context mimetypes --size "${size}" --theme "${theme}" --novendor --noupdate %{_datarootdir}/%{name}/gui/icons/mimetypes/application-x-custom-${theme}-${size}.png application-x-rdp &
   #   done
   #
   #done
   #
   ## Deploy custom mimetype icons
   ## custom: Numix
   #cp -p %{_datarootdir}/%{name}/gui/icons/mimetypes/application-x-custom-Numix.svg %{_datarootdir}/icons/Numix/48/mimetypes/application-x-rdp.svg

   # Update icon caches
   xdg-icon-resource forceupdate &
   for word in hicolor locolor Numix-Circle Numix Lubuntu elementary-xfce ;
   do
      touch --no-create %{_datadir}/icons/${word}
      gtk-update-icon-cache %{_datadir}/icons/${word} &
   done

} 1>%{devtty} 2>&1

# Deploy desktop file
desktop-file-install --rebuild-mime-info-cache %{_datadir}/%{name}/irfanview.desktop 1>%{devtty} 2>&1

# Remove wine viewer things
for td in $( %{_datadir}/%{name}/build/enumerate-users.sh homedir ) ;
do
   for word in "application/pdf=wine-extension-pdf.desktop;" "image/gif=wine-extension-gif.desktop;" "image/jpeg=wine-extension-jpe.desktop;wine-extension-jfif.desktop;" "image/png=wine-extension-png.desktop;" ;
   do
      tf="${td}/.local/share/applications/mimeinfo.cache"
      test -f "${tf}" && /usr/share/bgscripts/py/updateval.py --apply "${tf}" "${word}" "" 1>%{devtty} 2>&1
   done
done

# Mimetypes and default applications
which xdg-mime 1>/dev/null 2>&1 &&
{
   for user in $( %{_datadir}/%{name}/build/enumerate-users.sh ) ;
   do
   
      # Skip non-user objects
      ! getent passwd "${user}" && continue
   
      # Add new mimetypes
      #su "${user}" -c "xdg-mime install %{_datadir}/%{name}/inc/nonedefined.xml &"
   
      # Assign default applications
      while read line;
      do
         echo "${user} ${line}"
         # Assign mimetype a default application
         su "${user}" -c "test -f ~/.config/mimeapps.list && xdg-mime default irfanview.desktop ${line} &" &
   
         # Deprecated
         #which gio && su "${user}" -c "test -f ~/.config/mimeapps.list && gio mime ${line} irfanview.desktop &" &
   
      done <<'EOW'
image/jpeg
image/gif
image/png
image/tiff
image/bmp
image/ico
image/vnd.adobe.photoshop
EOW
   
      # Update mimetype database
      # only needed if new mimetypes are added
      #which update-mime-database && {
      #   case "${user}" in
      #      root) update-mime-database %{_datadir}/mime & ;;
      #      *) su "${user}" -c "update-mime-database ~${user}/.local/share/mime &" & ;;
      #   esac
      #}
   
   done
} 1>%{devtty} 2>&1

# deploy systemd files
# NONE. see bgscripts for example.

exit 0

%preun
# rpm preun 2018-02-21
if test "$1" = "0" ;
then
{
   # total uninstall

   # Mimetypes and default applications
   which xdg-mime 1>/dev/null 2>&1 &&
   {

      for user in $( %{_datadir}/%{name}/build/enumerate-users.sh ) ;
      do

         # Skip non-user objects
         ! getent passwd "${user}" && continue
   
         # Remove new mimetypes
         #su "${user}" -c "xdg-mime uninstall %{_datadir}/%{name}/inc/irfan-mimeinfo.xml &" &

         # Unassign default applications
         # xdg-mime default undo is not implemented
         # gio uninstall is not implemented
   
         # Update mimetype database
         #which update-mime-database && {
         #   case "${user}" in
         #      root) update-mime-database %{_datarootdir}/mime & ;;
         #      *) su "${user}" -c "update-mime-database ~${user}/.local/share/mime &" & ;;
         #  esac
         #}

      done
   }

   # Remove systemd files
   # NONE. See bgscripts for example.

   # Remove desktop file
   rm -f %{_datadir}/applications/irfanview.desktop
   which update-desktop-database && update-desktop-database -q %{_datadir}/applications &

   # Remove icons
   which xdg-icon-resource && {

      # Remove default application icons
      for theme in hicolor locolor Numix-Circle Lubuntu ;
      do

         # Remove scalable application icons
         rm -f %{_datadir}/icons/${theme}/scalable/apps/irfan.svg

         # Remove size application icons
         for size in 16 24 32 48 64 ;
         do
            xdg-icon-resource uninstall --context apps --size "${size}" --theme "${theme}" --noupdate irfan &
         done

      done

      # Remove custom application icons
      # custom: Numix-Circle apps 48 uses svg
      rm -f %{_datadir}/icons/Numix-Circle/48/apps/irfan.svg
      # custom: Lubuntu uses svg for size 48
      rm -f %{_datadir}/icons/Lubuntu/apps/48/irfan.svg
      # default
      rm -f %{_datadir}/icons/hicolor/48x48/apps/irfan.png
      rm -f %{_datadir}/icons/hicolor/scalable/apps/irfan.svg

      # Remove default mimetype icons
      # NONE. See bgscripts.

      # Remove custom mimetype icons
      # NONE. See bgscripts.

      # Update icon caches
      xdg-icon-resource forceupdate &
      for word in hicolor locolor Numix-Circle Numix Lubuntu elementary-xfce ;
      do
         touch --no-create %{_datadir}/icons/${word}
         gtk-update-icon-cache %{_datadir}/icons/${word} &
      done

   }

} 1>%{devtty} 2>&1
true

fi

exit 0

%postun
# rpm postun 2018-02-20
exit 0

%files
%dir /usr/share/irfan
%dir /usr/share/irfan/inc
%dir /usr/share/irfan/inc/icons
%dir /usr/share/irfan/inc/icons/apps
%dir /usr/share/irfan/build
%dir /usr/share/irfan/build/debian-irfan
%doc %attr(444, -, -) /usr/share/doc/irfan/version.txt
%doc %attr(444, -, -) /usr/share/doc/irfan/README.md
%attr(644, -, -) /usr/share/irfan/irfanview.desktop
/usr/share/irfan/doc
/usr/share/irfan/inc/irfan_ver.txt
/usr/share/irfan/inc/sha256sum.txt
%attr(755, -, -) /usr/share/irfan/inc/install-irfanview.sh
%attr(755, -, -) /usr/share/irfan/inc/irfan-vlc.sh
/usr/share/irfan/inc/extra.txt
%attr(755, -, -) /usr/share/irfan/inc/uninstall-irfanview.sh
/usr/share/irfan/inc/icons/apps/irfan-square-16.png
/usr/share/irfan/inc/icons/apps/irfan-lubuntu.svg
/usr/share/irfan/inc/icons/apps/irfan-clear-48.png
/usr/share/irfan/inc/icons/apps/irfan-circle-24.png
/usr/share/irfan/inc/icons/apps/irfan-square-48.png
/usr/share/irfan/inc/icons/apps/irfan-clear-16.png
/usr/share/irfan/inc/icons/apps/irfan-circle-16.png
/usr/share/irfan/inc/icons/apps/irfan-clear-32.png
/usr/share/irfan/inc/icons/apps/irfan-lubuntu-48.png
/usr/share/irfan/inc/icons/apps/irfan-square-64.png
/usr/share/irfan/inc/icons/apps/irfan-lubuntu-32.png
/usr/share/irfan/inc/icons/apps/irfan-clear-64.png
/usr/share/irfan/inc/icons/apps/irfan-lubuntu-16.png
/usr/share/irfan/inc/icons/apps/irfan-lubuntu-24.png
/usr/share/irfan/inc/icons/apps/irfan-circle-48.png
/usr/share/irfan/inc/icons/apps/irfan-circle-64.png
/usr/share/irfan/inc/icons/apps/irfan-circle.svg
/usr/share/irfan/inc/icons/apps/irfan-square.svg
/usr/share/irfan/inc/icons/apps/irfan-square-24.png
/usr/share/irfan/inc/icons/apps/irfan-clear-24.png
/usr/share/irfan/inc/icons/apps/irfan-circle-32.png
/usr/share/irfan/inc/icons/apps/irfan-clear.svg
/usr/share/irfan/inc/icons/apps/irfan-lubuntu-64.png
/usr/share/irfan/inc/icons/apps/irfan-square-32.png
%attr(755, -, -) /usr/share/irfan/inc/icons/generate-icons.sh
%config %attr(666, -, -) /usr/share/irfan/inc/i_view32.ini
/usr/share/irfan/source
/usr/share/irfan/app
%config %attr(666, -, -) /usr/share/irfan/app/i_view32.ini
/usr/share/irfan/build/get-sources
/usr/share/irfan/build/get-files
%attr(755, -, -) /usr/share/irfan/build/enumerate-users.sh
/usr/share/irfan/build/pack
/usr/share/irfan/build/files-for-versioning.txt
/usr/share/irfan/build/irfan.spec
/usr/share/irfan/build/debian-irfan/compat
/usr/share/irfan/build/debian-irfan/md5sums
/usr/share/irfan/build/debian-irfan/preinst
/usr/share/irfan/build/debian-irfan/prerm
/usr/share/irfan/build/debian-irfan/control
/usr/share/irfan/build/debian-irfan/postrm
/usr/share/irfan/build/debian-irfan/rules
/usr/share/irfan/build/debian-irfan/conffiles
/usr/share/irfan/build/debian-irfan/postinst
%attr(755, -, -) /usr/share/irfan/irfan.sh
%verify(link) /usr/bin/irfan

%changelog
* Tue Nov 29 2016 B Stack <bgstack15@gmail.com>
- initial package built
