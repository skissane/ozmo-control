#!/bin/bash
ssh sysadmin@192.168.1.211 sudo bash -c '"passwd -l ozmo && loginctl lock-sessions"'
