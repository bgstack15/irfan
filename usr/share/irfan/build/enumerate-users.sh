#!/bin/sh
# File: enumerate-users.sh
# goal: output one per line: list of all known users, or alternatively all home directories
outputtype="${1}"
sssd_cache=/var/lib/sss/mc/passwd

case "${outputtype}" in
   homedir) col=6;; # homedir
   *) col=1;;       # user
esac

{

   # list all local objects
   getent passwd | awk -F':' -v "col=${col}" '$7 !~/nologin|shutdown|halt|sync/{print $col}' ;

   # list all domain objects
   strings "${sssd_cache}" 2>/dev/null | while read word ;
   do 
      case "${col}" in
         6) test -d "${word}" 2>/dev/null && echo "${word}" ;;
         *) getent passwd "${word}" 2>/dev/null | awk -F':' -v "col=${col}" '$7 !~/nologin|shutdown|halt|sync/{print $col}' ;;
      esac
   done
} 2>/dev/null | sort | uniq
