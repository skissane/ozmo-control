#!/bin/bash
_pwd="$(ssh sysadmin@192.168.1.211 sudo getent shadow ozmo | cut -d: -f2)"
if [[ "$_pwd" = \$* ]]; then
	echo UNLOCKED
elif [[ "$_pwd" = \!* ]]; then
	echo LOCKED
else
	echo ERROR: ozmo user account status could not be determined
	exit 1
fi
